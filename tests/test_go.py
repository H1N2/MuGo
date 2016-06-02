import unittest
import go

MANUAL_EMPTY_BOARD = '''         
.........
.........
.........
.........
.........
.........
.........
.........
.........
          '''


class TestGoBoard(unittest.TestCase):
    def test_load_board(self):
        self.assertEqual(len(go.EMPTY_BOARD), (go.W * (go.W + 1)))
        self.assertEqual(go.EMPTY_BOARD, MANUAL_EMPTY_BOARD)
        self.assertEqual(go.EMPTY_BOARD, go.load_board('. \n' * go.N ** 2))

    def test_parsing(self):
        self.assertEqual(go.parse_coords('A' + str(go.N)), go.W)

    def test_neighbors(self):
        corner = go.parse_coords('A1')
        neighbors = [go.EMPTY_BOARD[c] for c in go.neighbors(corner)]
        self.assertEqual(sum(1 for n in neighbors if n.isspace()), 2)

        side = go.parse_coords('A2')
        side_neighbors = [go.EMPTY_BOARD[c] for c in go.neighbors(side)]
        self.assertEqual(sum(1 for n in side_neighbors if n.isspace()), 1)

class TestGroupHandling(unittest.TestCase):
    def test_update_groups(self):
        board = go.load_board('''
            .X.......
            X........
            .........
            .........
            .........
            .........
            .........
            .........
            .........
        ''')
        pc = go.parse_coords
        existing_groups = [
            go.Group(
                stones=set([pc('B9')]),
                liberties=set([pc('A9'), pc('C9'), pc('B8')])
            ),
            go.Group(
                stones=set([pc('A8')]),
                liberties=set([pc('A9'), pc('A7'), pc('B8')])
            )
        ]
        updated_board = go.place_stone(board, 'X', go.parse_coords('A9'))
        updated_groups = go.update_groups(updated_board, existing_groups, go.parse_coords('A9'))
        self.assertEqual(updated_groups, [go.Group(
            stones=set([pc('A8'), pc('A9'), pc('B9')]),
            liberties=set([pc('A7'), pc('B8'), pc('C9')])
        )])
