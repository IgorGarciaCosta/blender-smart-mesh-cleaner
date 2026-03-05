from abc import ABC, abstractmethod
from typing import Sequence, Literal
from mathutils import Vector
import bpy
bl_info = {
    "name":        "Smart Mesh Cleaner Pro",
    "author":      "Igor Garcia",
    "version":     (3, 5, 0),
    "blender":     (3, 0, 0),
    "location":    "Sidebar (N) → Clean",
    "description": "Professional cleanup tool with Smart Trash Bin & Restore.",
    "category":    "Object",
}


TRASH_NAME = "🗑️ TRASH_BIN"

# ── Domain: Core Utilities ──────────────────────────────────────


def get_scene_objects() -> list[bpy.types.Object]:
    return list(bpy.context.scene.objects)


def get_trash_collection():
    return bpy.data.collections.get(TRASH_NAME)


def move_to_trash(objects: Sequence[bpy.types.Object]) -> None:
    """Moves objects to a hidden collection and stores their original location."""
    trash_col = get_trash_collection()
    if not trash_col:
        trash_col = bpy.data.collections.new(TRASH_NAME)
        bpy.context.scene.collection.children.link(trash_col)

    # Hide trash by default
    trash_col.hide_viewport = True
    trash_col.hide_render = True

    for obj in objects:
        # 1. Store original collection names in custom property
        original_cols = [
            c.name for c in obj.users_collection if c.name != TRASH_NAME]
        if original_cols:
            obj["origin_cols"] = ",".join(original_cols)

        # 2. Link to Trash
        if obj.name not in trash_col.objects:
            trash_col.objects.link(obj)

        # 3. Unlink from old collections
        for col in obj.users_collection:
            if col != trash_col:
                col.objects.unlink(obj)

    # Deselect everything to avoid confusion
    bpy.ops.object.select_all(action='DESELECT')


def restore_from_trash() -> None:
    """Restores objects to their original collections and deletes the bin."""
    trash_col = get_trash_collection()
    if not trash_col:
        return

    for obj in trash_col.objects:
        # Retrieve original collections
        origin_names = obj.get("origin_cols", "").split(",")
        restored = False

        # Try to link back to original collections
        for name in origin_names:
            col = bpy.data.collections.get(name)
            if col:
                if obj.name not in col.objects:
                    col.objects.link(obj)
                restored = True

        # Fallback: if original collection is gone, link to Scene Collection
        if not restored:
            bpy.context.scene.collection.objects.link(obj)

        # Clean up custom property
        if "origin_cols" in obj:
            del obj["origin_cols"]

    # Delete the Trash Collection
    bpy.data.collections.remove(trash_col)


def empty_trash_bin() -> None:
    """Permanently deletes everything in the trash."""
    trash_col = get_trash_collection()
    if not trash_col:
        return

    # Delete objects inside
    for obj in trash_col.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Delete the collection
    bpy.data.collections.remove(trash_col)


# ── Domain: Strategy Filters ────────────────────────────────────

class ObjectFilter(ABC):
    @abstractmethod
    def validate(self) -> tuple[bool, str]: pass
    @abstractmethod
    def matches(self, obj: bpy.types.Object) -> bool: pass

    def filter(self, objects: list[bpy.types.Object]) -> list[bpy.types.Object]:
        return [obj for obj in objects if self.matches(obj)]


class PrefixFilter(ObjectFilter):
    def __init__(self, prefix: str): self.prefix = prefix
    def validate(self): return (bool(self.prefix), "Prefix empty.")
    def matches(self, obj): return obj.name.startswith(self.prefix)


class VolumeFilter(ObjectFilter):
    def __init__(self, threshold, keep_above):
        self.t = threshold
        self.keep_above = keep_above

    def validate(self): return (True, "")

    def matches(self, obj):
        if obj.type != 'MESH':
            return False
        d = obj.dimensions
        vol = d.x * d.y * d.z
        return vol < self.t if self.keep_above else vol > self.t


class PolyCountFilter(ObjectFilter):
    def __init__(self, threshold, keep_above):
        self.t = threshold
        self.keep_above = keep_above

    def validate(self): return (True, "")

    def matches(self, obj):
        if obj.type != 'MESH':
            return False
        count = len(obj.data.polygons)
        return count < self.t if self.keep_above else count > self.t


class DistanceFilter(ObjectFilter):
    def __init__(self, max_dist): self.max_dist = max_dist
    def validate(self): return (True, "")
    def matches(self, obj): return obj.location.length > self.max_dist


class EmptyMeshFilter(ObjectFilter):
    def validate(self): return (True, "")
    def matches(self, obj): return obj.type == 'MESH' and len(
        obj.data.vertices) == 0

# ── Properties ──────────────────────────────────────────────────


class SmartCleanerProperties(bpy.types.PropertyGroup):
    action_type: bpy.props.EnumProperty(  # type: ignore
        name="Action",
        items=[
            ("SELECT", "Select Only", "Inspect before acting"),
            ("TRASH", "Move to Trash", "Safe Mode with Restore option"),
            ("DELETE", "Delete", "Destroy permanently"),
        ],
        default="SELECT",
    )
    mode: bpy.props.EnumProperty(  # type: ignore
        name="Filter Mode",
        items=[
            ("PREFIX", "Name Prefix", ""),
            ("VOLUME", "Volume (Size)", ""),
            ("POLY", "Poly Count", ""),
            ("DISTANCE", "Lost in Space", ""),
            ("EMPTY", "Empty Geometry", ""),
        ],
        default="PREFIX",
    )
    prefix: bpy.props.StringProperty(
        name="Prefix", default="DEL_")  # type: ignore
    threshold_direction: bpy.props.EnumProperty(  # type: ignore
        items=[("BELOW", "Below", ""), ("ABOVE", "Above", "")], default="BELOW"
    )
    volume_threshold: bpy.props.FloatProperty(
        name="Volume", default=0.1, precision=4)  # type: ignore
    poly_threshold: bpy.props.IntProperty(
        name="Faces", default=100)  # type: ignore
    max_distance: bpy.props.FloatProperty(
        name="Dist (m)", default=100.0)  # type: ignore

# ── UI Panel ────────────────────────────────────────────────────


class VIEW3D_PT_SmartCleaner(bpy.types.Panel):
    bl_label = "Smart Mesh Cleaner"
    bl_idname = "VIEW3D_PT_smart_cleaner"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Clean'

    def draw(self, context):
        layout = self.layout
        props = context.scene.smart_cleaner_props
        trash_exists = get_trash_collection() is not None

        # 1. Action Selector (Disable TRASH option if bin exists to force decision)
        row = layout.row()
        row.prop(props, "action_type", expand=True)
        layout.separator()

        # 2. Filter Settings (Hide if Trash exists to focus on Restore/Empty)
        if props.action_type == 'TRASH' and trash_exists:
            box = layout.box()
            box.label(text="Trash Bin is full!", icon="ERROR")
            box.label(text="Please Empty or Restore first.")
        else:
            layout.label(text="Filter Criteria:")
            layout.prop(props, "mode", text="")

            box = layout.box()
            if props.mode == "PREFIX":
                box.prop(props, "prefix")
            elif props.mode == "VOLUME":
                box.prop(props, "threshold_direction", expand=True)
                box.prop(props, "volume_threshold")
            elif props.mode == "POLY":
                box.prop(props, "threshold_direction", expand=True)
                box.prop(props, "poly_threshold")
            elif props.mode == "DISTANCE":
                box.label(text="Distance from Center:")
                box.prop(props, "max_distance")
            elif props.mode == "EMPTY":
                box.label(text="Meshes with 0 vertices", icon="INFO")

        layout.separator()

        # 3. Dynamic Buttons Logic

        # Case A: TRASH MODE + BIN EXISTS -> Show Restore / Empty
        if props.action_type == 'TRASH' and trash_exists:
            col = layout.column(align=True)
            col.scale_y = 1.5

            # Button 1: Restore
            op_restore = col.operator(
                "mesh.smart_cleaner_restore", text="RESTORE OBJECTS", icon="RECOVER_LAST")

            # Button 2: Empty
            col.separator()
            op_empty = col.operator(
                "mesh.smart_cleaner_empty", text="EMPTY TRASH BIN", icon="TRASH")

        # Case B: TRASH MODE + NO BIN -> Show Move to Trash
        elif props.action_type == 'TRASH' and not trash_exists:
            col = layout.column()
            col.scale_y = 1.5
            col.operator("mesh.smart_cleaner_exec",
                         text="MOVE TO TRASH", icon="FILE_FOLDER")

        # Case C: SELECT or DELETE -> Standard Button
        else:
            btn_text = "EXECUTE DELETE" if props.action_type == "DELETE" else "EXECUTE SELECT"
            icon = "X" if props.action_type == "DELETE" else "RESTRICT_SELECT_OFF"

            col = layout.column()
            col.scale_y = 1.5
            col.operator("mesh.smart_cleaner_exec", text=btn_text, icon=icon)

# ── Operators ───────────────────────────────────────────────────


class MESH_OT_SmartCleanerExec(bpy.types.Operator):
    bl_idname = "mesh.smart_cleaner_exec"
    bl_label = "Execute Action"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.smart_cleaner_props

        # Strategy Setup
        strategy_map = {
            "PREFIX": PrefixFilter(props.prefix),
            "VOLUME": VolumeFilter(props.volume_threshold, props.threshold_direction == "BELOW"),
            "POLY": PolyCountFilter(props.poly_threshold, props.threshold_direction == "BELOW"),
            "DISTANCE": DistanceFilter(props.max_distance),
            "EMPTY": EmptyMeshFilter()
        }

        filtr = strategy_map.get(props.mode)
        if not filtr:
            return {"CANCELLED"}

        valid, msg = filtr.validate()
        if not valid:
            self.report({"WARNING"}, msg)
            return {"CANCELLED"}

        objects = filtr.filter(get_scene_objects())

        if not objects:
            self.report({"WARNING"}, "No objects found.")
            return {"CANCELLED"}

        # Execution
        if props.action_type == "SELECT":
            bpy.ops.object.select_all(action="DESELECT")
            for obj in objects:
                obj.select_set(True)
            self.report({"INFO"}, f"Selected {len(objects)} objects.")

        elif props.action_type == "DELETE":
            bpy.ops.object.select_all(action="DESELECT")
            for obj in objects:
                obj.select_set(True)
            bpy.ops.object.delete()
            self.report({"INFO"}, f"Deleted {len(objects)} objects.")

        elif props.action_type == "TRASH":
            move_to_trash(objects)
            self.report({"INFO"}, f"Moved {len(objects)} objects to Trash.")

        return {"FINISHED"}


class MESH_OT_RestoreTrash(bpy.types.Operator):
    bl_idname = "mesh.smart_cleaner_restore"
    bl_label = "Restore Trash"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        restore_from_trash()
        self.report({"INFO"}, "Objects Restored.")
        return {"FINISHED"}


class MESH_OT_EmptyTrash(bpy.types.Operator):
    bl_idname = "mesh.smart_cleaner_empty"
    bl_label = "Empty Trash"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        empty_trash_bin()
        self.report({"INFO"}, "Trash Emptied.")
        return {"FINISHED"}

# ── Registration ────────────────────────────────────────────────


classes = (
    SmartCleanerProperties,
    MESH_OT_SmartCleanerExec,
    MESH_OT_RestoreTrash,
    MESH_OT_EmptyTrash,
    VIEW3D_PT_SmartCleaner
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.smart_cleaner_props = bpy.props.PointerProperty(
        type=SmartCleanerProperties)


def unregister():
    del bpy.types.Scene.smart_cleaner_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
