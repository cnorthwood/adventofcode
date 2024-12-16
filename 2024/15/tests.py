from textwrap import dedent
import unittest

from challenge import Direction, EMPTY, check_width_aware_move, unsafe_width_aware_move, visualise


class TestWideBoxes(unittest.TestCase):
    def test_box_can_move_sidewise(self):
        grid = self._build_grid(".[].#")
        self.assertTrue(check_width_aware_move((0, 0), grid, Direction.RIGHT))

    def test_box_can_not_move_sidewise_into_wall(self):
        grid = self._build_grid(".[]#")
        self.assertFalse(check_width_aware_move((0, 0), grid, Direction.RIGHT))

    def test_box_moves_sidewise(self):
        grid = self._build_grid(".[].#")

        unsafe_width_aware_move((0, 0), grid, Direction.RIGHT)

        self.assertEqual(grid, self._build_grid("..[]#"))

    def test_chain_box_moves_sidewise(self):
        grid = self._build_grid(".[][].#")

        unsafe_width_aware_move((0, 0), grid, Direction.RIGHT)

        self.assertEqual(grid, self._build_grid("..[][]#"))

    def test_chain_box_can_move_sidewise(self):
        grid = self._build_grid(".[][]#")

        self.assertFalse(check_width_aware_move((0, 0), grid, Direction.RIGHT))

    def test_chain_box_can_not_move_sidewise(self):
        grid = self._build_grid(".[][].#")

        self.assertTrue(check_width_aware_move((0, 0), grid, Direction.RIGHT))

    def test_chain_box_moves_sidewise_and_stops_by_collision(self):
        grid = self._build_grid(".[].[]#")

        unsafe_width_aware_move((0, 0), grid, Direction.RIGHT)

        self.assertEqual(grid, self._build_grid("..[][]#"))

    def test_box_left_moves_up(self):
        grid = self._build_grid(
            """
            ##
            ..
            []
            ..
            """
        )

        self.assertTrue(check_width_aware_move((0, 3), grid, Direction.UP))
        unsafe_width_aware_move((0, 3), grid, Direction.UP)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ##
                []
                ..
                ..
                """
            )
        )

    def test_box_left_moves_down(self):
        grid = self._build_grid(
            """
            ..
            []
            ..
            ##
            """
        )

        self.assertTrue(check_width_aware_move((0, 0), grid, Direction.DOWN))
        unsafe_width_aware_move((0, 0), grid, Direction.DOWN)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ..
                ..
                []
                ##
                """
            )
        )

    def test_box_right_moves_up(self):
        grid = self._build_grid(
            """
            ##
            ..
            []
            ..
            """
        )

        self.assertTrue(check_width_aware_move((1, 3), grid, Direction.UP))
        unsafe_width_aware_move((1, 3), grid, Direction.UP)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ##
                []
                ..
                ..
                """
            )
        )

    def test_box_right_moves_down(self):
        grid = self._build_grid(
            """
            ..
            []
            ..
            ##
            """
        )

        self.assertTrue(check_width_aware_move((1, 0), grid, Direction.DOWN))
        unsafe_width_aware_move((1, 0), grid, Direction.DOWN)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ..
                ..
                []
                ##
                """
            )
        )

    def test_chaining_boxes_moves_down_left(self):
        grid = self._build_grid(
            """
            ..
            []
            []
            ..
            ##
            """
        )

        self.assertTrue(check_width_aware_move((0, 0), grid, Direction.DOWN))
        unsafe_width_aware_move((0, 0), grid, Direction.DOWN)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ..
                ..
                []
                []
                ##
                """
            )
        )

    def test_chaining_boxes_moves_down_right(self):
        grid = self._build_grid(
            """
            ..
            []
            []
            ..
            ##
            """
        )

        self.assertTrue(check_width_aware_move((1, 0), grid, Direction.DOWN))
        unsafe_width_aware_move((1, 0), grid, Direction.DOWN)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ..
                ..
                []
                []
                ##
                """
            )
        )

    def test_cascading_boxes_moves_down(self):
        grid = self._build_grid(
            """
            ....
            .[].
            [][]
            ....
            ####
            """
        )

        self.assertTrue(check_width_aware_move((1, 0), grid, Direction.DOWN))
        unsafe_width_aware_move((1, 0), grid, Direction.DOWN)

        self.assertEqual(
            grid,
            self._build_grid(
                """
                ....
                ....
                .[].
                [][]
                ####
                """
            )
        )

    def test_cascading_boxes_can_not_move_down_with_a_wall(self):
        grid = self._build_grid(
            """
            ....
            .[].
            [][]
            ####
            """
        )

        self.assertFalse(check_width_aware_move((1, 0), grid, Direction.DOWN))

    def test_cascading_boxes_can_not_move_down_with_a_wall_right(self):
        grid = self._build_grid(
            """
            ....
            .[].
            [][]
            ####
            """
        )

        self.assertFalse(check_width_aware_move((2, 0), grid, Direction.DOWN))

    def test_cascading_boxes_can_not_move_down_with_a_partial_wall(self):
        grid = self._build_grid(
            """
            ....
            .[].
            [][]
            ...#
            ####
            """
        )

        self.assertFalse(check_width_aware_move((1, 0), grid, Direction.DOWN))

    def _build_grid(self, grid):
        parsed_grid = {}
        for y, line in enumerate(dedent(grid.strip()).splitlines()):
            line = line.strip()
            for x, c in enumerate(line):
                parsed_grid[x, y] = c
        return parsed_grid


if __name__ == "__main__":
    unittest.main()
