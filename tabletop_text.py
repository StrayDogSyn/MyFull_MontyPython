#!/usr/bin/env python3
"""
TabletopInventory (Text Edition) - A Character Inventory Management System

This application provides a text-based interface for managing character inventories
for tabletop role-playing games. Users can create characters, add/remove items,
track currency, and save/load character data.

Author: StrayDog Syndications LLC
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
            
    def display(self) -> str:
        """Return a string representation of the item"""
        equipped_str = "[E]" if self.equipped else ""
        return f"{self.name} {equipped_str} - Qty: {self.quantity}, Value: {self.value}, Weight: {self.weight}, Rarity: {self.rarity.name.capitalize()}"


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
        
    def display(self) -> str:
        """Return a string representation of the currency"""
        return f"PP: {self.platinum}, GP: {self.gold}, SP: {self.silver}, CP: {self.copper}"


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


class TextInterface:
    """Text-based user interface for TabletopInventory"""
    
    def __init__(self):
        """Initialize the text interface"""
        self.character_manager = CharacterManager()
        self.current_character = None
        self.running = True
        
    def main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("TABLETOP INVENTORY MANAGER".center(50))
        print("=" * 50)
        print(f"Current Character: {self.current_character.name if self.current_character else 'None'}")
        print("-" * 50)
        print("1. Create New Character")
        print("2. Load Character")
        print("3. Save Character")
        print("4. Character Details")
        print("5. Inventory Management")
        print("6. Currency Management")
        print("7. Exit")
        print("-" * 50)
        
        choice = input("Enter choice (1-7): ")
        
        if choice == "1":
            self.create_character()
        elif choice == "2":
            self.load_character()
        elif choice == "3":
            self.save_character()
        elif choice == "4":
            self.character_details()
        elif choice == "5":
            self.inventory_management()
        elif choice == "6":
            self.currency_management()
        elif choice == "7":
            self.running = False
        else:
            print("Invalid choice. Please try again.")
    
    def create_character(self):
        """Create a new character"""
        print("\n" + "=" * 50)
        print("CREATE NEW CHARACTER".center(50))
        print("=" * 50)
        
        name = input("Enter character name: ")
        if not name:
            print("Character name cannot be empty.")
            return
        
        game_system = input("Enter game system (or leave blank for Generic): ")
        if not game_system:
            game_system = "Generic"
        
        level = input("Enter character level (or leave blank for 1): ")
        try:
            level = int(level) if level else 1
        except ValueError:
            level = 1
            
        character = self.character_manager.create_character(name, game_system)
        character.level = level
        self.current_character = character
        
        print(f"Character '{name}' created successfully!")
    
    def load_character(self):
        """Load a character from file"""
        print("\n" + "=" * 50)
        print("LOAD CHARACTER".center(50))
        print("=" * 50)
        
        # Get all character files
        character_files = []
        for file_name in os.listdir(self.character_manager.save_dir):
            if file_name.endswith(".json"):
                character_files.append(file_name)
        
        if not character_files:
            print("No saved characters found.")
            return
        
        # Display character files
        print("Available characters:")
        for i, file_name in enumerate(character_files, 1):
            print(f"{i}. {file_name}")
        
        choice = input("Enter choice (or 0 to cancel): ")
        try:
            choice = int(choice)
            if choice == 0:
                return
            if choice < 1 or choice > len(character_files):
                print("Invalid choice.")
                return
            
            file_path = os.path.join(self.character_manager.save_dir, character_files[choice - 1])
            character = self.character_manager.load_character(file_path)
            if character:
                self.current_character = character
                print(f"Character '{character.name}' loaded successfully!")
            else:
                print("Failed to load character.")
        except ValueError:
            print("Invalid choice.")
    
    def save_character(self):
        """Save the current character to file"""
        if not self.current_character:
            print("No character selected.")
            return
        
        print("\n" + "=" * 50)
        print("SAVE CHARACTER".center(50))
        print("=" * 50)
        
        # Update timestamp
        self.current_character.updated_at = datetime.now().isoformat()
        
        # Save character
        if self.character_manager.save_character(self.current_character.id):
            print(f"Character '{self.current_character.name}' saved successfully!")
        else:
            print("Failed to save character.")
    
    def character_details(self):
        """View and edit character details"""
        if not self.current_character:
            print("No character selected.")
            return
        
        print("\n" + "=" * 50)
        print("CHARACTER DETAILS".center(50))
        print("=" * 50)
        print(f"Name: {self.current_character.name}")
        print(f"Game System: {self.current_character.game_system}")
        print(f"Level: {self.current_character.level}")
        print(f"Currency: {self.current_character.currency.display()}")
        print(f"Created: {self.current_character.created_at}")
        print(f"Updated: {self.current_character.updated_at}")
        print(f"Notes: {self.current_character.notes}")
        print("-" * 50)
        print("1. Edit Name")
        print("2. Edit Game System")
        print("3. Edit Level")
        print("4. Edit Notes")
        print("5. Back to Main Menu")
        print("-" * 50)
        
        choice = input("Enter choice (1-5): ")
        
        if choice == "1":
            name = input("Enter new name: ")
            if name:
                self.current_character.name = name
                print("Name updated.")
        elif choice == "2":
            game_system = input("Enter new game system: ")
            if game_system:
                self.current_character.game_system = game_system
                print("Game system updated.")
        elif choice == "3":
            level = input("Enter new level: ")
            try:
                level = int(level)
                self.current_character.level = level
                print("Level updated.")
            except ValueError:
                print("Invalid level.")
        elif choice == "4":
            notes = input("Enter new notes: ")
            self.current_character.notes = notes
            print("Notes updated.")
        elif choice == "5":
            return
        else:
            print("Invalid choice.")
    
    def inventory_management(self):
        """Manage character inventory"""
        if not self.current_character:
            print("No character selected.")
            return
        
        while True:
            print("\n" + "=" * 50)
            print("INVENTORY MANAGEMENT".center(50))
            print("=" * 50)
            print(f"Character: {self.current_character.name}")
            print(f"Total Items: {sum(item.quantity for item in self.current_character.inventory)}")
            print(f"Total Weight: {self.current_character.total_weight():.1f}")
            print(f"Total Value: {self.current_character.total_value():.1f}")
            print("-" * 50)
            print("1. View Inventory")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Back to Main Menu")
            print("-" * 50)
            
            choice = input("Enter choice (1-4): ")
            
            if choice == "1":
                self.view_inventory()
            elif choice == "2":
                self.add_item()
            elif choice == "3":
                self.remove_item()
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
    
    def view_inventory(self):
        """View character inventory"""
        if not self.current_character.inventory:
            print("Inventory is empty.")
            return
        
        print("\n" + "=" * 50)
        print("INVENTORY".center(50))
        print("=" * 50)
        
        for i, item in enumerate(self.current_character.inventory, 1):
            print(f"{i}. {item.display()}")
            if item.description:
                print(f"   Description: {item.description}")
        
        input("\nPress Enter to continue...")
    
    def add_item(self):
        """Add an item to inventory"""
        print("\n" + "=" * 50)
        print("ADD ITEM".center(50))
        print("=" * 50)
        
        name = input("Enter item name: ")
        if not name:
            print("Item name cannot be empty.")
            return
        
        description = input("Enter item description (optional): ")
        
        quantity = input("Enter quantity (default 1): ")
        try:
            quantity = int(quantity) if quantity else 1
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        
        weight = input("Enter weight (default 0): ")
        try:
            weight = float(weight) if weight else 0.0
            if weight < 0:
                weight = 0.0
        except ValueError:
            weight = 0.0
        
        value = input("Enter value (default 0): ")
        try:
            value = float(value) if value else 0.0
            if value < 0:
                value = 0.0
        except ValueError:
            value = 0.0
        
        print("Rarity options:")
        for i, rarity in enumerate(ItemRarity, 1):
            print(f"{i}. {rarity.name.capitalize()}")
        
        rarity_choice = input("Enter rarity (1-6, default 1): ")
        try:
            rarity_index = int(rarity_choice) - 1 if rarity_choice else 0
            if rarity_index < 0 or rarity_index >= len(ItemRarity):
                rarity_index = 0
            rarity = list(ItemRarity)[rarity_index]
        except ValueError:
            rarity = ItemRarity.COMMON
        
        equipped = input("Is this item equipped? (y/n, default n): ").lower() == 'y'
        
        item = Item(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            quantity=quantity,
            weight=weight,
            value=value,
            rarity=rarity,
            equipped=equipped
        )
        
        self.current_character.add_item(item)
        print(f"Item '{name}' added to inventory.")
    
    def remove_item(self):
        """Remove an item from inventory"""
        if not self.current_character.inventory:
            print("Inventory is empty.")
            return
        
        print("\n" + "=" * 50)
        print("REMOVE ITEM".center(50))
        print("=" * 50)
        
        for i, item in enumerate(self.current_character.inventory, 1):
            print(f"{i}. {item.name} (Qty: {item.quantity})")
        
        choice = input("Enter item number to remove (or 0 to cancel): ")
        try:
            choice = int(choice)
            if choice == 0:
                return
            if choice < 1 or choice > len(self.current_character.inventory):
                print("Invalid choice.")
                return
            
            item = self.current_character.inventory[choice - 1]
            self.current_character.remove_item(item.id)
            print(f"Item '{item.name}' removed from inventory.")
        except ValueError:
            print("Invalid choice.")
    
    def currency_management(self):
        """Manage character currency"""
        if not self.current_character:
            print("No character selected.")
            return
        
        while True:
            print("\n" + "=" * 50)
            print("CURRENCY MANAGEMENT".center(50))
            print("=" * 50)
            print(f"Character: {self.current_character.name}")
            print(f"Currency: {self.current_character.currency.display()}")
            print(f"Total in Copper: {self.current_character.currency.total_in_copper()}")
            print("-" * 50)
            print("1. Edit Platinum")
            print("2. Edit Gold")
            print("3. Edit Silver")
            print("4. Edit Copper")
            print("5. Back to Main Menu")
            print("-" * 50)
            
            choice = input("Enter choice (1-5): ")
            
            if choice == "1":
                self.edit_currency("platinum")
            elif choice == "2":
                self.edit_currency("gold")
            elif choice == "3":
                self.edit_currency("silver")
            elif choice == "4":
                self.edit_currency("copper")
            elif choice == "5":
                break
            else:
                print("Invalid choice.")
    
    def edit_currency(self, currency_type: str):
        """Edit a currency value"""
        current_value = getattr(self.current_character.currency, currency_type)
        
        print(f"Current {currency_type.capitalize()}: {current_value}")
        new_value = input(f"Enter new {currency_type} amount: ")
        
        try:
            new_value = int(new_value)
            if new_value < 0:
                print("Currency cannot be negative.")
                return
            
            setattr(self.current_character.currency, currency_type, new_value)
            print(f"{currency_type.capitalize()} updated to {new_value}.")
        except ValueError:
            print("Invalid value.")
    
    def run(self):
        """Run the text interface"""
        print("Welcome to TabletopInventory (Text Edition)!")
        
        while self.running:
            self.main_menu()
        
        print("Thank you for using TabletopInventory!")


def main():
    """Application entry point"""
    interface = TextInterface()
    interface.run()


if __name__ == "__main__":
    main()
