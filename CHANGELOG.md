# Changelog

All notable changes to Smart Mesh Cleaner Pro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.5.0] - 2026-03-04

### Added

- Smart Trash Bin system with soft-delete functionality
- Restore feature to undo trash operations
- Memory preservation for original collection locations
- Five filter modes (Prefix, Volume, Poly Count, Distance, Empty Geometry)
- Three action modes (Select, Trash, Delete)
- Dynamic UI that adapts to trash bin state
- Confirmation dialog for permanent deletion
- Full undo/redo support for all operations
- Type hints and ABC interfaces for clean architecture
- Professional panel in 3D Viewport sidebar

### Features

- **Name Prefix Filter** - Target objects by naming convention
- **Volume Filter** - Select objects by bounding box volume
- **Polygon Count Filter** - Filter meshes by face count
- **Distance Filter** - Find objects beyond distance threshold
- **Empty Geometry Filter** - Detect meshes with zero vertices
- **Trash Bin** - Non-destructive deletion workflow
- **Restore System** - Return objects to original collections
- **Safe Mode** - Preview selections before acting

### Technical

- Strategy Pattern implementation for filters
- Domain-driven design architecture
- Clean separation of concerns (utilities, filters, UI, operators)
- Efficient filtering algorithms
- Collection management without data corruption

## [Future Releases]

### Planned Features

- Material-based filtering
- Modifier-based filtering
- UV map validation filter
- Batch export selected objects
- Custom filter expressions
- Filter presets/templates
- Statistics and analysis panel
- Multi-language support

### Under Consideration

- Integration with asset libraries
- Cloud backup for trash bin
- Automated cleanup on import
- LOD generation tools
- Scene optimization suggestions

---

## Version History Summary

- **3.5.0** - Initial public release with full feature set
