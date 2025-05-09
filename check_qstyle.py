try:
    from PyQt6.QtWidgets import QStyle, QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    print("PyQt6 QStyle StandardPixmap values:")
    for attr in dir(QStyle.StandardPixmap):
        if not attr.startswith('__'):
            print(f"  {attr}")
    
    # Test if some specific attributes exist
    print("\nTesting if specific attributes exist:")
    icons_to_test = [
        "SP_FileDialogDetailedView",
        "SP_FileDialogListView",
        "SP_FileIcon",
        "SP_DialogOpenButton"
    ]
    
    for icon in icons_to_test:
        try:
            attr = getattr(QStyle.StandardPixmap, icon)
            print(f"  {icon} exists: {attr}")
        except AttributeError:
            print(f"  {icon} does NOT exist")
            
except Exception as e:
    print(f"Error: {str(e)}")
