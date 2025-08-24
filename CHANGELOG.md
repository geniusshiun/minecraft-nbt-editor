# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2024-12-19

### 🚀 Major Bedrock NBT Compatibility Improvements

#### Fixed
- **CRITICAL: Fixed Bedrock NBT file corruption** - Resolved issue where Python modifications would break VSCode NBT extension compatibility and Minecraft reading
  - **Root cause**: Bedrock NBT prefix byte 4 contains content length checksum that wasn't being updated
  - **Impact**: Files modified by Python tool would show empty SNBT in VSCode and fail to load in Minecraft
  - **Solution**: Automatically calculate and update checksum (prefix byte 4) when writing modified files
- **Fixed compound tag errors** - Resolved "Top tag should be a compound" errors in VSCode NBT extension
- **Fixed prefix preservation** - Correctly maintain original Bedrock 8-byte prefixes while updating checksums
- **Fixed auto-detection logic** - Improved Bedrock format detection with better scoring system

#### Enhanced
- **Perfect VSCode compatibility** - Python-modified files now produce identical results to VSCode NBT extension
- **Minecraft compatibility** - All experimental features now properly toggle in Bedrock worlds  
- **Robust file format handling** - Supports various Bedrock prefix formats with automatic checksum management
- **Better error reporting** - Clear debugging information for NBT parsing issues

#### Technical Details
- Added `bedrock_prefix` attribute to preserve original 8-byte prefixes
- Implemented content length checksum calculation (prefix[4] = content_length & 0xFF)
- Enhanced `write()` method to update checksums before file output
- Improved auto-detection algorithm with offset-aware parsing
- Added comprehensive test coverage for Bedrock format edge cases

### 🔧 Breaking Changes
- Bedrock NBT files now correctly update internal checksums (may change file headers)
- Previous 0.2.x modified Bedrock files may need to be regenerated for full compatibility

## [0.2.0] - 2025-08-19

### Added
- **NEW: `enable` command** - Quick toggle for Minecraft Bedrock experimental features
  - `minecraft-nbt enable level.dat --exp` - Enable all experimental features at once
  - `--backup` option to create backup before changes
  - Supports 9 experimental features: data_driven_biomes, experimental_creator_cameras, experiments_ever_used, gametest, jigsaw_structures, saved_with_toggled_experiments, upcoming_creator_features, villager_trades_rebalance, y_2025_drop_3
- **Internationalization (i18n) support** - Full English and Chinese language support
  - Automatic language detection based on system locale
  - Complete translation for all CLI messages and help text
- **Enhanced documentation** - Updated README with detailed usage examples
  - Comprehensive command examples for Bedrock edition
  - Dedicated section for `enable` command with feature descriptions

### Fixed
- Resolved import issues in CLI entry points
- Fixed NBT parsing edge cases for Bedrock format
- Improved error handling and user feedback

### Changed
- Improved CLI user experience with rich formatting and emojis
- Better error messages with internationalization support

## [0.1.0] - 2025-08-18

### Added
- Basic NBT file reading and writing
- Support for Java and Bedrock Minecraft formats
- Command line tools for NBT manipulation
- Core NBT operations (get, set, add, remove, search)
- File format detection (compression, endianness, headers)

### Technical Details
- Python 3.8+ compatibility
- Cross-platform support
- Comprehensive test coverage
- MIT License
