import mock
import unittest
import numpy as np
import triple_triple.court_region_coord as crc


class TestCourtRegionCoord(unittest.TestCase):
    """Tests for court_region_coord.py"""
    # Test triangle coord
    def test_check_pts_make_triange_x_collinear_points(self):
        p1 = [1, 0]
        p2 = [1, 1]
        p3 = [1, 2]
        self.assertFalse(expr=crc.check_pts_make_triangle(p1=p1, p2=p2, p3=p3))

    def test_check_pts_make_triange_y_collinear_points(self):
        p1 = [0, 1]
        p2 = [1, 1]
        p3 = [2, 1]
        self.assertFalse(expr=crc.check_pts_make_triangle(p1=p1, p2=p2, p3=p3))

    def test_check_pts_make_triange_non_collinear(self):
        p1 = [0, 0]
        p2 = [1, 1]
        p3 = [1, 0]
        self.assertTrue(expr=crc.check_pts_make_triangle(p1=p1, p2=p2, p3=p3))

    # Test centroid_triangle
    def test_centroid_triangle_on_non_triangle(self):
        p1 = [1, 0]
        p2 = [1, 1]
        p3 = [1, 2]

        with self.assertRaises(ValueError):
            self.assertRaises(crc.centroid_triangle(p1=p1, p2=p2, p3=p3))

    def test_centroid_triangle_on_basic_triangle(self):
        p1 = [0, 0]
        p2 = [1, 1]
        p3 = [2, 0]
        self.assertEqual(
            first=crc.centroid_triangle(p1=p1, p2=p2, p3=p3),
            second=[1, 1 / 3.]
        )

    # Test generate_back_court
    def test_generate_back_court_left_shooting_side(self):
        self.assertEqual(
            first=crc.generate_back_court('left'),
            second=[70.5, 25]
        )

    def test_generate_back_court_right_shooting_side(self):
        self.assertEqual(
            first=crc.generate_back_court('right'),
            second=[23.5, 25]
        )

    def test_generate_back_court_wrong_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(crc.generate_back_court('bad_input'))

    # Test generate mid-range
    @mock.patch('numpy.random.choice', return_value=0)
    def test_generate_mid_range_left_ss_component_0(self, return_value):
        self.assertEqual(
            first=crc.generate_mid_range('left'),
            second=[9.5, 11]
        )

    @mock.patch('numpy.random.choice', return_value=0)
    def test_generate_mid_range_right_ss_component_0(self, return_value):
        self.assertEqual(
            first=crc.generate_mid_range('right'),
            second=[84.5, 11]
        )

    @mock.patch('numpy.random.choice', return_value=1)
    def test_generate_mid_range_left_ss_component_1(self, return_value):
        self.assertEqual(
            first=crc.generate_mid_range('left'),
            second=[9.5, 39]
        )

    @mock.patch('numpy.random.choice', return_value=1)
    def test_generate_mid_range_right_ss_component_1(self, return_value):
        self.assertEqual(
            first=crc.generate_mid_range('right'),
            second=[84.5, 39]
        )

    @mock.patch('numpy.random.choice', return_value=2)
    def test_generate_mid_range_left_ss_component_2(self, return_value):
        self.assertEqual(
            first=crc.generate_mid_range('left'),
            second=[27.5, 25]
        )

    @mock.patch('numpy.random.choice', return_value=2)
    def test_generate_mid_range_right_ss_component_2(self, return_value):
        self.assertEqual(
            first=crc.generate_mid_range('right'),
            second=[67, 25]
        )

    def test_generate_mid_range_wrong_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(crc.generate_back_court('bad_input'))

    # Test generate_key
    def test_generate_key_left_shooting_side(self):
        self.assertEqual(
            first=crc.generate_key('left'),
            second=[22, 25]
        )

    def test_generate_key_right_shooting_side(self):
        self.assertEqual(
            first=crc.generate_key('right'),
            second=[72, 25]
        )

    def test_generate_key_wrong_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(crc.generate_key('bad_input'))

    # Test generate_paint
    def test_generate_paint_left_shooting_side(self):
        self.assertEqual(
            first=crc.generate_paint('left'),
            second=[9.5, 25]
        )

    def test_generate_paint_right_shooting_side(self):
        self.assertEqual(
            first=crc.generate_paint('right'),
            second=[84.5, 25]
        )

    def test_generate_paint_wrong_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(crc.generate_paint('bad_input'))

    # Test generate_out_of_bounds
    def test_generate_out_of_bounds_left_shooting_side(self):
        self.assertEqual(
            first=crc.generate_out_of_bounds('left'),
            second=[-2, 25]
        )

    def test_generate_out_of_bounds_right_shooting_side(self):
        self.assertEqual(
            first=crc.generate_out_of_bounds('right'),
            second=[96, 25]
        )

    def test_generate_out_of_bounds_wrong_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(crc.generate_out_of_bounds('bad_input'))

    # Test generate perimeter
    @mock.patch('numpy.random.choice', return_value=0)
    def test_generate_perimeter_left_ss_component_0(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('left'),
            second=[7, 1.5]
        )

    @mock.patch('numpy.random.choice', return_value=1)
    def test_generate_perimeter_left_ss_component_1(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('left'),
            second=[7, 48.5]
        )

    @mock.patch('numpy.random.choice', return_value=2)
    def test_generate_perimeter_left_ss_component_2(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('left'),
            second=[36, 25 / 3.]
        )

    @mock.patch('numpy.random.choice', return_value=3)
    def test_generate_perimeter_left_ss_component_3(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('left'),
            second=[36, 125 / 3.]
        )

    @mock.patch('numpy.random.choice', return_value=0)
    def test_generate_perimeter_right_ss_component_0(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('right'),
            second=[89, 1.5]
        )

    @mock.patch('numpy.random.choice', return_value=1)
    def test_generate_perimeter_right_ss_component_1(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('right'),
            second=[89, 48.5]
        )

    @mock.patch('numpy.random.choice', return_value=2)
    def test_generate_perimeter_right_ss_component_2(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('right'),
            second=[58, 25 / 3.]
        )

    @mock.patch('numpy.random.choice', return_value=3)
    def test_generate_perimeter_right_ss_component_3(self, return_value):
        self.assertEqual(
            first=crc.generate_perimeter('right'),
            second=[58, 125 / 3.]
        )

    def test_generate_rand_regions_back_court_ss_left(self):
            shooting_side = 'left'
            self.assertEqual(
                first=crc.generate_rand_regions(4, shooting_side),
                second=crc.generate_back_court(shooting_side)
            )

    def test_generate_rand_regions_back_court(self):
        generate_back_court_mock = mock.Mock()
        method_to_mock = ('triple_triple.court_region_coord'
                          '.generate_back_court')
        with mock.patch(method_to_mock, generate_back_court_mock):
            crc.generate_rand_regions(4, 'left/right')
            generate_back_court_mock.assert_called_once_with('left/right')

    def test_generate_rand_regions_mid_range(self):
        generate_mid_range_mock = mock.Mock()
        method_to_mock = ('triple_triple.court_region_coord'
                          '.generate_mid_range')

        with mock.patch(method_to_mock, generate_mid_range_mock):
            crc.generate_rand_regions(1, 'left/right')
            generate_mid_range_mock.assert_called_once_with('left/right')

    def test_generate_rand_regions_key(self):
        generate_key_mock = mock.Mock()
        method_to_mock = ('triple_triple.court_region_coord'
                          '.generate_key')

        with mock.patch(method_to_mock, generate_key_mock):
            crc.generate_rand_regions(2, 'left/right')
            generate_key_mock.assert_called_once_with('left/right')

    def test_generate_rand_regions_out_of_bounds(self):
        generate_out_of_bounds_mock = mock.Mock()
        method_to_mock = ('triple_triple.court_region_coord'
                          '.generate_out_of_bounds')

        with mock.patch(method_to_mock, generate_out_of_bounds_mock):
            crc.generate_rand_regions(5, 'left/right')
            generate_out_of_bounds_mock.assert_called_once_with('left/right')

    def test_generate_rand_regions_paint(self):
        generate_paint_mock = mock.Mock()
        method_to_mock = ('triple_triple.court_region_coord'
                          '.generate_paint')

        with mock.patch(method_to_mock, generate_paint_mock):
            crc.generate_rand_regions(0, 'left/right')
            generate_paint_mock.assert_called_once_with('left/right')

    def test_generate_rand_regions_perimeter(self):
        generate_perimeter_mock = mock.Mock()
        method_to_mock = ('triple_triple.court_region_coord'
                          '.generate_perimeter')

        with mock.patch(method_to_mock, generate_perimeter_mock):
            crc.generate_rand_regions(3, 'left/right')
            generate_perimeter_mock.assert_called_once_with('left/right')

    def test_generate_rand_region_bad_input(self):
        with self.assertRaises(ValueError):
            self.assertRaises(
                crc.generate_rand_regions('bad_input', 'bad_input')
            )

    # def test_generate_rand_regions_mid_range(self):
    #     generate_mid_range_mock = mock.Mock()
    #     generate_mid_range_mock.return_value = [9.5, 11]
    #     method_to_mock = ('triple_triple.court_region_coord'
    #                       '.generate_mid_range')
    #
    #     with mock.patch(method_to_mock, generate_mid_range_mock):
    #         resp = crc.generate_rand_regions('mid_range', 'blarg')
    #
    #     generate_mid_range_mock.assert_called_once_with('blarg')
    #     self.assertEqual(resp, [9.5, 11])


if __name__ == '__main__':
    unittest.main()
