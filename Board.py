class Board:
    board_matrix = None
    def __init__(self, board_size):
        #  self.gui = BoardGUI(side_length, board_size) #
        self.board_matrix = [[0 for _ in range(board_size)] for _ in range(board_size)]
        
    def copy_board(self):
        new_board = Board(len(self.board_matrix))
        new_board.board_matrix = [row[:] for row in self.board_matrix]
        return new_board
        

    def get_board_size(self):
        return len(self.board_matrix)

    def remove_stone_no_gui(self, pos_x, pos_y):
        self.board_matrix[pos_x][pos_y] = 0

    def add_stone_no_gui(self, pos_x, pos_y, black):
        self.board_matrix[pos_x][pos_y] = 2 if black else 1

    def add_stone(self, pos_x, pos_y, black):
        # check if the cell is empty
        if self.board_matrix[pos_x][pos_y] != 0:
            return False

        # self.gui.draw_stone(pos_x, pos_y, black) #
        self.board_matrix[pos_x][pos_y] = 2 if black else 1
        return True

    def generate_moves(self):
        move_list = []
        board_size = len(self.board_matrix)

        # Look for cells that has at least one stone in an adjacent cell.
        for i in range(board_size):
            for j in range(board_size):
                if self.board_matrix[i][j] > 0:
                    continue

                if i > 0:
                    if j > 0:
                        if self.board_matrix[i - 1][j - 1] > 0 or self.board_matrix[i][j - 1] > 0:
                            move = [i, j]
                            move_list.append(move)
                            continue
                    if j < board_size - 1:
                        if self.board_matrix[i - 1][j + 1] > 0 or self.board_matrix[i][j + 1] > 0:
                            move = [i, j]
                            move_list.append(move)
                            continue
                    if self.board_matrix[i - 1][j] > 0:
                        move = [i, j]
                        move_list.append(move)
                        continue
                if i < board_size - 1:
                    if j > 0:
                        if self.board_matrix[i + 1][j - 1] > 0 or self.board_matrix[i][j - 1] > 0:
                            move = [i, j]
                            move_list.append(move)
                            continue
                    if j < board_size - 1:
                        if self.board_matrix[i + 1][j + 1] > 0 or self.board_matrix[i][j + 1] > 0:
                            move = [i, j]
                            move_list.append(move)
                            continue
                    if self.board_matrix[i + 1][j] > 0:
                        move = [i, j]
                        move_list.append(move)
                        continue

        return move_list

    def get_board_matrix(self):
        return self.board_matrix
    
    def printBoard(self):
        for row in self.board_matrix:
            print(row)
        

"""
    def start_listening(self, listener):
        self.gui.attach_listener(listener)

    def get_gui(self):
        return self.gui

    def get_relative_pos(self, x):
        return self.gui.get_relative_pos(x)

    def print_winner(self, winner):
        self.gui.print_winner(winner)

    def thinking_started(self):
        self.gui.set_ai_thinking(True)

    def thinking_finished(self):
        self.gui.set_ai_thinking(False)
"""