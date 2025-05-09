#!/usr/bin/env python3
"""
PyQt6 test with file-based logging.
"""

import os
import sys
import traceback
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

def main():
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyqt_test_log.txt")
    with open(log_path, "w") as log:
        log.write("Starting PyQt6 test application...\n")
        try:
            log.write("Creating QApplication...\n")
            app = QApplication(sys.argv)
            log.write("QApplication created successfully\n")
            
            log.write("Creating window...\n")
            window = QWidget()
            window.setWindowTitle("PyQt6 Test")
            window.setGeometry(100, 100, 400, 200)
            
            log.write("Setting up UI...\n")
            layout = QVBoxLayout(window)
            label = QLabel("If you can see this, PyQt6 is working correctly!")
            layout.addWidget(label)
            
            log.write("Showing window...\n")
            window.show()
            log.write("Window show() method called\n")
            
            log.write("Starting event loop...\n")
            log.flush()
            return app.exec()
            
        except Exception as e:
            log.write(f"Error: {str(e)}\n")
            log.write(traceback.format_exc())
            return 1

if __name__ == "__main__":
    sys.exit(main())
