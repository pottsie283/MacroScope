import pytest
from PySide6.QtWidgets import QApplication
from gui.main import MainWindow
import sys

@pytest.fixture(scope="module")
def app():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app

# GUI smoke test

def test_mainwindow_launch(app):
    window = MainWindow()
    window.show()
    assert window.windowTitle() == "MacroScope Document Malware Triage Toolkit"
    assert window.tabs.count() == 3
    assert window.open_button.text() == "Open Document"
