import unittest
import triple_triple.class_court_regions as ccr


class TestClassCourtRegions(unittest.TestCase):
    """Tests for class_court_regions.py"""

    def test_get_polygon_perimeter_out_of_bounds(self):
        polygon_perimeter_l = ccr.get_polygon_perimeter('left')
        polygon_perimeter_r = ccr.get_polygon_perimeter('right')

        out_of_bounds_points = [
            (0, -1),
            (-1, 0),
            (99, 10),
            (10, 99),
            (47, 51),
            (47, -1),
            (0, 0)
        ]
        for polygon_perimeter in polygon_perimeter_l, polygon_perimeter_r:
            for x, y in out_of_bounds_points:
                self.assertFalse(polygon_perimeter(x, y))

        self.assertTrue(polygon_perimeter_l(46, 25))
        self.assertTrue(polygon_perimeter_r(48, 25))
        # polygon_perimeter_mock = mock.Mock()
        # method_to_mock = ('triple_triple.class_court_regions.polygon_perimeter')
        # with mock.patch(method_to_mock, polygon_perimeter_mock):
        #     ccr.get_polygon_perimeter('right')
        #     polygon_perimeter_mock.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
