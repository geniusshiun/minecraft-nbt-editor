# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
