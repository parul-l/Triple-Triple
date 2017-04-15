import mock
import unittest
import triple_triple.court_regions as cr


class TestCourtRegions(unittest.TestCase):
    """Tests for court_regions.py"""

    # left shooting_side
    def test_get_region_paint_left_ss(self):
        self.assertEqual(
            first=cr.get_region(x=4, y=20, shooting_side='left'),
            second='paint'
        )

    def test_get_region_key_left_ss(self):
        self.assertEqual(
            first=cr.get_region(x=20, y=26, shooting_side='left'),
            second='key'
        )

    def test_get_region_mid_range_left_ss(self):
        self.assertEqual(
            first=cr.get_region(x=15, y=44, shooting_side='left'),
            second='mid_range'
        )

    def test_get_region_perimeter_left_ss(self):
        self.assertEqual(
            first=cr.get_region(x=38, y=25, shooting_side='left'),
            second='perimeter'
        )

    def test_get_region_back_court_left_ss(self):
        self.assertEqual(
            first=cr.get_region(x=50, y=45, shooting_side='left'),
            second='back_court'
        )

    def test_get_region_out_of_bounds_left_ss(self):
        self.assertEqual(
            first=cr.get_region(x=18, y=50, shooting_side='left'),
            second='out_of_bounds'
        )


    # right shooting_side
    def test_get_region_paint_right_ss(self):
        self.assertEqual(
            first=cr.get_region(x=75, y=25, shooting_side='right'),
            second='paint'
        )

    def test_get_region_key_right_ss(self):
        self.assertEqual(
            first=cr.get_region(x=73, y=30, shooting_side='right'),
            second='key'
        )

    def test_get_region_mid_range_right_ss(self):
        self.assertEqual(
            first=cr.get_region(x=74, y=43, shooting_side='right'),
            second='mid_range'
        )

    def test_get_region_perimeter_right_ss(self):
        self.assertEqual(
            first=cr.get_region(x=65, y=2.5, shooting_side='right'),
            second='perimeter'
        )

    def test_get_region_back_court_right_ss(self):
        self.assertEqual(
            first=cr.get_region(x=5, y=15, shooting_side='right'),
            second='back_court'
        )

    def test_get_region_out_of_bounds_right_ss(self):
        self.assertEqual(
            first=cr.get_region(x=-2, y=5, shooting_side='right'),
            second='out_of_bounds'
        )

    def test_get_region_bad_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(cr.get_region('bad_input', 'bad_input', 'bad_input'))

if __name__ == '__main__':
    unittest.main()
