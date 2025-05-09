#!/usr/bin/env python3
"""
TabletopInventory - A Character Inventory Management System

This application provides a GUI interface for managing character inventories
for tabletop role-playing games. Users can create characters, add/remove items,
track currency, and save/load character data.

Author: GitHub Copilot
Date: May 8, 2025
Version: 1.0.0
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
    QMessageBox, QInputDialog, QScrollArea, QGroupBox, QFormLayout
)
from PyQt6.QtGui import QIcon, QFont, QAction
from PyQt6.QtCore import Qt, QSize


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
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("TabletopInventory")
        self.setMinimumSize(800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Character tab
        self.character_tab = QWidget()
        self.tabs.addTab(self.character_tab, "Characters")
        
        character_layout = QVBoxLayout(self.character_tab)
        
        # Character selection
        char_select_layout = QHBoxLayout()
        character_layout.addLayout(char_select_layout)
        
        self.character_combo = QComboBox()
        self.character_combo.currentIndexChanged.connect(self.on_character_selected)
        char_select_layout.addWidget(QLabel("Character:"))
        char_select_layout.addWidget(self.character_combo, stretch=1)
        
        # Character buttons
        self.new_char_btn = QPushButton("New Character")
        self.new_char_btn.clicked.connect(self.create_new_character)
        self.delete_char_btn = QPushButton("Delete Character")
        self.delete_char_btn.clicked.connect(self.delete_character)
        self.save_char_btn = QPushButton("Save Character")
        self.save_char_btn.clicked.connect(self.save_character)
        
        char_select_layout.addWidget(self.new_char_btn)
        char_select_layout.addWidget(self.delete_char_btn)
        char_select_layout.addWidget(self.save_char_btn)
        
        # Character details
        char_details_group = QGroupBox("Character Details")
        character_layout.addWidget(char_details_group)
        
        details_layout = QFormLayout(char_details_group)
        
        self.name_edit = QLineEdit()
        self.game_system_edit = QLineEdit()
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 99)
        
        details_layout.addRow("Name:", self.name_edit)
        details_layout.addRow("Game System:", self.game_system_edit)
        details_layout.addRow("Level:", self.level_spin)
        
        # Currency group
        currency_group = QGroupBox("Currency")
        character_layout.addWidget(currency_group)
        
        currency_layout = QHBoxLayout(currency_group)
        
        self.platinum_spin = QSpinBox()
        self.platinum_spin.setRange(0, 999999)
        self.gold_spin = QSpinBox()
        self.gold_spin.setRange(0, 999999)
        self.silver_spin = QSpinBox()
        self.silver_spin.setRange(0, 999999)
        self.copper_spin = QSpinBox()
        self.copper_spin.setRange(0, 999999)
        
        currency_layout.addWidget(QLabel("Platinum:"))
        currency_layout.addWidget(self.platinum_spin)
        currency_layout.addWidget(QLabel("Gold:"))
        currency_layout.addWidget(self.gold_spin)
        currency_layout.addWidget(QLabel("Silver:"))
        currency_layout.addWidget(self.silver_spin)
        currency_layout.addWidget(QLabel("Copper:"))
        currency_layout.addWidget(self.copper_spin)
        
        # Inventory tab
        self.inventory_tab = QWidget()
        self.tabs.addTab(self.inventory_tab, "Inventory")
        
        inventory_layout = QVBoxLayout(self.inventory_tab)
        
        # Add item section
        add_item_group = QGroupBox("Add Item")
        inventory_layout.addWidget(add_item_group)
        
        add_item_layout = QFormLayout(add_item_group)
        
        self.item_name_edit = QLineEdit()
        self.item_desc_edit = QLineEdit()
        self.item_quantity_spin = QSpinBox()
        self.item_quantity_spin.setRange(1, 9999)
        self.item_weight_spin = QDoubleSpinBox()
        self.item_weight_spin.setRange(0, 9999.99)
        self.item_weight_spin.setSingleStep(0.1)
        self.item_value_spin = QDoubleSpinBox()
        self.item_value_spin.setRange(0, 9999.99)
        self.item_value_spin.setSingleStep(0.1)
        self.item_rarity_combo = QComboBox()
        
        for rarity in ItemRarity:
            self.item_rarity_combo.addItem(rarity.name.capitalize())
        
        add_item_layout.addRow("Name:", self.item_name_edit)
        add_item_layout.addRow("Description:", self.item_desc_edit)
        add_item_layout.addRow("Quantity:", self.item_quantity_spin)
        add_item_layout.addRow("Weight:", self.item_weight_spin)
        add_item_layout.addRow("Value:", self.item_value_spin)
        add_item_layout.addRow("Rarity:", self.item_rarity_combo)
        
        add_item_btn = QPushButton("Add Item")
        add_item_btn.clicked.connect(self.add_item)
        add_item_layout.addRow("", add_item_btn)
        
        # Inventory table
        self.inventory_table = QTableWidget(0, 7)
        self.inventory_table.setHorizontalHeaderLabels(["Name", "Quantity", "Weight", "Value", "Rarity", "Description", "Actions"])
        inventory_layout.addWidget(self.inventory_table, stretch=1)
        
        # Inventory summary
        summary_layout = QHBoxLayout()
        inventory_layout.addLayout(summary_layout)
        
        self.total_items_label = QLabel("Total Items: 0")
        self.total_weight_label = QLabel("Total Weight: 0.0")
        self.total_value_label = QLabel("Total Value: 0.0")
        
        summary_layout.addWidget(self.total_items_label)
        summary_layout.addWidget(self.total_weight_label)
        summary_layout.addWidget(self.total_value_label)
        
        # Notes tab
        self.notes_tab = QWidget()
        self.tabs.addTab(self.notes_tab, "Notes")
        
        notes_layout = QVBoxLayout(self.notes_tab)
        
        self.notes_edit = QLineEdit()
        self.notes_edit.setPlaceholderText("Enter character notes here...")
        notes_layout.addWidget(self.notes_edit)
        
        # Set up menu bar
        menu_bar = self.menuBar()
        
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
        
        # Set up status bar
        self.status_bar = self.statusBar()
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
            self.notes_edit.setText("")
            self.inventory_table.setRowCount(0)
            self.total_items_label.setText("Total Items: 0")
            self.total_weight_label.setText("Total Weight: 0.0")
            self.total_value_label.setText("Total Value: 0.0")
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
        
        # Update notes
        self.notes_edit.setText(self.current_character.notes)
        
        # Update inventory table
        self.update_inventory_table()
    
    def update_inventory_table(self):
        """Update inventory table with current character's items"""
        if not self.current_character:
            self.inventory_table.setRowCount(0)
            return
        
        # Disconnect signals to prevent recursion
        self.inventory_table.blockSignals(True)
        
        # Clear table
        self.inventory_table.setRowCount(0)
        
        # Add items
        for i, item in enumerate(self.current_character.inventory):
            self.inventory_table.insertRow(i)
            
            # Item name
            name_item = QTableWidgetItem(item.name)
            self.inventory_table.setItem(i, 0, name_item)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(item.quantity))
            self.inventory_table.setItem(i, 1, quantity_item)
            
            # Weight
            weight_item = QTableWidgetItem(f"{item.weight:.1f}")
            self.inventory_table.setItem(i, 2, weight_item)
            
            # Value
            value_item = QTableWidgetItem(f"{item.value:.1f}")
            self.inventory_table.setItem(i, 3, value_item)
            
            # Rarity
            rarity_item = QTableWidgetItem(item.rarity.name.capitalize())
            self.inventory_table.setItem(i, 4, rarity_item)
            
            # Description
            desc_item = QTableWidgetItem(item.description)
            self.inventory_table.setItem(i, 5, desc_item)
            
            # Actions
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, item_id=item.id: self.remove_item(item_id))
            self.inventory_table.setCellWidget(i, 6, delete_btn)
        
        # Re-enable signals
        self.inventory_table.blockSignals(False)
        
        # Update inventory summary
        total_items = sum(item.quantity for item in self.current_character.inventory)
        total_weight = self.current_character.total_weight()
        total_value = self.current_character.total_value()
        
        self.total_items_label.setText(f"Total Items: {total_items}")
        self.total_weight_label.setText(f"Total Weight: {total_weight:.1f}")
        self.total_value_label.setText(f"Total Value: {total_value:.1f}")
    
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
        
        # Update notes
        self.current_character.notes = self.notes_edit.text()
        
        # Update timestamp
        self.current_character.updated_at = datetime.now().isoformat()
        
        # Save to file
        if self.character_manager.save_character(self.current_character.id):
            self.status_bar.showMessage(f"Saved character: {self.current_character.name}")
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
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About TabletopInventory",
            "TabletopInventory 1.0.0\n\n"
            "A character inventory management system for tabletop role-playing games.\n\n"
            "Created with PyQt6 and Python 3.\n"
            "© 2025 GitHub Copilot"
        )


def main():
    """Application entry point"""
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tabletop_log.txt")
    with open(log_path, "w") as log:
        log.write("Starting TabletopInventory application...\n")
        try:
            app = QApplication(sys.argv)
            log.write("QApplication created\n")
            window = MainWindow()
            log.write("MainWindow created\n")
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