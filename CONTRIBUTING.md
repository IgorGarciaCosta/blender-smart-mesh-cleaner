# Contributing to Smart Mesh Cleaner Pro

First off, thank you for considering contributing to Smart Mesh Cleaner Pro! It's people like you that make this tool better for the entire Blender community.

## 🎯 Ways to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Blender version** you're using
- **Operating system** (Windows, macOS, Linux)
- **Addon version**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Error messages** from Blender console

### 💡 Suggesting Features

Feature suggestions are welcome! Please provide:

- **Clear use case** - What problem does it solve?
- **Expected behavior** - How should it work?
- **Examples** - Are there similar features elsewhere?
- **Priority** - Nice to have vs critical need

### 🔧 Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** following our code style
4. **Test** thoroughly in Blender 3.0+
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add amazing feature for X purpose"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** with a clear description

## 📝 Code Style Guidelines

### Python Style

- Follow **PEP 8** conventions
- Use **type hints** where appropriate
- Keep functions **focused and small**
- Add **docstrings** for complex functions
- Use **meaningful variable names**

### Blender API Conventions

- Use `bpy.types` for class inheritance
- Handle `do_unlink` properly for object removal
- Always validate context before operations
- Use `bl_options` appropriately for operators

### Example Code Style

```python
def process_objects(objects: Sequence[bpy.types.Object]) -> list[str]:
    """Process a list of objects and return their names.

    Args:
        objects: Sequence of Blender objects to process

    Returns:
        List of object names that were processed
    """
    processed = []
    for obj in objects:
        if obj.type == 'MESH':
            processed.append(obj.name)
    return processed
```

## 🧪 Testing

Before submitting:

1. **Test in clean Blender scene** - Start with default cube scene
2. **Test edge cases**:
   - Empty scenes
   - Scenes with no meshes
   - Objects in multiple collections
   - Locked collections
3. **Test all filter modes** - Ensure none are broken
4. **Test trash bin flow**:
   - Move to trash
   - Restore
   - Empty trash
5. **Check for console errors** - No Python errors should appear

## 🎨 New Filter Ideas

If you want to add a new filter mode:

1. Create a class inheriting from `ObjectFilter`
2. Implement `validate()` and `matches()` methods
3. Add to `strategy_map` in operator
4. Add UI controls in panel
5. Add property to `SmartCleanerProperties`
6. Update README with examples

### Filter Template

```python
class MyNewFilter(ObjectFilter):
    def __init__(self, parameter: type):
        self.param = parameter

    def validate(self) -> tuple[bool, str]:
        """Return (is_valid, error_message)"""
        return (True, "")

    def matches(self, obj: bpy.types.Object) -> bool:
        """Return True if object matches filter criteria"""
        return # your logic here
```

## 📚 Documentation

When adding features:

- Update README.md with usage examples
- Add docstrings to new functions
- Update version number in `bl_info`
- Document any new properties

## 🏗️ Architecture Guidelines

The addon follows these principles:

- **Strategy Pattern** for filters
- **Single Responsibility** - One class, one job
- **Open/Closed** - Extend via new filters, not modifications
- **DRY** - Don't repeat yourself

## ❓ Questions?

Feel free to open an issue with the `question` label or start a discussion.

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make this project better for everyone. Whether it's code, bug reports, or suggestions - it all helps!

---

**Happy Coding! 🚀**
