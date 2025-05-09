import sys
import re

# Path to the input file
input_file = r'c:\Users\Petro\repos\MyFull_MontyPython\tabletop_inventory.py'

# Read the input file content
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Define a regular expression pattern to match QStyle.SP_* occurrences
# This pattern ensures we match the exact pattern with proper word boundaries
pattern = r'QStyle\.SP_([A-Za-z]+)'
replacement = r'QStyle.StandardPixmap.SP_\1'

# Count occurrences before replacement
matches = re.findall(pattern, content)
print(f"Found {len(matches)} occurrences of QStyle.SP_* to update")

# Replace all occurrences with QStyle.StandardPixmap.SP_*
modified_content = re.sub(pattern, replacement, content)

# Write the modified content back to the file
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"Updated all QStyle.SP_* references in {input_file}")
print("Done!")
