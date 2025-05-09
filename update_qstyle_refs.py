import re

# Path to the input file
input_file = r'c:\Users\Petro\repos\MyFull_MontyPython\tabletop_inventory.py'

# Read the input file content
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Count original occurrences
original_count = len(re.findall(r'QStyle\.SP_', content))
print(f"Found {original_count} occurrences of QStyle.SP_")

# Define a more specific pattern to match exactly QStyle.SP_*
# This pattern ensures we match the entire token with word boundaries
pattern = r'(QStyle\.)(SP_[a-zA-Z]+)'

# Replace all occurrences with QStyle.StandardPixmap.SP_*
modified_content = re.sub(pattern, r'\1StandardPixmap.\2', content)

# Count new occurrences to verify
new_count = len(re.findall(r'QStyle\.StandardPixmap\.SP_', modified_content))
print(f"Replaced with {new_count} occurrences of QStyle.StandardPixmap.SP_")

if original_count == new_count:
    print("All occurrences successfully updated!")
    # Write the modified content back to the file
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print(f"Updated all QStyle.SP_* references in {input_file}")
else:
    print(f"Warning: Original count ({original_count}) doesn't match new count ({new_count})")
    print("No changes were made to the file.")
