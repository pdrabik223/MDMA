import re
import sys

from PyQt5.QtCore import QRegularExpression, Qt
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit

from src.gui_controls.SpectrumAnalyzerControllerWidget import (
    SpectrumAnalyzerControllerWidget,
)

app = QApplication(sys.argv)


class TestSpectrumAnalyzerControllerWidget:
    def test_frequency_input_validation(self):
        widget = SpectrumAnalyzerControllerWidget()

        # Test frequency input validation
        valid_inputs = ["10 Hz", "1.23 kHz", "100 MHz", "3.5 GHz"]
        invalid_inputs = ["abc", "10.5 mHz", "10.123456 GHz"]
        validator = QRegularExpressionValidator(
            QRegularExpression(widget.freq_box_regex)
        )

        for input_str in valid_inputs:
            assert (
                validator.validate(input_str, 0)[0]
                == QRegularExpressionValidator.Acceptable
            )
        for input_str in invalid_inputs:
            assert (
                validator.validate(input_str, 0)[0]
                == QRegularExpressionValidator.Invalid
            )

    def test_frequency_parsing(self):
        widget = SpectrumAnalyzerControllerWidget()

        # Test frequency parsing
        widget.freq_box.setText("10 Hz")
        assert widget.parse_freq_box() == (10.0, "Hz")

        widget.freq_box.setText("1.23 kHz")
        assert widget.parse_freq_box() == (1.23, "kHz")

        widget.freq_box.setText("100 MHz")
        assert widget.parse_freq_box() == (100, "MHz")

        widget.freq_box.setText("3.5 GHz")
        assert widget.parse_freq_box() == (3.5, "GHz")
