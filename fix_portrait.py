#!/usr/bin/env python3
"""
Fix Portrait Loading Script for TabletopInventory

This script fixes issues with the portrait label in the tabletop_inventory.py file.
It modifies the portrait_layout initialization in the init_ui method to avoid 
duplication of portrait_label variables.

Author: GitHub Copilot
Date: May 9, 2025
"""

import os
import sys
import re

def fix_portrait_layout():
    """Fix the portrait layout code in tabletop_inventory.py"""
    
    filepath = "tabletop_inventory.py"
    temp_filepath = "tabletop_inventory_temp.py"
    
    if not os.path.exists(filepath):
        print(f"Error: Could not find {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix the portrait layout section
    portrait_pattern = r"""        # Add character portrait with image loading capability
        portrait_layout = QVBoxLayout\(\)
        portrait_label = QLabel\("Character Portrait"\)
        portrait_label\.setAlignment\(Qt\.AlignmentFlag\.AlignCenter\)
        
        # Create the portrait display
        self\.portrait_label = QLabel\(\)
        self\.portrait_label\.setFrameShape\(QFrame\.Shape\.StyledPanel\)
        self\.portrait_label\.setMinimumSize\(150, 150\)
        self\.portrait_label\.setMaximumSize\(150, 150\)
        self\.portrait_label\.setStyleSheet\("background-color: #333333; border: 1px solid #555555;"\)
        self\.portrait_label\.setAlignment\(Qt\.AlignmentFlag\.AlignCenter\)
        self\.portrait_label\.setScaledContents\(True\)
        
        # Add a button to change portrait
        change_portrait_btn = QPushButton\("Change Portrait"\)
        change_portrait_btn\.clicked\.connect\(self\.change_character_portrait\)
        
        portrait_layout\.addWidget\(portrait_label\)
        portrait_layout\.addWidget\(self\.portrait_label\)
        portrait_layout\.addWidget\(change_portrait_btn\)
        portrait_layout\.addStretch\(\)
        details_layout\.addRow\("", portrait_layout\)"""
    
    fixed_portrait = """        # Add character portrait with image loading capability
        portrait_layout = QVBoxLayout()
        portrait_title_label = QLabel("Character Portrait")
        portrait_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create the portrait display
        self.portrait_label = QLabel()
        self.portrait_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.portrait_label.setMinimumSize(150, 150)
        self.portrait_label.setMaximumSize(150, 150)
        self.portrait_label.setStyleSheet("background-color: #333333; border: 1px solid #555555;")
        self.portrait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portrait_label.setScaledContents(True)
        
        # Add a button to change portrait
        change_portrait_btn = QPushButton("Change Portrait")
        change_portrait_btn.clicked.connect(self.change_character_portrait)
        
        portrait_layout.addWidget(portrait_title_label)
        portrait_layout.addWidget(self.portrait_label)
        portrait_layout.addWidget(change_portrait_btn)
        portrait_layout.addStretch()
        details_layout.addRow("", portrait_layout)"""
    
    # Use relaxed matching due to potential whitespace differences
    updated_content = re.sub(re.escape("""        # Add character portrait with image loading capability
        portrait_layout = QVBoxLayout()
        portrait_label = QLabel("Character Portrait")
        portrait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create the portrait display
        self.portrait_label = QLabel()"""), 
        """        # Add character portrait with image loading capability
        portrait_layout = QVBoxLayout()
        portrait_title_label = QLabel("Character Portrait")
        portrait_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create the portrait display
        self.portrait_label = QLabel()""", content, flags=re.MULTILINE)
    
    # Also fix the reference to portrait_label in the layout
    updated_content = re.sub(r'portrait_layout\.addWidget\(portrait_label\)', 
                          'portrait_layout.addWidget(portrait_title_label)', 
                          updated_content)
    
    with open(temp_filepath, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    # Replace the original file with the updated one
    try:
        os.replace(temp_filepath, filepath)
        print(f"Successfully updated {filepath}. Portrait layout fixed.")
        return True
    except Exception as e:
        print(f"Error replacing file: {e}")
        return False

if __name__ == "__main__":
    fix_portrait_layout()
