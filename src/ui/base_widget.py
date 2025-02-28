from PySide6.QtWidgets import QWidget

from src.utils.gui_utilites import connect_async


class BaseWidget(QWidget):
    """Base widget class that provides common functionality for all widgets"""

    def __init__(self, /, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        self._initialize_state()

    def _setup_ui(self):
        """Set up UI components"""
        pass

    def _connect_signals(self):
        """Connect widget signals to slots"""
        pass

    def _initialize_state(self):
        """Initialize widget state"""
        pass

    def connect_async_signals(self, connections: list):
        """
        Connect multiple signals to async slots at once

        Args:
            connections: List of tuples (widget, signal, async_method)
        """
        for widget, signal, async_method in connections:
            connect_async(widget, signal, async_method)
