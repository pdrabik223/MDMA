from functionalities.PrinterPath import f_range


class TestFRange:
    def test_f_range(self):
        # Test case 1: Default arguments
        assert f_range() == [0]

        # Test case 2: Start = 0, End = 5, Step = 1
        assert f_range(start=0, end=5, step=1) == [0, 1, 2, 3, 4]

        # Test case 3: Start = 1, End = 10, Step = 2
        assert f_range(start=1, end=10, step=2) == [1, 3, 5, 7, 9]

        # Test case 4: Start = -5, End = 5, Step = 2
        assert f_range(start=-5, end=5, step=2) == [-5, -3, -1, 1, 3]

        # Test case 5: Start = 0, End = 10, Step = 3, Include start and end
        assert f_range(start=0, end=10, step=3, include_start=True, include_end=True) == [0, 3, 6, 9, 12]

        assert f_range(0.1, 2.2, 0.3, True, True) == [0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9000000000000001, 2.2]

        range = f_range(0.1, 2.2, 0.3, True, True)
        rounder_range = [round(val, 4) for val in range]
        assert rounder_range == [0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9, 2.2]
