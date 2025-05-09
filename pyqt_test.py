#!/usr/bin/env python3
"""
Simple PyQt6 test script to verify installation and functionality.
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("PyQt6 Test Window")
    window.setGeometry(100, 100, 400, 200)
    
    layout = QVBoxLayout(window)
    label = QLabel("If you can see this, PyQt6 is working correctly!")
    layout.addWidget(label)
    
    window.show()
    
    print("PyQt6 window should be visible now. Close the window to exit.")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
