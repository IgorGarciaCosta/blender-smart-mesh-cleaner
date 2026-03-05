# 🧹 Smart Mesh Cleaner Pro

[![Blender](https://img.shields.io/badge/Blender-3.0+-orange.svg)](https://www.blender.org/)
[![Version](https://img.shields.io/badge/version-3.5.0-blue.svg)](https://github.com/yourusername/blender-smart-mesh-cleaner)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A professional Blender addon for intelligently cleaning up your 3D scenes with advanced filtering options and a safe trash bin system.

## ✨ Features

### 🎯 Smart Filtering Modes

- **Name Prefix Filter** - Target objects by naming convention (e.g., `DEL_`, `TMP_`, `OLD_`)
- **Volume Filter** - Select objects above or below a specific volume threshold
- **Polygon Count Filter** - Filter meshes by face count (perfect for LOD cleanup)
- **Distance Filter** - Find objects lost in space beyond a certain distance from origin
- **Empty Geometry Filter** - Detect and remove meshes with zero vertices

### 🗑️ Safety-First Trash Bin System

- **Move to Trash** - Soft-delete objects to a hidden collection instead of permanent removal
- **Restore Feature** - Undo mistakes by restoring objects to their original collections
- **Memory Preservation** - Automatically remembers and restores objects to their exact original locations
- **Empty Trash** - Permanently delete when you're ready (with confirmation dialog)

### ⚡ Three Action Modes

1. **Select Only** - Preview what will be affected before taking action
2. **Move to Trash** - Safe mode with full restore capability
3. **Delete** - Permanent removal for when you're absolutely sure

## 📦 Installation

### Method 1: Install from File

1. Download `delete_meshes_by_filter.py`
2. Open Blender
3. Go to `Edit > Preferences > Add-ons`
4. Click `Install...`
5. Select the downloaded `.py` file
6. Enable "Smart Mesh Cleaner Pro" checkbox

### Method 2: Manual Installation

1. Locate your Blender scripts folder:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux**: `~/.config/blender/{version}/scripts/addons/`
2. Copy `delete_meshes_by_filter.py` to the `addons` folder
3. Restart Blender
4. Enable the addon in Preferences

## 🚀 Usage

### Accessing the Panel

1. Open the **3D Viewport**
2. Press `N` to open the sidebar
3. Navigate to the **Clean** tab
4. The Smart Mesh Cleaner panel will appear

### Basic Workflow

#### Example 1: Remove Small Debris

```
1. Select Action: "Move to Trash"
2. Filter Mode: "Volume (Size)"
3. Direction: "Below"
4. Threshold: 0.1
5. Click "MOVE TO TRASH"
6. Review your scene
7. If satisfied, click "EMPTY TRASH BIN"
8. If not, click "RESTORE OBJECTS"
```

#### Example 2: Clean Up Temporary Objects

```
1. Select Action: "Select Only" (preview first)
2. Filter Mode: "Name Prefix"
3. Prefix: "TMP_"
4. Click "EXECUTE SELECT"
5. Review selected objects
6. Change to "Delete" action
7. Click "EXECUTE DELETE"
```

#### Example 3: Remove High-Poly Meshes

```
1. Select Action: "Move to Trash"
2. Filter Mode: "Poly Count"
3. Direction: "Above"
4. Faces: 100000
5. Click "MOVE TO TRASH"
6. Check performance improvement
7. Restore or empty as needed
```

#### Example 4: Find Lost Objects

```
1. Select Action: "Select Only"
2. Filter Mode: "Lost in Space"
3. Distance: 1000
4. Click "EXECUTE SELECT"
5. Review outliers in your scene
```

## 🎨 Use Cases

### Game Asset Optimization

- Remove meshes with too many polygons for real-time rendering
- Clean up tiny objects that won't be visible in-game
- Filter out development scaffolding by prefix

### Scene Cleanup

- Remove empty geometry left over from modeling
- Delete objects accidentally placed far from the scene
- Clean up imported models with excess detail

### Batch Processing

- Use name prefixes to mark objects for deletion across multiple scenes
- Standardize LOD (Level of Detail) management
- Automated cleanup workflow for production pipelines

## 🛡️ Safety Features

- **Non-destructive Preview** - "Select Only" mode lets you see what will be affected
- **Undo Support** - All operations are undo-able with `Ctrl+Z`
- **Trash Bin** - Soft-delete objects with full restore capability
- **Confirmation Dialog** - Empty Trash requires explicit confirmation
- **Collection Memory** - Restored objects return to their exact original collections

## 🔧 Technical Details

### Architecture

The addon is built using object-oriented design principles:

- **Strategy Pattern** - Each filter mode is an independent strategy
- **Domain-Driven Design** - Clear separation between utilities, filters, UI, and operators
- **Clean Code** - Type hints, ABC interfaces, and SOLID principles

### Performance

- Efficient filtering using list comprehensions
- Minimal overhead on Blender's scene graph
- Safe collection management without data corruption

### Compatibility

- **Blender Version**: 3.0 and above
- **Platform**: Windows, macOS, Linux
- **Type**: Add-on (Python script)

## 📖 API Reference

### Filter Classes

All filters inherit from `ObjectFilter` ABC:

- `PrefixFilter(prefix: str)` - Match object names starting with prefix
- `VolumeFilter(threshold: float, keep_above: bool)` - Filter by bounding box volume
- `PolyCountFilter(threshold: int, keep_above: bool)` - Filter by polygon count
- `DistanceFilter(max_dist: float)` - Filter by distance from origin
- `EmptyMeshFilter()` - Match meshes with zero vertices

### Core Functions

```python
move_to_trash(objects: Sequence[bpy.types.Object]) -> None
restore_from_trash() -> None
empty_trash_bin() -> None
get_trash_collection() -> Optional[bpy.types.Collection]
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new filter modes
- 🔧 Submit pull requests
- 📖 Improve documentation
- ⭐ Star this repository

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Igor Garcia**

## 🙏 Acknowledgments

- Built for the Blender community
- Inspired by real production pipeline challenges
- Special thanks to all contributors and users

## 📮 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/blender-smart-mesh-cleaner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/blender-smart-mesh-cleaner/discussions)

---

<p align="center">Made with ❤️ for the Blender Community</p>
