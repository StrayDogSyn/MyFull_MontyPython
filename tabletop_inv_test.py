#!/usr/bin/env python3
"""
TabletopInventory - Status Bar Test
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QStatusBar
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    """Test main window with enhanced status bar"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Status Bar Test")
        self.setGeometry(100, 100, 800, 600)
        
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
        
        self.total_weight_label = QLabel("Weight: 0.0 lb")
        self.total_weight_label.setStyleSheet("padding: 2px 10px;")
        self.status_bar.addPermanentWidget(self.total_weight_label)
        
        self.status_bar.showMessage("Application ready")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
