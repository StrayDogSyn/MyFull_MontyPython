# TabletopInventory 🎲🧙‍♂️

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Version](https://img.shields.io/badge/version-1.2.0-orange)

A professional tabletop RPG character and inventory management system with an intuitive modern interface built with PyQt6. This project demonstrates advanced Python programming techniques and modern software development practices.

<div align="center">
  <img src="assets/screenshots/Screenshot%20(178).png" alt="TabletopInventory Screenshot" width="800"/>
</div>

## 🌟 Features

- **Comprehensive Character Management**:
  - Create, edit, and save multiple character profiles
  - Track detailed character information
  - Import/export character data in JSON format
  
- **Advanced Inventory System**:
  - Track items with categorization and rarity
  - Sort, filter, and search inventory items
  - Calculate total weight and value automatically
  
- **Rich Currency Management**:
  - Handle multiple currency denominations (platinum, gold, silver, copper)
  - Currency conversion calculations
  
- **Interactive Notes System**:
  - Rich text formatting with markdown support
  - Pre-built templates for character bios, quest logs, and NPC notes
  
- **Modern GUI**:
  - Dark mode interface with professional styling
  - Responsive layout with dockable panels
  - Custom icons and visual indicators for item rarity

## 💻 Technical Highlights

- **Object-Oriented Architecture**:
  - Proper use of classes, inheritance, and encapsulation
  - Implementation of design patterns for maintainable code
  
- **Modern Python Features**:
  - Type hints and annotations
  - Dataclasses for clean data models
  - Enum classes for type safety

- **PyQt6 Implementation**:
  - Custom-styled UI components
  - Signal/slot architecture for event handling
  - Responsive layouts that adapt to window size

- **Data Persistence**:
  - JSON serialization/deserialization
  - Proper error handling for file operations
  - Automatic save/backup functionality

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- PyQt6

### Setup

1. Clone the repository:
```powershell
git clone https://github.com/StrayDogSyn/MyFull_MontyPython.git
cd MyFull_MontyPython
```

2. Install dependencies:
```powershell
pip install -r requirements.txt  # If you have a requirements file
# or
pip install PyQt6
```

## 📋 Usage

### GUI Version
Run the application with:

```powershell
python tabletop_inventory.py
```

### Text-Based Version
For terminal-based usage (lightweight alternative):

```powershell
python tabletop_text.py
```

### Sample Data
The project includes a sample character file to demonstrate functionality:
- `pasa_phist.json` - A pre-configured character for demonstration

## 🧪 Testing

Run the test suite with:

```powershell
python tabletop_inv_test.py
```

## 🛠️ Development Tools

- **Code Quality**:
  - Type checking with mypy
  - Code formatting with black
  - Linting with flake8
  
- **Version Control**:
  - Git for source code management
  - Feature branch workflow
  
- **Documentation**:
  - Comprehensive docstrings
  - Markdown documentation
  - Automatic documentation generation

## 🔄 Project Structure

```
MyFull_MontyPython/
├── tabletop_inventory.py  # Main GUI application
├── tabletop_text.py       # Terminal-based alternative
├── tabletop_inv_test.py   # Test suite
├── check_qstyle.py        # Utility for PyQt6 style references
├── fix_qstyle_refs.py     # Utility for fixing PyQt6 style references
├── update_qstyle_refs.py  # Utility for updating PyQt6 style references
├── pasa_phist.json        # Sample character data
├── tabletop_log.txt       # Application log
├── LICENSE                # MIT License
├── pyproject.toml         # Project configuration
└── README.md              # Project documentation
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created by StrayDog Syndications LLC - [GitHub](https://github.com/StrayDogSyn)

---

*This project demonstrates my progression as a Python developer, showcasing skills in object-oriented design, GUI development, data management, and modern Python practices.*
