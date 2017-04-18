import mock
import unittest
import triple_triple.court_regions as cr


class TestCourtRegions(unittest.TestCase):
    """Tests for court_regions.py"""

    def test_get_region_bounds_left_ss(self):
        with mock.patch('triple_triple.class_court_regions.CourtRegions') as mocked:
            PERIMETER = mocked.return_value
            MID_RANGE = mocked.return_value
            KEY = mocked.return_value
            PAINT = mocked.return_value
            BACK_COURT = mocked.return_value
            OUT_OF_BOUNDS = mocked.return_value

            self.assertEqual(
                first=cr.get_region_bounds(shooting_side='left'),
                second=(PERIMETER, MID_RANGE, KEY, PAINT, BACK_COURT, OUT_OF_BOUNDS)
            )

    def test_region_bounds_bad_input(self):
        with self.assertRaises(ValueError):
            cr.get_region_bounds('bad_input')

    def test_get_region_perimeter_left_ss(self):
        self.assertEqual(
            first=cr.get_region(29, 6, shooting_side='left'),
            second='perimeter'
        )

    def test_get_region_perimeter_right_ss(self):
        self.assertEqual(
            first=cr.get_region(61.3, 9.6, shooting_side='right'),
            second='perimeter'
        )

    def test_get_region_midrange_left_ss(self):
        self.assertEqual(
            first=cr.get_region(17.5, 36.36, shooting_side='left'),
            second='mid_range'
        )

    def test_get_region_midrange_right_ss(self):
        self.assertEqual(
            first=cr.get_region(72.15, 13.97, shooting_side='right'),
            second='mid_range'
        )

    def test_get_region_key_left_ss(self):
        self.assertEqual(
            first=cr.get_region(22.35, 25.31, shooting_side='left'),
            second='key'
        )

    def test_get_region_key_right_ss(self):
        self.assertEqual(
            first=cr.get_region(72.15, 29.97, shooting_side='right'),
            second='key'
        )

    def test_get_region_paint_left_ss(self):
        self.assertEqual(
            first=cr.get_region(5.19, 29.39, shooting_side='left'),
            second='paint'
        )

    def test_get_region_paint_right_ss(self):
        self.assertEqual(
            first=cr.get_region(86.43, 25.97, shooting_side='right'),
            second='paint'
        )

    def test_get_region_back_court_left_ss(self):
        self.assertEqual(
            first=cr.get_region(64.23, 43.39, shooting_side='left'),
            second='back_court'
        )

    def test_get_region_back_court_right_ss(self):
        self.assertEqual(
            first=cr.get_region(3.17, 10.18, shooting_side='right'),
            second='back_court'
        )

    def test_get_region_out_of_bounds_left(self):
        self.assertEqual(
            first=cr.get_region(-2.45, 34.45, shooting_side='left'),
            second='out_of_bounds'
        )

    def test_get_region_out_of_bounds_top(self):
        self.assertEqual(
            first=cr.get_region(3.17, 51.48, shooting_side='right'),
            second='out_of_bounds'
        )

    def test_get_region_out_of_bounds_right(self):
        self.assertEqual(
            first=cr.get_region(96.45, 34, shooting_side='left'),
            second='out_of_bounds'
        )

    def test_get_region_out_of_bounds_bottom(self):
        self.assertEqual(
            first=cr.get_region(3.17, -2, shooting_side='right'),
            second='out_of_bounds'
        )

    def test_get_region_bad_input(self):
        with self.assertRaises(ValueError):
            cr.get_region('bad_input', 'bad_input', 'bad_input')

if __name__ == '__main__':
    unittest.main()
