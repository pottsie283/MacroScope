
import sys
import os
import hashlib
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget, QTabWidget, QLabel, QHBoxLayout, QMenuBar, QMenu, QAction, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent
from macroscope.analysis.office import OfficeAnalyzer
from macroscope.analysis.pdf import PDFAnalyzer
from macroscope.report import Report

import importlib

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MacroScope Document Malware Triage Toolkit")
        self.setMinimumSize(900, 600)
        self.setAcceptDrops(True)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open Document", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Plugin menu
        plugin_menu = menubar.addMenu("Plugins")
        self.plugin_actions = []
        self.selected_plugins = set()
        self.available_plugins = self.discover_plugins()
        for plugin in self.available_plugins:
            action = QAction(plugin, self)
            action.setCheckable(True)
            action.toggled.connect(lambda checked, p=plugin: self.toggle_plugin(p, checked))
            plugin_menu.addAction(action)
            self.plugin_actions.append(action)

        # Tabs
        self.tabs = QTabWidget()
        self.info_tab = QWidget()
        self.findings_tab = QWidget()
        self.risk_tab = QWidget()
        self.tabs.addTab(self.info_tab, "File Info")
        self.tabs.addTab(self.findings_tab, "Findings")
        self.tabs.addTab(self.risk_tab, "Risk Score")

        # Info tab
        self.info_layout = QVBoxLayout()
        self.file_label = QLabel("No file loaded.")
        self.hash_label = QLabel("")
        self.info_layout.addWidget(self.file_label)
        self.info_layout.addWidget(self.hash_label)
        self.info_tab.setLayout(self.info_layout)

        # Findings tab
        self.findings_layout = QVBoxLayout()
        self.findings_text = QTextEdit()
        self.findings_text.setReadOnly(True)
        self.findings_layout.addWidget(self.findings_text)
        self.findings_tab.setLayout(self.findings_layout)

        # Risk tab
        self.risk_layout = QVBoxLayout()
        self.risk_label = QLabel("No analysis yet.")
        self.risk_layout.addWidget(self.risk_label)
        self.risk_tab.setLayout(self.risk_layout)

        # Main layout
        main_layout = QVBoxLayout()
        self.open_button = QPushButton("Open Document")
        self.open_button.clicked.connect(self.open_file)
        main_layout.addWidget(self.open_button)
        main_layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load style
        style_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def discover_plugins(self):
        # Discover plugins in macroscope.plugins
        plugin_dir = os.path.join(os.path.dirname(__file__), "..", "macroscope", "plugins")
        plugins = []
        for fname in os.listdir(plugin_dir):
            if fname.endswith(".py") and not fname.startswith("__"):
                plugins.append(fname[:-3])
        return plugins

    def toggle_plugin(self, plugin, checked):
        if checked:
            self.selected_plugins.add(plugin)
        else:
            self.selected_plugins.discard(plugin)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Document", "", "Documents (*.doc *.docx *.xls *.xlsx *.ppt *.pptx *.pdf)")
        if file_path:
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        self.file_label.setText(f"File: {os.path.basename(file_path)}")
        self.hash_label.setText(f"SHA256: {self.get_sha256(file_path)}")
        if file_path.lower().endswith(".pdf"):
            analyzer = PDFAnalyzer()
        else:
            analyzer = OfficeAnalyzer()
        findings = analyzer.analyze(file_path)
        # Run plugins
        plugin_results = {}
        for plugin in self.selected_plugins:
            try:
                mod = importlib.import_module(f"macroscope.plugins.{plugin}")
                plugin_class = getattr(mod, [c for c in dir(mod) if c.endswith("Plugin")][0])
                plugin_instance = plugin_class()
                plugin_results[plugin] = plugin_instance.run(file_path)
            except Exception as e:
                plugin_results[plugin] = {"error": str(e)}
        findings["plugins"] = plugin_results
        report = Report(findings)
        self.findings_text.setPlainText(report.to_json())
        self.risk_label.setText(f"Risk Score: {report.risk_score}")

    def get_sha256(self, file_path):
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path:
                self.analyze_file(file_path)

    def show_about(self):
        QMessageBox.information(self, "About MacroScope", "Unified Document Malware Triage Toolkit\n\nDeveloped with security and privacy in mind.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
