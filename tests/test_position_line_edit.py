import pytest
from PyQt5.QtWidgets import QApplication

from gui_controls.custom_input_fiedls.PositionLineEdit import PositionLineEdit


class TestPositionLineEdit:
    @pytest.fixture(scope="class")
    def qt_app(self):
        app = QApplication([])
        yield app
        app.exit()

    @pytest.fixture
    def position_line_edit(self, qt_app):
        return PositionLineEdit()

    def test_default_value(self, position_line_edit):
        assert position_line_edit.text() == "50 mm"

    def test_valid_input(self, position_line_edit):
        position_line_edit.setText("20 cm")
        assert position_line_edit.get_value_in_mm() == 200

        position_line_edit.setText("30.5 mm")
        assert position_line_edit.get_value_in_mm() == 30.5

    def test_invalid_input(self, position_line_edit):
        position_line_edit.setText("abc")
        with pytest.raises(ValueError):
            position_line_edit.get_value_in_mm()

        position_line_edit.setText("100 kg")
        with pytest.raises(ValueError):
            position_line_edit.get_value_in_mm()
