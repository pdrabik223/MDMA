import pytest
from PyQt6.QtWidgets import QApplication

from src.gui_controls.FreqLineEdit import FreqLineEdit


class TestFreqLineEdit:
    @pytest.fixture(scope="class")
    def qt_app(self):
        app = QApplication([])
        yield app
        app.exit()

    @pytest.fixture
    def freq_line_edit(self, qt_app):
        return FreqLineEdit()

    def test_valid_frequency(self, freq_line_edit):
        freq_line_edit.setText("1.23 GHz")
        assert freq_line_edit.get_frequency_in_hz() == 1.23e9

    def test_invalid_unit(self, freq_line_edit):
        freq_line_edit.setText("1.23 THz")
        with pytest.raises(ValueError):
            freq_line_edit.get_frequency_in_hz()

    def test_invalid_value(self, freq_line_edit):
        freq_line_edit.setText("abc")
        with pytest.raises(ValueError):
            freq_line_edit.get_frequency_in_hz()
