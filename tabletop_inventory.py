#!/usr/bin/env python3
"""
The Full Monty(Python) - A Character Inventory Management System

This application provides a GUI interface for managing character inventories
for tabletop role-playing games. Users can create characters, add/remove items,
track currency, and save/load character data.

Author: StrayDog Syndications LLC
Date: May 8, 2025

Version: 1.2.0
"""

import json
import os
import sys
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Optional, Union
from enum import Enum, auto

# Modern GUI with PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, 
    QComboBox, QSpinBox, QDoubleSpinBox, QTabWidget, QFileDialog,
    QMessageBox, QInputDialog, QScrollArea, QGroupBox, QFormLayout,
    QTextEdit, QHeaderView, QSplitter, QFrame, QToolBar, QStatusBar,
    QStyle, QStyleFactory, QMenu, QDialog, QGridLayout, QProgressBar,
    QSplashScreen, QCheckBox, QRadioButton
)
from PyQt6.QtGui import (
    QIcon, QFont, QAction, QColor, QPalette, QPixmap, 
    QTextCursor, QShortcut, QKeySequence, QFontDatabase
)
from PyQt6.QtCore import Qt, QSize, QTimer, QSortFilterProxyModel, QRect, QPropertyAnimation, QEasingCurve

# Global stylesheet for the application
GLOBAL_STYLESHEET = """
QMainWindow {
    background-color: #272727;
}

QWidget {
    color: #E0E0E0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
}

QTabWidget::pane {
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 2px;
}

QTabBar::tab {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 8ex;
    padding: 8px 12px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background-color: #4A4A4A;
}

QTabBar::tab:selected {
    border-bottom: 2px solid #6A9DDF;
}

QPushButton {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px 15px;
}

QPushButton:hover {
    background-color: #4A4A4A;
    border: 1px solid #6A9DDF;
}

QPushButton:pressed {
    background-color: #2A2A2A;
}

QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #2A2A2A;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px;
    selection-background-color: #6A9DDF;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #6A9DDF;
}

QTableWidget {
    gridline-color: #3A3A3A;
    background-color: #222222;
    selection-background-color: #3A6EA5;
    border: 1px solid #3A3A3A;
    border-radius: 4px;
}

QHeaderView::section {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    padding: 5px;
    font-weight: bold;
}

QToolBar {
    background-color: #2A2A2A;
    border: none;
    spacing: 3px;
    padding: 3px;
}

QToolButton {
    background-color: #2A2A2A;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 5px;
}

QToolButton:hover {
    background-color: #3A3A3A;
    border: 1px solid #555555;
}

QToolButton:pressed {
    background-color: #1A1A1A;
}

QGroupBox {
    background-color: #2A2A2A;
    border: 1px solid #555555;
    border-radius: 5px;
    margin-top: 15px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 10px;
    color: #E0E0E0;
}

QStatusBar {
    background-color: #1A1A1A;
    color: #E0E0E0;
}

QStatusBar QLabel {
    padding: 0 8px;
}

QScrollBar:vertical {
    border: none;
    background-color: #2A2A2A;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #5A5A5A;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6A9DDF;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #2A2A2A;
    height: 10px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #5A5A5A;
    border-radius: 4px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #6A9DDF;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMenu {
    background-color: #2A2A2A;
    border: 1px solid #555555;
    padding: 5px;
}

QMenu::item {
    padding: 5px 30px 5px 30px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #3A6EA5;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
    border: 1px solid #555555;
    background-color: #2A2A2A;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    border: 1px solid #6A9DDF;
    background-color: #3A6EA5;
}

QSplitter::handle {
    background-color: #555555;
}

QSplitter::handle:horizontal {
    width: 1px;
}

QSplitter::handle:vertical {
    height: 1px;
}

QProgressBar {
    border: 1px solid #555555;
    border-radius: 4px;
    background-color: #2A2A2A;
    text-align: center;
    color: #E0E0E0;
}

QProgressBar::chunk {
    background-color: #3A6EA5;
    width: 10px;
    margin: 0.5px;
}
"""

class ItemRarity(Enum):
    """Enum representing item rarity levels"""
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    VERY_RARE = auto()
    LEGENDARY = auto()
    ARTIFACT = auto()


@dataclass
class Item:
    """Represents an inventory item"""
    id: str  # UUID for the item
    name: str
    description: str = ""
    quantity: int = 1
    weight: float = 0.0  # Weight in pounds/kg (depending on game system)
    value: float = 0.0   # Value in game currency
    rarity: ItemRarity = ItemRarity.COMMON
    equipped: bool = False
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure id is a string UUID"""
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Currency:
    """Represents character currency with multiple denominations"""
    platinum: int = 0
    gold: int = 0
    silver: int = 0
    copper: int = 0
    
    def total_in_copper(self) -> int:
        """Convert all currency to copper value"""
        return self.copper + (self.silver * 10) + (self.gold * 100) + (self.platinum * 1000)


@dataclass
class Character:
    """Represents a character and their inventory"""
    id: str  # UUID for the character
    name: str
    game_system: str = "Generic"
    level: int = 1
    inventory: List[Item] = field(default_factory=list)
    currency: Currency = field(default_factory=Currency)
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        """Ensure id is a string UUID"""
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def add_item(self, item: Item) -> None:
        """Add an item to the inventory"""
        self.inventory.append(item)
        self.updated_at = datetime.now().isoformat()
    
    def remove_item(self, item_id: str) -> Optional[Item]:
        """Remove an item from inventory by ID"""
        for i, item in enumerate(self.inventory):
            if item.id == item_id:
                self.updated_at = datetime.now().isoformat()
                return self.inventory.pop(i)
        return None
    
    def total_weight(self) -> float:
        """Calculate total weight of all inventory items"""
        return sum(item.quantity * item.weight for item in self.inventory)
    
    def total_value(self) -> float:
        """Calculate total value of all inventory items"""
        return sum(item.quantity * item.value for item in self.inventory)


class CharacterManager:
    """Manages character data and persistence"""
    
    def __init__(self, save_dir: str = None):
        """Initialize the character manager"""
        self.characters: Dict[str, Character] = {}
        self.save_dir = save_dir or os.path.join(os.path.expanduser("~"), "tabletop_inventory")
        
        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)
    
    def create_character(self, name: str, game_system: str = "Generic") -> Character:
        """Create a new character"""
        character = Character(id=str(uuid.uuid4()), name=name, game_system=game_system)
        self.characters[character.id] = character
        return character
    
    def delete_character(self, character_id: str) -> bool:
        """Delete a character by ID"""
        if character_id in self.characters:
            del self.characters[character_id]
            
            # Remove saved file if it exists
            save_path = os.path.join(self.save_dir, f"{character_id}.json")
            if os.path.exists(save_path):
                os.remove(save_path)
            
            return True
        return False
    
    def save_character(self, character_id: str) -> bool:
        """Save a character to file"""
        if character_id not in self.characters:
            return False
        
        character = self.characters[character_id]
        save_path = os.path.join(self.save_dir, f"{character_id}.json")
        
        try:
            # Convert character to dictionary
            character_dict = asdict(character)
            
            # Convert enum values to strings
            for item in character_dict["inventory"]:
                if isinstance(item["rarity"], ItemRarity):
                    item["rarity"] = item["rarity"].name
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(character_dict, f, indent=2)
            return True
        
        except Exception as e:
            print(f"Error saving character: {e}")
            return False
    
    def load_character(self, file_path: str) -> Optional[Character]:
        """Load a character from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                character_dict = json.load(f)
            
            # Convert string rarity back to enum
            for item in character_dict["inventory"]:
                if isinstance(item["rarity"], str):
                    item["rarity"] = ItemRarity[item["rarity"]]
            
            # Create character object
            character = Character(
                id=character_dict["id"],
                name=character_dict["name"],
                game_system=character_dict["game_system"],
                level=character_dict["level"],
                notes=character_dict["notes"],
                created_at=character_dict["created_at"],
                updated_at=character_dict["updated_at"]
            )
            
            # Add inventory items
            for item_dict in character_dict["inventory"]:
                item = Item(
                    id=item_dict["id"],
                    name=item_dict["name"],
                    description=item_dict["description"],
                    quantity=item_dict["quantity"],
                    weight=item_dict["weight"],
                    value=item_dict["value"],
                    rarity=item_dict["rarity"],
                    equipped=item_dict["equipped"],
                    tags=item_dict["tags"]
                )
                character.inventory.append(item)
            
            # Add currency
            currency_dict = character_dict["currency"]
            character.currency = Currency(
                platinum=currency_dict["platinum"],
                gold=currency_dict["gold"],
                silver=currency_dict["silver"],
                copper=currency_dict["copper"]
            )
            
            # Add character to dictionary
            self.characters[character.id] = character
            
            return character
        
        except Exception as e:
            print(f"Error loading character: {e}")
            return None
    
    def load_all_characters(self) -> List[Character]:
        """Load all characters from save directory"""
        characters = []
        
        for file_name in os.listdir(self.save_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.save_dir, file_name)
                character = self.load_character(file_path)
                if character:
                    characters.append(character)
        
        return characters


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        self.character_manager = CharacterManager()
        self.current_character = None
        
        self.init_ui()
        self.load_characters()
    
    def create_dark_palette(self):
        """Create a dark color palette for the application"""
        dark_palette = QPalette()
        
        # Set colors for the dark theme
        dark_color = QColor(45, 45, 45)
        dark_palette.setColor(QPalette.ColorRole.Window, dark_color)
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(55, 55, 55))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, dark_color)
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        return dark_palette
    
    def create_toolbar(self):
        """Create the main toolbar with common actions"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        
        # Add character action
        new_char_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "New Character", self)
        new_char_action.setToolTip("Create a new character")
        new_char_action.triggered.connect(self.create_new_character)
        toolbar.addAction(new_char_action)
        
        # Open character action
        open_char_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton), "Open", self)
        open_char_action.setToolTip("Open a character file")
        open_char_action.triggered.connect(self.open_character)
        toolbar.addAction(open_char_action)
        
        # Save character action
        save_char_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "Save", self)
        save_char_action.setToolTip("Save the current character")
        save_char_action.triggered.connect(self.save_character)
        toolbar.addAction(save_char_action)
        
        toolbar.addSeparator()
        
        # Add item action
        add_item_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton), "Add Item", self)
        add_item_action.setToolTip("Add a new item to inventory")
        add_item_action.triggered.connect(lambda: self.tabs.setCurrentIndex(1))
        toolbar.addAction(add_item_action)
        
        # Refresh action
        refresh_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload), "Refresh", self)
        refresh_action.setToolTip("Refresh the current view")
        refresh_action.triggered.connect(self.update_ui)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # Help action
        help_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton), "Help", self)
        help_action.setToolTip("Show help")
        help_action.triggered.connect(self.show_about)
        toolbar.addAction(help_action)
        
        # Add the toolbar to the main window
        self.addToolBar(toolbar)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Set application style for a more professional look
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        
        # Apply global stylesheet
        QApplication.setStyleSheet(GLOBAL_STYLESHEET)
        
        self.setWindowTitle("TabletopInventory - Character Management System")
        self.setMinimumSize(1024, 768)
        
        # Set application icon
        # Note: In a real application, you would use an actual icon file
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        
        # Create central widget with splitter for resizable sections
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(10)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create tabs with custom styling
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        main_layout.addWidget(self.tabs)
        
        # Character tab
        self.character_tab = QWidget()
        self.tabs.addTab(self.character_tab, self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton), "Character")
        
        character_layout = QVBoxLayout(self.character_tab)
        character_layout.setContentsMargins(10, 10, 10, 10)
        character_layout.setSpacing(10)
        
        # Character selection with styled elements
        char_select_frame = QFrame()
        char_select_frame.setFrameShape(QFrame.Shape.StyledPanel)
        char_select_frame.setStyleSheet("background-color: rgba(60, 60, 60, 120); border-radius: 5px;")
        character_layout.addWidget(char_select_frame)
        
        char_select_layout = QHBoxLayout(char_select_frame)
        char_select_layout.setContentsMargins(10, 10, 10, 10)
        
        char_label = QLabel("Character:")
        char_label.setStyleSheet("font-weight: bold; color: #cccccc;")
        self.character_combo = QComboBox()
        self.character_combo.setMinimumWidth(250)
        self.character_combo.setStyleSheet("padding: 5px;")
        self.character_combo.currentIndexChanged.connect(self.on_character_selected)
        char_select_layout.addWidget(char_label)
        char_select_layout.addWidget(self.character_combo, stretch=1)
        
        # Character buttons with icons
        self.new_char_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), " New")
        self.new_char_btn.setToolTip("Create a new character (Ctrl+N)")
        self.new_char_btn.clicked.connect(self.create_new_character)
        
        self.delete_char_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon), " Delete")
        self.delete_char_btn.setToolTip("Delete the current character (Ctrl+D)")
        self.delete_char_btn.clicked.connect(self.delete_character)
        
        self.save_char_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), " Save")
        self.save_char_btn.setToolTip("Save the current character (Ctrl+S)")
        self.save_char_btn.clicked.connect(self.save_character)
        
        # Add button shortcuts
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.create_new_character)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.delete_character)
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.save_character)
        
        char_select_layout.addWidget(self.new_char_btn)
        char_select_layout.addWidget(self.delete_char_btn)
        char_select_layout.addWidget(self.save_char_btn)
        
        # Create a horizontal splitter for character details and currency
        char_details_splitter = QSplitter(Qt.Orientation.Horizontal)
        character_layout.addWidget(char_details_splitter, 1)
        
        # Character details
        char_details_group = QGroupBox("Character Details")
        char_details_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #555555; border-radius: 5px; margin-top: 10px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        char_details_splitter.addWidget(char_details_group)
        
        details_layout = QFormLayout(char_details_group)
        details_layout.setContentsMargins(15, 20, 15, 15)
        details_layout.setSpacing(10)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter character name")
        self.name_edit.setStyleSheet("padding: 5px; border-radius: 3px;")
        
        self.game_system_edit = QLineEdit()
        self.game_system_edit.setPlaceholderText("E.g. D&D 5e, Pathfinder, etc.")
        self.game_system_edit.setStyleSheet("padding: 5px; border-radius: 3px;")
        
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 99)
        self.level_spin.setStyleSheet("padding: 5px;")
        self.level_spin.setSuffix(" level")
        
        details_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        details_layout.addRow(QLabel("<b>Name:</b>"), self.name_edit)
        details_layout.addRow(QLabel("<b>Game System:</b>"), self.game_system_edit)
        details_layout.addRow(QLabel("<b>Level:</b>"), self.level_spin)
        
        # Add character portrait placeholder (in a real app, you would implement image loading)
        portrait_layout = QVBoxLayout()
        portrait_label = QLabel("Character Portrait")
        portrait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        portrait_frame = QFrame()
        portrait_frame.setFrameShape(QFrame.Shape.StyledPanel)
        portrait_frame.setMinimumSize(150, 150)
        portrait_frame.setMaximumSize(150, 150)
        portrait_frame.setStyleSheet("background-color: #333333; border: 1px solid #555555;")
        portrait_layout.addWidget(portrait_label)
        portrait_layout.addWidget(portrait_frame)
        portrait_layout.addStretch()
        details_layout.addRow("", portrait_layout)
        
        # Currency group with styled spinboxes
        currency_group = QGroupBox("Currency")
        currency_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #555555; border-radius: 5px; margin-top: 10px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        char_details_splitter.addWidget(currency_group)
        
        currency_layout = QGridLayout(currency_group)
        currency_layout.setContentsMargins(15, 20, 15, 15)
        currency_layout.setSpacing(10)
        
        # Currency spinboxes with custom styling
        self.platinum_spin = QSpinBox()
        self.platinum_spin.setRange(0, 999999)
        self.platinum_spin.setStyleSheet("padding: 5px; background: rgba(220, 220, 255, 30);")
        self.platinum_spin.setPrefix("🟪 ")
        
        self.gold_spin = QSpinBox()
        self.gold_spin.setRange(0, 999999)
        self.gold_spin.setStyleSheet("padding: 5px; background: rgba(255, 255, 0, 30);")
        self.gold_spin.setPrefix("🟨 ")
        
        self.silver_spin = QSpinBox()
        self.silver_spin.setRange(0, 999999)
        self.silver_spin.setStyleSheet("padding: 5px; background: rgba(200, 200, 200, 30);")
        self.silver_spin.setPrefix("⬜ ")
        
        self.copper_spin = QSpinBox()
        self.copper_spin.setRange(0, 999999)
        self.copper_spin.setStyleSheet("padding: 5px; background: rgba(180, 100, 0, 30);")
        self.copper_spin.setPrefix("🟧 ")
        
        currency_layout.addWidget(QLabel("<b>Platinum:</b>"), 0, 0)
        currency_layout.addWidget(self.platinum_spin, 0, 1)
        currency_layout.addWidget(QLabel("<b>Gold:</b>"), 1, 0)
        currency_layout.addWidget(self.gold_spin, 1, 1)
        currency_layout.addWidget(QLabel("<b>Silver:</b>"), 2, 0)
        currency_layout.addWidget(self.silver_spin, 2, 1)
        currency_layout.addWidget(QLabel("<b>Copper:</b>"), 3, 0)
        currency_layout.addWidget(self.copper_spin, 3, 1)
        
        # Add total currency value display
        self.total_currency_label = QLabel("Total (in copper): 0")
        self.total_currency_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: rgba(60, 60, 60, 120); border-radius: 3px;")
        currency_layout.addWidget(self.total_currency_label, 4, 0, 1, 2)
        
        # Add a converter between currency types
        converter_layout = QHBoxLayout()
        self.convert_from_combo = QComboBox()
        self.convert_from_combo.addItems(["Copper", "Silver", "Gold", "Platinum"])
        self.convert_to_combo = QComboBox()
        self.convert_to_combo.addItems(["Copper", "Silver", "Gold", "Platinum"])
        self.convert_amount_spin = QSpinBox()
        self.convert_amount_spin.setRange(1, 9999)
        self.convert_amount_spin.setValue(1)
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_currency)
        
        converter_layout.addWidget(self.convert_amount_spin)
        converter_layout.addWidget(self.convert_from_combo)
        converter_layout.addWidget(QLabel("to"))
        converter_layout.addWidget(self.convert_to_combo)
        converter_layout.addWidget(self.convert_button)
        
        currency_layout.addLayout(converter_layout, 5, 0, 1, 2)
        
        # Inventory tab with enhanced styling
        self.inventory_tab = QWidget()
        self.tabs.addTab(self.inventory_tab, self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView), "Inventory")
        
        inventory_layout = QVBoxLayout(self.inventory_tab)
        inventory_layout.setContentsMargins(10, 10, 10, 10)
        inventory_layout.setSpacing(10)
        
        # Add item section with grid layout
        add_item_group = QGroupBox("Add New Item")
        add_item_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #555555; border-radius: 5px; margin-top: 10px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        inventory_layout.addWidget(add_item_group)
        
        add_item_layout = QGridLayout(add_item_group)
        add_item_layout.setContentsMargins(15, 20, 15, 15)
        add_item_layout.setSpacing(10)
        
        self.item_name_edit = QLineEdit()
        self.item_name_edit.setPlaceholderText("Item name")
        self.item_name_edit.setStyleSheet("padding: 5px; border-radius: 3px;")
        
        self.item_desc_edit = QLineEdit()
        self.item_desc_edit.setPlaceholderText("Short description")
        self.item_desc_edit.setStyleSheet("padding: 5px; border-radius: 3px;")
        
        self.item_quantity_spin = QSpinBox()
        self.item_quantity_spin.setRange(1, 9999)
        self.item_quantity_spin.setStyleSheet("padding: 5px;")
        
        self.item_weight_spin = QDoubleSpinBox()
        self.item_weight_spin.setRange(0, 9999.99)
        self.item_weight_spin.setSingleStep(0.1)
        self.item_weight_spin.setSuffix(" lb")
        self.item_weight_spin.setStyleSheet("padding: 5px;")
        
        self.item_value_spin = QDoubleSpinBox()
        self.item_value_spin.setRange(0, 9999.99)
        self.item_value_spin.setSingleStep(0.1)
        self.item_value_spin.setSuffix(" gp")
        self.item_value_spin.setStyleSheet("padding: 5px;")
        
        self.item_rarity_combo = QComboBox()
        self.item_rarity_combo.setStyleSheet("padding: 5px;")
        
        # Add color indicators for item rarity
        rarity_colors = {
            "COMMON": "#aaaaaa",
            "UNCOMMON": "#1eff00", 
            "RARE": "#0070dd", 
            "VERY_RARE": "#a335ee", 
            "LEGENDARY": "#ff8000",
            "ARTIFACT": "#e6cc80"
        }
        
        for rarity in ItemRarity:
            self.item_rarity_combo.addItem(rarity.name.capitalize())
            self.item_rarity_combo.setItemData(
                self.item_rarity_combo.count() - 1, 
                QColor(rarity_colors.get(rarity.name, "#aaaaaa")), 
                Qt.ItemDataRole.ForegroundRole
            )
        
        # Equipped checkbox
        self.item_equipped_check = QComboBox()
        self.item_equipped_check.addItems(["Not Equipped", "Equipped"])
        self.item_equipped_check.setStyleSheet("padding: 5px;")
        
        # Tags field
        self.item_tags_edit = QLineEdit()
        self.item_tags_edit.setPlaceholderText("Tags (comma separated)")
        self.item_tags_edit.setStyleSheet("padding: 5px; border-radius: 3px;")
        
        add_item_layout.addWidget(QLabel("<b>Name:</b>"), 0, 0)
        add_item_layout.addWidget(self.item_name_edit, 0, 1, 1, 3)
        add_item_layout.addWidget(QLabel("<b>Description:</b>"), 1, 0)
        add_item_layout.addWidget(self.item_desc_edit, 1, 1, 1, 3)
        add_item_layout.addWidget(QLabel("<b>Quantity:</b>"), 2, 0)
        add_item_layout.addWidget(self.item_quantity_spin, 2, 1)
        add_item_layout.addWidget(QLabel("<b>Weight:</b>"), 2, 2)
        add_item_layout.addWidget(self.item_weight_spin, 2, 3)
        add_item_layout.addWidget(QLabel("<b>Value:</b>"), 3, 0)
        add_item_layout.addWidget(self.item_value_spin, 3, 1)
        add_item_layout.addWidget(QLabel("<b>Rarity:</b>"), 3, 2)
        add_item_layout.addWidget(self.item_rarity_combo, 3, 3)
        add_item_layout.addWidget(QLabel("<b>Status:</b>"), 4, 0)
        add_item_layout.addWidget(self.item_equipped_check, 4, 1)
        add_item_layout.addWidget(QLabel("<b>Tags:</b>"), 4, 2)
        add_item_layout.addWidget(self.item_tags_edit, 4, 3)
        
        # Item buttons layout
        item_buttons_layout = QHBoxLayout()
        add_item_layout.addLayout(item_buttons_layout, 5, 0, 1, 4)
        
        # Add item button with icon
        add_item_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton), " Add Item")
        add_item_btn.setStyleSheet("padding: 5px; font-weight: bold;")
        add_item_btn.clicked.connect(self.add_item)
        
        # Clear form button
        clear_form_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton), " Clear Form")
        clear_form_btn.clicked.connect(self.clear_item_form)
        
        item_buttons_layout.addStretch(1)
        item_buttons_layout.addWidget(clear_form_btn)
        item_buttons_layout.addWidget(add_item_btn)
        
        # Search and filter bar for inventory
        filter_layout = QHBoxLayout()
        inventory_layout.addLayout(filter_layout)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search items...")
        self.search_edit.setStyleSheet("padding: 5px; border-radius: 3px;")
        self.search_edit.textChanged.connect(self.filter_inventory)
        
        self.filter_rarity_combo = QComboBox()
        self.filter_rarity_combo.addItem("All Rarities")
        for rarity in ItemRarity:
            self.filter_rarity_combo.addItem(rarity.name.capitalize())
        self.filter_rarity_combo.currentIndexChanged.connect(self.filter_inventory)
        
        self.sort_by_combo = QComboBox()
        self.sort_by_combo.addItems(["Name", "Quantity", "Weight", "Value", "Rarity"])
        self.sort_by_combo.currentIndexChanged.connect(self.filter_inventory)
        
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_edit, stretch=3)
        filter_layout.addWidget(QLabel("Rarity:"))
        filter_layout.addWidget(self.filter_rarity_combo, stretch=1)
        filter_layout.addWidget(QLabel("Sort by:"))
        filter_layout.addWidget(self.sort_by_combo, stretch=1)
        
        # Enhanced inventory table
        self.inventory_table = QTableWidget(0, 7)
        self.inventory_table.setHorizontalHeaderLabels(["Name", "Quantity", "Weight", "Value", "Rarity", "Description", "Actions"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.inventory_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.inventory_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setStyleSheet("QTableWidget { gridline-color: #444444; alternate-background-color: #383838; }")
        inventory_layout.addWidget(self.inventory_table, stretch=1)
        
        # Inventory summary with enhanced styling
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        summary_frame.setStyleSheet("background-color: rgba(60, 60, 60, 120); border-radius: 5px; padding: 5px;")
        inventory_layout.addWidget(summary_frame)
        
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(10, 10, 10, 10)
        
        self.total_items_label = QLabel("Total Items: 0")
        self.total_items_label.setStyleSheet("font-weight: bold;")
        self.total_weight_label = QLabel("Total Weight: 0.0 lb")
        self.total_weight_label.setStyleSheet("font-weight: bold;")
        self.total_value_label = QLabel("Total Value: 0.0 gp")
        self.total_value_label.setStyleSheet("font-weight: bold;")
        
        summary_layout.addWidget(self.total_items_label)
        summary_layout.addStretch(1)
        summary_layout.addWidget(self.total_weight_label)
        summary_layout.addStretch(1)
        summary_layout.addWidget(self.total_value_label)
          # Notes tab with enhanced text editor
        self.notes_tab = QWidget()
        self.tabs.addTab(self.notes_tab, self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView), "Notes")
        
        notes_layout = QVBoxLayout(self.notes_tab)
        notes_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create a splitter for notes section
        notes_splitter = QSplitter(Qt.Orientation.Vertical)
        notes_layout.addWidget(notes_splitter)
        
        # Top section with editor
        notes_edit_container = QWidget()
        notes_edit_layout = QVBoxLayout(notes_edit_container)
        notes_edit_layout.setContentsMargins(0, 0, 0, 0)
        notes_edit_layout.setSpacing(5)
        
        # Enhanced text editor
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Enter character notes here...")
        self.notes_edit.setStyleSheet("padding: 8px; border-radius: 3px; line-height: 1.3;")
        font = QFont("Segoe UI", 10)
        self.notes_edit.setFont(font)
        
        # Add comprehensive formatting toolbar for notes
        notes_toolbar = QToolBar("Notes Toolbar")
        notes_toolbar.setIconSize(QSize(16, 16))
        notes_toolbar.setStyleSheet("QToolBar { spacing: 2px; background-color: #333333; border-radius: 3px; }")
        
        # Text style section
        bold_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton), "Bold", self)
        bold_action.setShortcut(QKeySequence.StandardKey.Bold)
        bold_action.setToolTip("Bold Text (Ctrl+B)")
        bold_action.triggered.connect(lambda: self.notes_edit.insertPlainText("**Bold Text**"))
        
        italic_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarShadeButton), "Italic", self)
        italic_action.setShortcut(QKeySequence.StandardKey.Italic)
        italic_action.setToolTip("Italic Text (Ctrl+I)")
        italic_action.triggered.connect(lambda: self.notes_edit.insertPlainText("*Italic Text*"))
        
        underline_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUnderline), "Underline", self)
        underline_action.setToolTip("Underlined Text")
        underline_action.triggered.connect(lambda: self.notes_edit.insertPlainText("__Underlined Text__"))
        
        strikethrough_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_LineEditClearButton), "Strikethrough", self)
        strikethrough_action.setToolTip("Strikethrough Text")
        strikethrough_action.triggered.connect(lambda: self.notes_edit.insertPlainText("~~Strikethrough Text~~"))
        
        code_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "Code", self)
        code_action.setToolTip("Code Text")
        code_action.triggered.connect(lambda: self.notes_edit.insertPlainText("`Code Text`"))
        
        # Heading section
        heading1_action = QAction("H1", self)
        heading1_action.setToolTip("Heading 1")
        heading1_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n# Heading 1 #\n"))
        
        heading2_action = QAction("H2", self)
        heading2_action.setToolTip("Heading 2")
        heading2_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n## Heading 2 ##\n"))
        
        heading3_action = QAction("H3", self)
        heading3_action.setToolTip("Heading 3")
        heading3_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n### Heading 3 ###\n"))
        
        # List section
        bullet_list_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView), "Bullet List", self)
        bullet_list_action.setToolTip("Bullet List")
        bullet_list_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n- List item\n- Another item\n- Third item\n"))
        
        numbered_list_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView), "Numbered List", self)
        numbered_list_action.setToolTip("Numbered List")
        numbered_list_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n1. First item\n2. Second item\n3. Third item\n"))
        
        checklist_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton), "Checklist", self)
        checklist_action.setToolTip("Checklist")
        checklist_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n- [ ] Task to do\n- [x] Completed task\n- [ ] Another task\n"))
        
        # Dividers section
        separator_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_LineEditHBar), "Separator", self)
        separator_action.setToolTip("Horizontal Separator")
        separator_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n---\n"))
        
        # Blocks section
        quote_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation), "Quote", self)
        quote_action.setToolTip("Quote Block")
        quote_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n> This is a quote or important note\n> It can span multiple lines\n"))
        
        code_block_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView), "Code Block", self)
        code_block_action.setToolTip("Code Block")
        code_block_action.triggered.connect(lambda: self.notes_edit.insertPlainText("\n```\nCode block\nfor multi-line code\n```\n"))
        
        # Templates menu
        templates_menu = QMenu("Templates")
        templates_menu.setStyleSheet("QMenu { background-color: #333333; border: 1px solid #555555; }")
        
        character_template_action = QAction("Character Bio", self)
        character_template_action.triggered.connect(self.insert_character_template)
        templates_menu.addAction(character_template_action)
        
        quest_template_action = QAction("Quest Log", self)
        quest_template_action.triggered.connect(self.insert_quest_template)
        templates_menu.addAction(quest_template_action)
        
        inventory_template_action = QAction("Important Items", self)
        inventory_template_action.triggered.connect(self.insert_inventory_template)
        templates_menu.addAction(inventory_template_action)
        
        npc_template_action = QAction("NPC Notes", self)
        npc_template_action.triggered.connect(self.insert_npc_template)
        templates_menu.addAction(npc_template_action)
        
        templates_action = QAction("Templates", self)
        templates_action.setMenu(templates_menu)
        
        # Utility actions
        clear_notes_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton), "Clear", self)
        clear_notes_action.setToolTip("Clear Notes")
        clear_notes_action.triggered.connect(self.notes_edit.clear)
        
        # Add actions to toolbar
        notes_toolbar.addAction(bold_action)
        notes_toolbar.addAction(italic_action)
        notes_toolbar.addAction(underline_action)
        notes_toolbar.addAction(strikethrough_action)
        notes_toolbar.addAction(code_action)
        notes_toolbar.addSeparator()
        
        notes_toolbar.addAction(heading1_action)
        notes_toolbar.addAction(heading2_action)
        notes_toolbar.addAction(heading3_action)
        notes_toolbar.addSeparator()
        
        notes_toolbar.addAction(bullet_list_action)
        notes_toolbar.addAction(numbered_list_action)
        notes_toolbar.addAction(checklist_action)
        notes_toolbar.addSeparator()
        
        notes_toolbar.addAction(quote_action)
        notes_toolbar.addAction(separator_action)
        notes_toolbar.addAction(code_block_action)
        notes_toolbar.addSeparator()
        
        notes_toolbar.addAction(templates_action)
        notes_toolbar.addSeparator()
        
        notes_toolbar.addAction(clear_notes_action)
        
        # Add toolbar and editor to layout
        notes_edit_layout.addWidget(notes_toolbar)
        notes_edit_layout.addWidget(self.notes_edit)
        
        notes_splitter.addWidget(notes_edit_container)
        
        # Bottom section with preview (could be implemented with a markdown renderer)
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        preview_label = QLabel("Notes Preview")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_label.setStyleSheet("font-weight: bold; background-color: #333333; padding: 5px;")
        
        self.notes_preview = QTextEdit()
        self.notes_preview.setReadOnly(True)
        self.notes_preview.setStyleSheet("background-color: #2a2a2a; padding: 10px; border-radius: 3px;")
        
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.notes_preview)
        
        # Connect preview update
        self.notes_edit.textChanged.connect(self.update_notes_preview)
        
        notes_splitter.addWidget(preview_container)
        
        # Set the initial size ratio
        notes_splitter.setSizes([600, 400])
        
        # Set up menu bar with enhanced options
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("QMenuBar { background-color: #2d2d2d; } QMenuBar::item:selected { background-color: #3d3d3d; }")
        
        file_menu = menu_bar.addMenu("File")
        
        new_action = QAction("New Character", self)
        new_action.triggered.connect(self.create_new_character)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Character", self)
        open_action.triggered.connect(self.open_character)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Character", self)
        save_action.triggered.connect(self.save_character)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
          # Set up enhanced status bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("QStatusBar { border-top: 1px solid #555555; }")
        
        # Add permanent widgets to status bar
        self.last_saved_label = QLabel("No character loaded")
        self.last_saved_label.setStyleSheet("padding: 2px 10px; border-right: 1px solid #555555;")
        self.status_bar.addPermanentWidget(self.last_saved_label)
        
        self.item_count_label = QLabel("Items: 0")
        self.item_count_label.setStyleSheet("padding: 2px 10px; border-right: 1px solid #555555;")
        self.status_bar.addPermanentWidget(self.item_count_label)
        
        self.total_weight_status_label = QLabel("Weight: 0.0 lb")
        self.total_weight_status_label.setStyleSheet("padding: 2px 10px;")
        self.status_bar.addPermanentWidget(self.total_weight_status_label)
        
        self.status_bar.showMessage("Ready")
    
    def load_characters(self):
        """Load all characters from save directory"""
        self.character_combo.clear()
        characters = self.character_manager.load_all_characters()
        
        for character in characters:
            self.character_combo.addItem(character.name, character.id)
    
    def on_character_selected(self, index):
        """Handle character selection"""
        if index < 0:
            self.current_character = None
            self.update_ui()
            return
        
        character_id = self.character_combo.itemData(index)
        self.current_character = self.character_manager.characters.get(character_id)
        self.update_ui()
    def update_ui(self):
        """Update UI with current character data"""
        if not self.current_character:
            # Clear UI
            self.name_edit.setText("")
            self.game_system_edit.setText("")
            self.level_spin.setValue(1)
            self.platinum_spin.setValue(0)
            self.gold_spin.setValue(0)
            self.silver_spin.setValue(0)
            self.copper_spin.setValue(0)
            self.total_currency_label.setText("Total (in copper): 0")
            self.notes_edit.clear()
            self.inventory_table.setRowCount(0)
            self.total_items_label.setText("Total Items: 0")
            self.total_weight_label.setText("Total Weight: 0.0 lb")
            self.total_value_label.setText("Total Value: 0.0 gp")
            
            # Disable currency converter in absence of character
            self.convert_button.setEnabled(False)
            self.convert_amount_spin.setEnabled(False)
            self.convert_from_combo.setEnabled(False)
            self.convert_to_combo.setEnabled(False)
            
            # Update status bar
            self.last_saved_label.setText("No character loaded")
            return
        
        # Update character details
        self.name_edit.setText(self.current_character.name)
        self.game_system_edit.setText(self.current_character.game_system)
        self.level_spin.setValue(self.current_character.level)
        
        # Update currency
        self.platinum_spin.setValue(self.current_character.currency.platinum)
        self.gold_spin.setValue(self.current_character.currency.gold)
        self.silver_spin.setValue(self.current_character.currency.silver)
        self.copper_spin.setValue(self.current_character.currency.copper)
        
        # Update total currency
        total_copper = self.current_character.currency.total_in_copper()
        self.total_currency_label.setText(f"Total (in copper): {total_copper}")
        
        # Enable currency converter
        self.convert_button.setEnabled(True)
        self.convert_amount_spin.setEnabled(True)
        self.convert_from_combo.setEnabled(True)
        self.convert_to_combo.setEnabled(True)
        
        # Update notes - now using QTextEdit
        self.notes_edit.setPlainText(self.current_character.notes)
        
        # Update inventory table
        self.update_inventory_table()
        
        # Update status bar with last saved time
        self.update_status()
    
    def update_inventory_table(self):
        """Update inventory table with current character's items"""
        if not self.current_character:
            self.inventory_table.setRowCount(0)
            return
        
        # Rarity colors for better visual distinction
        rarity_colors = {
            ItemRarity.COMMON: "#aaaaaa",
            ItemRarity.UNCOMMON: "#1eff00", 
            ItemRarity.RARE: "#0070dd", 
            ItemRarity.VERY_RARE: "#a335ee", 
            ItemRarity.LEGENDARY: "#ff8000",
            ItemRarity.ARTIFACT: "#e6cc80"
        }
        
        # Background colors (more subtle)
        rarity_bg_colors = {
            ItemRarity.COMMON: "rgba(170, 170, 170, 20)",
            ItemRarity.UNCOMMON: "rgba(30, 255, 0, 20)", 
            ItemRarity.RARE: "rgba(0, 112, 221, 20)", 
            ItemRarity.VERY_RARE: "rgba(163, 53, 238, 20)", 
            ItemRarity.LEGENDARY: "rgba(255, 128, 0, 20)",
            ItemRarity.ARTIFACT: "rgba(230, 204, 128, 20)"
        }
        
        # Disconnect signals to prevent recursion
        self.inventory_table.blockSignals(True)
        
        # Clear table
        self.inventory_table.setRowCount(0)
        
        # Add items
        for i, item in enumerate(self.current_character.inventory):
            self.inventory_table.insertRow(i)
            
            # Item name
            name_item = QTableWidgetItem(item.name)
            name_item.setForeground(QColor(rarity_colors.get(item.rarity, "#ffffff")))
            
            # Apply some styling to the entire row based on rarity
            for col in range(6):
                cell_item = QTableWidgetItem("")
                if col == 0:
                    cell_item = name_item
                elif col == 1:
                    cell_item = QTableWidgetItem(str(item.quantity))
                elif col == 2:
                    cell_item = QTableWidgetItem(f"{item.weight:.1f}")
                elif col == 3:
                    cell_item = QTableWidgetItem(f"{item.value:.1f}")
                elif col == 4:
                    cell_item = QTableWidgetItem(item.rarity.name.capitalize())
                    cell_item.setForeground(QColor(rarity_colors.get(item.rarity, "#ffffff")))
                elif col == 5:
                    cell_item = QTableWidgetItem(item.description)
                
                # Apply background color based on rarity
                cell_item.setData(Qt.ItemDataRole.UserRole, item.id)
                self.inventory_table.setItem(i, col, cell_item)
                
                # Apply background styling
                self.inventory_table.item(i, col).setBackground(QColor(rarity_bg_colors.get(item.rarity, "#2A2A2A")))
                
                # Make the text for common items a bit brighter for better contrast
                if item.rarity == ItemRarity.COMMON:
                    self.inventory_table.item(i, col).setForeground(QColor("#cccccc"))
            
            # Actions - create a better-styled delete button
            delete_btn = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon), "")
            delete_btn.setToolTip("Remove this item")
            delete_btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 3px;
                    background-color: #3A3A3A;
                }
                QPushButton:hover {
                    background-color: #cc4444;
                    border-color: #ff5555;
                }
            """)
            delete_btn.clicked.connect(lambda _, item_id=item.id: self.remove_item(item_id))
            self.inventory_table.setCellWidget(i, 6, delete_btn)
        
        # Re-enable signals
        self.inventory_table.blockSignals(False)
        
        # Update inventory summary
        total_items = sum(item.quantity for item in self.current_character.inventory)
        total_weight = self.current_character.total_weight()
        total_value = self.current_character.total_value()
        
        self.total_items_label.setText(f"Total Items: {total_items}")
        self.total_weight_label.setText(f"Total Weight: {total_weight:.1f} lb")
        self.total_value_label.setText(f"Total Value: {total_value:.1f} gp")
    
    def create_new_character(self):
        """Create a new character"""
        name, ok = QInputDialog.getText(self, "New Character", "Character Name:")
        
        if ok and name:
            game_system, ok = QInputDialog.getText(self, "New Character", "Game System:")
            
            if ok:
                character = self.character_manager.create_character(name, game_system)
                
                # Add to combo box
                self.character_combo.addItem(character.name, character.id)
                
                # Select new character
                index = self.character_combo.findData(character.id)
                self.character_combo.setCurrentIndex(index)
                
                self.status_bar.showMessage(f"Created character: {name}")
    
    def delete_character(self):
        """Delete the current character"""
        if not self.current_character:
            return
        
        reply = QMessageBox.question(
            self, 
            "Delete Character", 
            f"Are you sure you want to delete {self.current_character.name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            character_id = self.current_character.id
            character_name = self.current_character.name
            
            # Delete character
            if self.character_manager.delete_character(character_id):
                # Remove from combo box
                index = self.character_combo.currentIndex()
                self.character_combo.removeItem(index)
                
                self.status_bar.showMessage(f"Deleted character: {character_name}")
    def save_character(self):
        """Save the current character"""
        if not self.current_character:
            return
        
        # Update character with UI data
        self.current_character.name = self.name_edit.text()
        self.character_combo.setItemText(self.character_combo.currentIndex(), self.current_character.name)
        
        self.current_character.game_system = self.game_system_edit.text()
        self.current_character.level = self.level_spin.value()
        
        # Update currency
        self.current_character.currency.platinum = self.platinum_spin.value()
        self.current_character.currency.gold = self.gold_spin.value()
        self.current_character.currency.silver = self.silver_spin.value()
        self.current_character.currency.copper = self.copper_spin.value()
        
        # Update total currency display
        total_copper = self.current_character.currency.total_in_copper()
        self.total_currency_label.setText(f"Total (in copper): {total_copper}")
        
        # Update notes - now using QTextEdit instead of QLineEdit
        self.current_character.notes = self.notes_edit.toPlainText()
        
        # Update timestamp
        self.current_character.updated_at = datetime.now().isoformat()
        
        # Save to file
        if self.character_manager.save_character(self.current_character.id):
            self.status_bar.showMessage(f"Saved character: {self.current_character.name}")
            self.update_status()  # Update the last saved timestamp in status bar
        else:
            self.status_bar.showMessage("Error saving character")
    
    def open_character(self):
        """Open a character file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Character", 
            self.character_manager.save_dir, 
            "Character Files (*.json)"
        )
        
        if file_path:
            character = self.character_manager.load_character(file_path)
            
            if character:
                # Check if character already exists in combo box
                index = self.character_combo.findData(character.id)
                
                if index < 0:
                    # Add to combo box
                    self.character_combo.addItem(character.name, character.id)
                    index = self.character_combo.count() - 1
                
                # Select character
                self.character_combo.setCurrentIndex(index)
                
                self.status_bar.showMessage(f"Loaded character: {character.name}")
    
    def add_item(self):
        """Add an item to the current character's inventory"""
        if not self.current_character:
            return
        
        # Get item data from UI
        name = self.item_name_edit.text()
        
        if not name:
            QMessageBox.warning(self, "Invalid Item", "Item name is required.")
            return
        
        description = self.item_desc_edit.text()
        quantity = self.item_quantity_spin.value()
        weight = self.item_weight_spin.value()
        value = self.item_value_spin.value()
        rarity = ItemRarity[self.item_rarity_combo.currentText().upper()]
        
        # Create item
        item = Item(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            quantity=quantity,
            weight=weight,
            value=value,
            rarity=rarity
        )
        
        # Add to inventory
        self.current_character.add_item(item)
        
        # Update UI
        self.update_inventory_table()
        
        # Clear inputs
        self.item_name_edit.clear()
        self.item_desc_edit.clear()
        self.item_quantity_spin.setValue(1)
        self.item_weight_spin.setValue(0)
        self.item_value_spin.setValue(0)
        
        self.status_bar.showMessage(f"Added item: {name}")
    
    def remove_item(self, item_id):
        """Remove an item from the current character's inventory"""
        if not self.current_character:
            return
        
        item = self.current_character.remove_item(item_id)
        
        if item:
            # Update UI
            self.update_inventory_table()
            
            self.status_bar.showMessage(f"Removed item: {item.name}")
    
    def convert_currency(self):
        """Convert between different currency denominations"""
        if not self.current_character:
            return
            
        amount = self.convert_amount_spin.value()
        from_type = self.convert_from_combo.currentText().lower()
        to_type = self.convert_to_combo.currentText().lower()
        
        # Convert everything to copper first
        copper_values = {
            "copper": 1,
            "silver": 10,
            "gold": 100,
            "platinum": 1000
        }
        
        total_copper = amount * copper_values[from_type]
        result = total_copper / copper_values[to_type]
        
        # Show result in a message box
        QMessageBox.information(
            self,
            "Currency Conversion",
            f"{amount} {from_type} = {result:.2f} {to_type}"
        )
        
        # Apply conversion to character's currency if confirmed
        reply = QMessageBox.question(
            self,
            "Apply Conversion?",
            f"Would you like to subtract {amount} {from_type} and add {int(result)} {to_type} to your character's currency?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Subtract the original currency
            if from_type == "copper":
                self.current_character.currency.copper -= amount
            elif from_type == "silver":
                self.current_character.currency.silver -= amount
            elif from_type == "gold":
                self.current_character.currency.gold -= amount
            elif from_type == "platinum":
                self.current_character.currency.platinum -= amount
                
            # Add the converted currency
            if to_type == "copper":
                self.current_character.currency.copper += int(result)
            elif to_type == "silver":
                self.current_character.currency.silver += int(result)
            elif to_type == "gold":
                self.current_character.currency.gold += int(result)
            elif to_type == "platinum":
                self.current_character.currency.platinum += int(result)
                
            # Update UI
            self.update_ui()
      def convert_currency(self):
        """Convert between different currency denominations"""
        if not self.current_character:
            return
            
        amount = self.convert_amount_spin.value()
        from_type = self.convert_from_combo.currentText().lower()
        to_type = self.convert_to_combo.currentText().lower()
        
        # Convert everything to copper first
        copper_values = {
            "copper": 1,
            "silver": 10,
            "gold": 100,
            "platinum": 1000
        }
        
        total_copper = amount * copper_values[from_type]
        result = total_copper / copper_values[to_type]
        
        # Show result in a message box
        QMessageBox.information(
            self,
            "Currency Conversion",
            f"{amount} {from_type} = {result:.2f} {to_type}"
        )
        
        # Apply conversion to character's currency if confirmed
        reply = QMessageBox.question(
            self,
            "Apply Conversion?",
            f"Would you like to subtract {amount} {from_type} and add {int(result)} {to_type} to your character's currency?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Subtract the original currency
            if from_type == "copper":
                self.current_character.currency.copper -= amount
            elif from_type == "silver":
                self.current_character.currency.silver -= amount
            elif from_type == "gold":
                self.current_character.currency.gold -= amount
            elif from_type == "platinum":
                self.current_character.currency.platinum -= amount
                
            # Add the converted currency
            if to_type == "copper":
                self.current_character.currency.copper += int(result)
            elif to_type == "silver":
                self.current_character.currency.silver += int(result)
            elif to_type == "gold":
                self.current_character.currency.gold += int(result)
            elif to_type == "platinum":
                self.current_character.currency.platinum += int(result)
                
            # Update UI
            self.update_ui()
    
    def update_status(self):
        """Update the status bar with current information"""
        if not self.current_character:
            self.last_saved_label.setText("No character loaded")
            self.item_count_label.setText("Items: 0")
            self.total_weight_status_label.setText("Weight: 0.0 lb")
            return
        
        # Format the last saved time nicely
        try:
            saved_dt = datetime.fromisoformat(self.current_character.updated_at)
            last_saved = saved_dt.strftime("%Y-%m-%d %H:%M:%S")
            self.last_saved_label.setText(f"Last saved: {last_saved}")
        except (ValueError, TypeError):
            self.last_saved_label.setText("Last saved: Unknown")
        
        # Update item count and weight in status bar
        total_items = sum(item.quantity for item in self.current_character.inventory)
        self.item_count_label.setText(f"Items: {total_items}")
        
        total_weight = self.current_character.total_weight()
        self.total_weight_status_label.setText(f"Weight: {total_weight:.1f} lb")
    
    def clear_item_form(self):
        """Clear the add item form"""
        self.item_name_edit.clear()
        self.item_desc_edit.clear()
        self.item_quantity_spin.setValue(1)
        self.item_weight_spin.setValue(0.0)
        self.item_value_spin.setValue(0.0)
        self.item_rarity_combo.setCurrentIndex(0)  # Common
        self.item_equipped_check.setCurrentIndex(0)  # Not equipped
        self.item_tags_edit.clear()
    
    def filter_inventory(self):
        """Filter inventory table based on search text and rarity filter"""
        if not self.current_character:
            return
            
        search_text = self.search_edit.text().lower()
        rarity_filter = self.filter_rarity_combo.currentText()
        sort_by = self.sort_by_combo.currentText()
        
        # Sort the inventory first
        sorted_inventory = list(self.current_character.inventory)
        if sort_by == "Name":
            sorted_inventory.sort(key=lambda x: x.name)
        elif sort_by == "Quantity":
            sorted_inventory.sort(key=lambda x: x.quantity, reverse=True)
        elif sort_by == "Weight":
            sorted_inventory.sort(key=lambda x: x.weight, reverse=True)
        elif sort_by == "Value":
            sorted_inventory.sort(key=lambda x: x.value, reverse=True)
        elif sort_by == "Rarity":
            sorted_inventory.sort(key=lambda x: x.rarity.value, reverse=True)
        
        # Now filter and display
        self.inventory_table.setRowCount(0)
        row = 0
        
        for item in sorted_inventory:
            # Filter by search text
            if search_text and search_text not in item.name.lower() and search_text not in item.description.lower():
                continue
                
            # Filter by rarity
            if rarity_filter != "All Rarities" and item.rarity.name.capitalize() != rarity_filter:
                continue
                
            # Add item to table
            self.inventory_table.insertRow(row)
            
            # Fill in row data (reusing code from update_inventory_table)
            # ... (this would be the same code as in update_inventory_table for a single row)
            
            row += 1
            
        # Update counters
        self.total_items_label.setText(f"Showing {row} of {len(self.current_character.inventory)} items")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About TabletopInventory",
            "TabletopInventory 1.0.0\n\n"
            "A character inventory management system for tabletop role-playing games.\n\n"
            "Created with PyQt6 and Python 3.\n"
            "Developed by StrayDog Syndications LLC.\n\n"
            "© 2025 GitHub CoPilot assisted code generation\n"
            "All rights reserved.\n\n"
            "This application is open-source and licensed under the MIT License.\n"
            "See the GitHub repository for more information.\n\n"
        )


def main():
    """Application entry point"""
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tabletop_log.txt")
    with open(log_path, "w") as log:
        log.write("Starting TabletopInventory application...\n")
        try:
            app = QApplication(sys.argv)
            log.write("QApplication created\n")
            
            # Apply global stylesheet
            app.setStyleSheet(GLOBAL_STYLESHEET)
            
            # Create and show splash screen
            splash_pixmap = QPixmap(400, 300)
            splash_pixmap.fill(QColor(40, 40, 40))
            
            # In a real app, you would use an actual image file like this:
            # splash_pixmap = QPixmap("path/to/splash_image.png")
            
            splash = QSplashScreen(splash_pixmap)
            
            # Add text to splash screen
            splash_font = QFont("Segoe UI", 14)
            splash_font.setBold(True)
            splash.setFont(splash_font)
            
            # Show the splash screen
            splash.show()
            splash.showMessage(
                "TabletopInventory\nLoading...", 
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                QColor(200, 200, 200)
            )
            
            app.processEvents()
            
            # Give the splash screen time to display and simulate loading
            for i in range(1, 5):
                splash.showMessage(
                    f"TabletopInventory\nLoading modules... {i*25}%", 
                    Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                    QColor(200, 200, 200)
                )
                app.processEvents()
                QTimer.singleShot(300, lambda: None)
                app.processEvents()
            
            log.write("MainWindow creating...\n")
            window = MainWindow()
            log.write("MainWindow created\n")
            
            # Finish splash and show main window
            splash.finish(window)
            window.show()
            
            log.write("Window shown - if you don't see it, check your display settings\n")
            log.flush()
            return app.exec()
        except Exception as e:
            log.write(f"Error: {str(e)}\n")
            import traceback
            log.write(traceback.format_exc())
            return 1


if __name__ == "__main__":
    sys.exit(main())
```