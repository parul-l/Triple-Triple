import unittest
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
            second=[1, 1/3.]
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

if __name__ == '__main__':
    unittest.main()
