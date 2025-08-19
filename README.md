# Minecraft NBT Editor (Python)

A Python-based Minecraft NBT editor supporting Bedrock editions. This project is a complete rewrite of the original VSCode plugin, designed to work on Linux and other platforms.

## Features

- **Full NBT Support**: All NBT tag types (Byte, Short, Int, Long, Float, Double, String, ByteArray, IntArray, LongArray, List, Compound)
- **Multi-Format Support**: .dat, .nbt, .mca, .mcstructure files
- **Complete Editing Operations**: Create, Read, Update, Delete, Move, Composite edits
- **Bedrock Minecraft Support**: Little-endian format with optional 8-byte headers
- **Command Line Interface**: Easy to use in automation scripts
- **Comprehensive Error Handling**: Robust data validation and error reporting
- **Cross-Platform**: Works on Linux, Windows, and macOS

## Installation

### From PyPI (Recommended)
```bash
pip install minecraft-nbt-editor
```

### From Source
```bash
git clone https://github.com/geniusshiun/minecraft-nbt-editor.git
cd minecraft-nbt-editor
pip install -e .
```

## Quick Start

After installation, you can use the `minecraft-nbt` or `nbt-editor` command:

```bash
# View NBT file content
minecraft-nbt view level.dat

# Get a specific value
minecraft-nbt get level.dat --path "Data.Player.GameType"

# Set a value
minecraft-nbt set level.dat --path "Data.Player.GameType" --value "1"

# Add a new tag
minecraft-nbt add level.dat --path "Data.CustomTag" --value "Hello World" --type string

# Remove a tag
minecraft-nbt remove level.dat --path "Data.CustomTag"
```

## Usage Examples

### Basic Commands

```bash
# View file info (shows format, compression, endianness)
minecraft-nbt info level.dat

# View NBT file structure with limited depth
minecraft-nbt view level.dat --max-depth 3

# View as JSON format
minecraft-nbt view level.dat --format json

# View as table format
minecraft-nbt view level.dat --format table

# Get specific value
minecraft-nbt get level.dat --path "GameType"

# Set specific value
minecraft-nbt set level.dat --path "GameType" --value 1

# Enable features (Bedrock specific)
minecraft-nbt enable level.dat --exp --backup
```

### Common Minecraft Operations

#### Game Settings
```bash
# Get current game type (0=Survival, 1=Creative, 2=Adventure, 3=Spectator)
minecraft-nbt get level.dat --path GameType

# Change to Creative mode
minecraft-nbt set level.dat --path GameType --value 1

# Get current difficulty (0=Peaceful, 1=Easy, 2=Normal, 3=Hard)
minecraft-nbt get level.dat --path Difficulty

# Set difficulty to Hard
minecraft-nbt set level.dat --path Difficulty --value 3

# Get world name
minecraft-nbt get level.dat --path LevelName

# Change world name
minecraft-nbt set level.dat --path LevelName --value "My Awesome World"
```

#### Player Spawn Location
```bash
# Get spawn coordinates
minecraft-nbt get level.dat --path SpawnX
minecraft-nbt get level.dat --path SpawnY
minecraft-nbt get level.dat --path SpawnZ

# Set new spawn location
minecraft-nbt set level.dat --path SpawnX --value 100
minecraft-nbt set level.dat --path SpawnY --value 64
minecraft-nbt set level.dat --path SpawnZ --value 200
```

#### Game Rules and Features
```bash
# Check if cheats are enabled
minecraft-nbt get level.dat --path cheatsEnabled

# Enable cheats
minecraft-nbt set level.dat --path cheatsEnabled --value 1

# Get keep inventory setting
minecraft-nbt get level.dat --path keepinventory

# Enable keep inventory
minecraft-nbt set level.dat --path keepinventory --value 1

# Check daylight cycle
minecraft-nbt get level.dat --path daylightCycle

# Stop daylight cycle
minecraft-nbt set level.dat --path daylightCycle --value 0
```

#### Bedrock Edition Specific
```bash
# Get experimental features
minecraft-nbt get level.dat --path experiments

# Enable all experimental features at once (with backup)
minecraft-nbt enable level.dat --exp --backup

# Enable all experimental features without backup
minecraft-nbt enable level.dat --exp

# Get player abilities
minecraft-nbt get level.dat --path abilities.flying
minecraft-nbt get level.dat --path abilities.mayfly

# Enable flight for player
minecraft-nbt set level.dat --path abilities.mayfly --value 1
minecraft-nbt set level.dat --path abilities.flying --value 1

# Get world version info
minecraft-nbt get level.dat --path MinimumCompatibleClientVersion
minecraft-nbt get level.dat --path lastOpenedWithVersion
```

### Enable Command (Bedrock Edition)

The `enable` command provides quick access to commonly needed Minecraft Bedrock features:

```bash
# Enable all experimental features at once
minecraft-nbt enable level.dat --exp --backup

# Available experimental features that will be enabled:
# - data_driven_biomes: Data-driven biomes
# - experimental_creator_cameras: Experimental creator cameras  
# - experiments_ever_used: Experiments usage tracking
# - gametest: GameTest framework
# - jigsaw_structures: Jigsaw structure support
# - saved_with_toggled_experiments: Experiment toggle tracking
# - upcoming_creator_features: Upcoming creator features
# - villager_trades_rebalance: Villager trade rebalancing
# - y_2025_drop_3: 2025 Q3 features
```

### Advanced Search Operations

```bash
# Search for specific values
minecraft-nbt search level.dat --value "survival"

# Search by tag type
minecraft-nbt search level.dat --type string

# Search by tag name pattern
minecraft-nbt search level.dat --name "GameType"

# Search in specific path
minecraft-nbt search level.dat --path abilities --type byte
```

### Batch Operations

```bash
# Convert NBT to JSON for external processing
minecraft-nbt convert level.dat --output level.json --format json

# Create backup before editing
cp level.dat level.dat.backup

# Batch modify multiple settings
minecraft-nbt set level.dat --path GameType --value 1
minecraft-nbt set level.dat --path cheatsEnabled --value 1
minecraft-nbt set level.dat --path keepinventory --value 1
```

## Development

### Setup Development Environment
```bash
git clone https://github.com/geniusshiun/minecraft-nbt-editor.git
cd minecraft-nbt-editor
pip install -r requirements-dev.txt
pip install -e .
```

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest test_basic.py
```

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Project Structure

```
src/
├── core/
│   ├── __init__.py
│   ├── nbt_types.py      # NBT tag type definitions
│   ├── nbt_path.py       # NBT path operations
│   ├── nbt_file.py       # NBT file I/O
│   └── operations.py     # Editing operations
├── cli/
│   ├── __init__.py
│   └── main.py           # Command line interface
└── utils/
    ├── __init__.py
    └── binary.py         # Binary operations
```

## Supported File Types

- **Java Edition**: Big-endian NBT files (typically gzipped)
- **Bedrock Edition**: Little-endian NBT files with optional 8-byte headers
- **Compression**: Gzip, Zlib, or uncompressed
- **Formats**: .dat, .nbt, .mca, .mcstructure

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original VSCode plugin reference project
- Minecraft community for NBT format documentation
- Python community for excellent libraries and tools

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.
