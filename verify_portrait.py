#!/usr/bin/env python3
"""
Character Portrait Verification Script

This script loads the pasa_phist.json file directly and verifies 
that the portrait path is correctly set and the file exists.

Author: GitHub Copilot
Date: May 9, 2025
"""

import json
import os
import sys

def verify_portrait():
    """Verify that the portrait file exists and is correctly referenced"""
    
    json_path = "pasa_phist.json"
    
    if not os.path.exists(json_path):
        print(f"Error: Could not find {json_path}")
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            character_data = json.load(f)
        
        print(f"Character name: {character_data.get('name')}")
        
        portrait_path = character_data.get('portrait')
        if not portrait_path:
            print("Error: No portrait specified in the character file")
            return False
            
        print(f"Portrait path in JSON: {portrait_path}")
        
        # Check if the portrait file exists
        app_dir = os.path.dirname(os.path.abspath(__file__))
        full_portrait_path = os.path.join(app_dir, portrait_path)
        
        if os.path.exists(full_portrait_path):
            print(f"Portrait file found at: {full_portrait_path}")
            return True
        else:
            print(f"Error: Portrait file not found at {full_portrait_path}")
            
            # Check for similar files in the directory
            portrait_dir = os.path.dirname(full_portrait_path)
            if os.path.exists(portrait_dir):
                print(f"Contents of {portrait_dir}:")
                for file in os.listdir(portrait_dir):
                    print(f"  - {file}")
            return False
            
    except Exception as e:
        print(f"Error processing character file: {e}")
        return False

if __name__ == "__main__":
    success = verify_portrait()
    print(f"\nVerification {'successful' if success else 'failed'}.")
