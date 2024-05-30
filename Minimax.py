import time
import math
from Board import *

class Minimax:
    # Biến này được sử dụng để theo dõi số lần đánh giá cho mục đích đo hiệu suất.
    evaluation_count = 0

    #Điểm số chiến thắng phải lớn hơn tất cả các điểm số có thể có trên bảng.
    WIN_SCORE = 100_000_000
    
    board = None

    def __init__(self, board):
        self.board = board

    @staticmethod
    def get_win_score():
        return Minimax.WIN_SCORE

    # Hàm này tính điểm tương đối của người chơi trắng so với người chơi đen.
	# (tức là khả năng người chơi trắng chiến thắng trò chơi trước người chơi đen như thế nào)
	# Giá trị này sẽ được sử dụng làm điểm trong thuật toán Minimax.
    @staticmethod
    def evaluate_board_for_white(board, blacks_turn):
        Minimax.evaluation_count += 1

        # Lấy điểm của cả hai người chơi.
        black_score = Minimax.get_score(board, True, blacks_turn)
        white_score = Minimax.get_score(board, False, blacks_turn)

        if black_score == 0:
            black_score = 1.0

        #Tính điểm tương đối của trắng so với đen.
        return white_score / black_score

    # Hàm này tính điểm của bảng cho người chơi được chỉ định.
	# (tức là vị trí tổng quát của một người chơi trên bảng như thế nào bằng cách xem xét có bao nhiêu 
	#  liên tiếp 2, 3, 4, bị chặn như thế nào, v.v...)
    @staticmethod
    def get_score(board, for_black, blacks_turn):
        #Đọc bảng
        board_matrix = board.get_board_matrix()

        #Tính điểm cho mỗi hướng
        return (Minimax.evaluate_horizontal(board_matrix, for_black, blacks_turn) +
                Minimax.evaluate_vertical(board_matrix, for_black, blacks_turn) +
                Minimax.evaluate_diagonal(board_matrix, for_black, blacks_turn))

    # Hàm này được sử dụng để lấy nước đi thông minh tiếp theo cho AI.
    def calculate_next_move(self, depth):
        #Khóa bảng để AI đưa ra quyết định.

        move = [0, 0]

        #Chỉ sử dụng cho mục đích đo hiệu suất.
        start_time = time.time()

        # Kiểm tra xem có nước đi nào có thể kết thúc trò chơi không để đảm bảo AI luôn
		# nắm lấy cơ hội kết thúc trò chơi.
        best_move = Minimax.search_winning_move(self.board)

        if best_move is not None:
            # Tìm thấy nước đi kết thúc trò chơi
            move[0] = int(best_move[1])
            move[1] = int(best_move[2])
        else:
            # Nếu không có nước đi như vậy, tìm kiếm cây Minimax với độ sâu đã chỉ định.
            best_move = Minimax.minimax_search_ab(depth, self.board, True, -1.0, self.get_win_score())
            if best_move[1] is None:
                move = None
            else:
                move[0] = int(best_move[1])
                move[1] = int(best_move[2])

        print(f"Cases calculated: {Minimax.evaluation_count} Calculation time: {time.time() - start_time:.2f} ms")

        Minimax.evaluation_count = 0

        return move

	 # alpha : Nước đi tốt nhất của AI (Max)
	 # beta : Nước đi tốt nhất của người chơi (Min)
	 # trả về: {score, move[0], move[1]}
    @staticmethod
    def minimax_search_ab(depth, dummy_board, max, alpha, beta):
        # Độ sâu cuối cùng (nút kết thúc), đánh giá điểm hiện tại của bảng.
        if depth == 0:
            return [Minimax.evaluate_board_for_white(dummy_board, not max), None, None]
        # Tạo tất cả các nước đi có thể từ nút này của cây Minimax
		#
		#                  (Nước đi 1)
		#	               /
		#  (Nút hiện tại) --- (Nước đi 2)
		#				   \   ...
		#                  (Nước đi N)
        all_possible_moves = dummy_board.generate_moves()

        # Nếu không có nước đi nào có thể, coi nút này là nút kết thúc và trả về điểm.
        if not all_possible_moves:
            return [Minimax.evaluate_board_for_white(dummy_board, not max), None, None]

        best_move = [None] * 3
        
        # Tạo cây Minimax và tính điểm của nút.
        if max:
            # Khởi tạo nước đi tốt nhất bắt đầu với -vô cực.
            best_move[0] = -math.inf

            #Lặp qua tất cả các nước đi có thể thực hiện.
            for move in all_possible_moves:
                # Thực hiện nước đi trên bảng tạm thời mà không vẽ bất cứ gì
                dummy_board.add_stone_no_gui(move[1], move[0], False)

                # Gọi hàm minimax cho độ sâu tiếp theo, để tìm kiếm điểm tối thiểu.
				# Hàm này sẽ đệ quy tạo ra các cây Minimax mới từ nút này 
				# (nếu depth > 0) và tìm kiếm điểm trắng tối thiểu trong mỗi cây con.
				# Chúng ta sẽ tìm điểm tối đa của độ sâu này, trong số các điểm tối thiểu tìm thấy ở
				# độ sâu thấp hơn
                temp_move = Minimax.minimax_search_ab(depth - 1, dummy_board, False, alpha, beta)

                # Quay lui và loại bỏ nước đi
                dummy_board.remove_stone_no_gui(move[1], move[0])

                # Cập nhật alpha (giá trị alpha giữ điểm tối đa)
				# Khi tìm kiếm điểm tối thiểu, nếu điểm của một nút nhỏ hơn alpha 
				# (điểm tối đa của các nút cùng cấp từ một cấp trên) thì toàn bộ cây con xuất phát
				# từ nút đó sẽ bị loại bỏ, vì người chơi tối đa sẽ chọn nút alpha thay vì bất kỳ nút nào
				# có điểm nhỏ hơn alpha.
                if float(temp_move[0] > alpha):
                    alpha = float(temp_move[0])

                # Cắt tỉa với beta
				# Giá trị beta giữ điểm tối thiểu trong số các nút cùng cấp từ một cấp trên.
				# Chúng ta cần tìm điểm thấp hơn điểm beta này, vì bất kỳ điểm nào cao hơn
				# beta sẽ bị loại bỏ bởi người chơi tối thiểu (cấp trên). Nếu điểm
				# cao hơn (hoặc bằng) beta, dừng vòng lặp, loại bỏ các nút còn lại 
				# và trả về nước đi cuối cùng   
                if float(temp_move[0] >= beta):
                    return temp_move
                
                # Tìm nước đi có điểm tối đa.
                if temp_move[0] > best_move[0]:
                    best_move = temp_move
                    best_move[1] = move[0]
                    best_move[2] = move[1]

        else:
            # Khởi tạo nước đi tốt nhất bắt đầu bằng nước đi đầu tiên trong danh sách và điểm +vô cực.
            best_move[0] = math.inf
            best_move[1] = all_possible_moves[0][0]
            best_move[2] = all_possible_moves[0][1]

            # Lặp qua tất cả các nước đi có thể thực hiện.
            for move in all_possible_moves:
                # Tạo một bảng tạm thời tương đương với bảng hiện tại
				# Thực hiện nước đi trên bảng tạm thời mà không vẽ bất cứ gì
                dummy_board.add_stone_no_gui(move[1], move[0], True)

                # Gọi hàm minimax cho độ sâu tiếp theo, để tìm kiếm điểm tối đa.
				# Hàm này sẽ đệ quy tạo ra các cây Minimax mới từ nút này 
				# (nếu depth > 0) và tìm kiếm điểm trắng tối đa trong mỗi cây con.
				# Chúng ta sẽ tìm điểm tối thiểu của độ sâu này, trong số các điểm tối đa tìm thấy ở
				# độ sâu thấp hơn.
                temp_move = Minimax.minimax_search_ab(depth - 1, dummy_board, True, alpha, beta)

                dummy_board.remove_stone_no_gui(move[1], move[0])

                # Cập nhật beta (giá trị beta giữ điểm tối thiểu)
				# Khi tìm kiếm điểm tối đa, nếu điểm của một nút cao hơn beta 
				# (điểm tối thiểu của các nút cùng cấp từ một cấp trên) thì toàn bộ cây con xuất phát
				# từ nút đó sẽ bị loại bỏ, vì người chơi tối thiểu sẽ chọn nút beta thay vì bất kỳ nút nào
				# có điểm cao hơn beta
                if float(temp_move[0] < beta):
                    beta = float(temp_move[0])

                # Cắt tỉa với alpha
				# Giá trị alpha giữ điểm tối đa trong số các nút cùng cấp từ một cấp trên.
				# Chúng ta cần tìm điểm cao hơn điểm alpha này, vì bất kỳ điểm nào thấp hơn
				# alpha sẽ bị loại bỏ bởi người chơi tối đa (cấp trên). Nếu điểm
				# thấp hơn (hoặc bằng) alpha, dừng vòng lặp, loại bỏ các nút còn lại 
				# và trả về nước đi cuối cùng.  
                if temp_move[0] <= alpha:
                    return temp_move
                
                # Tìm nước đi có điểm tối thiểu.
                if float(temp_move[0]) < float(best_move[0]):
                    best_move = temp_move
                    best_move[1] = move[0]
                    best_move[2] = move[1]
        # Trả về nước đi tốt nhất tìm thấy trong độ sâu này
        return best_move

    # Hàm này tìm kiếm một nước đi có thể ngay lập tức giành chiến thắng trò chơi.
    @staticmethod
    def search_winning_move(board):
        all_possible_moves = board.generate_moves()
        print(all_possible_moves)
        winning_move = [None] * 3

        # Lặp qua tất cả các nước đi có thể
        for move in all_possible_moves:
            Minimax.evaluation_count += 1
 ###        # Tạo một bảng tạm thời tương đương với bảng hiện tại
            dummy_board = board.copy_board()
            # Thực hiện nước đi trên bảng tạm thời mà không vẽ bất cứ gì
            dummy_board.add_stone(move[1], move[0], False)
            
            # Nếu người chơi trắng có điểm số chiến thắng trên bảng tạm thời, trả về nước đi đó.
            if Minimax.get_score(dummy_board, False, False) >= Minimax.get_win_score():
                winning_move[1] = move[0]
                winning_move[2] = move[1]
                return winning_move

        return None

    # Hàm này tính điểm bằng cách đánh giá các vị trí đá theo hướng ngang
    @staticmethod
    def evaluate_horizontal(board_matrix, for_black, players_turn):
        evaluations = [0, 2, 0] # [0] -> số lượng liên tiếp, [1] -> số lần bị chặn, [2] -> điểm số
		# Biến blocks được sử dụng để kiểm tra xem một tập hợp đá liên tiếp bị chặn bởi đối thủ hoặc
		# biên của bảng. Nếu cả hai bên của một tập hợp liên tiếp bị chặn, biến blocks sẽ là 2
		# Nếu chỉ một bên bị chặn, biến blocks sẽ là 1, và nếu cả hai bên của tập hợp liên tiếp
		# đều trống, số lần bị chặn sẽ là 0.
		# Mặc định, ô đầu tiên trong hàng bị chặn bởi biên trái của bảng.
		# Nếu ô đầu tiên trống, số lần bị chặn sẽ giảm 1.
		# Nếu có một ô trống sau tập hợp đá liên tiếp, số lần bị chặn lại giảm 1.
		# Lặp qua tất cả các hàng
        for i in range(len(board_matrix)):
            # Lặp qua tất cả các ô trong hàng
            for j in range(len(board_matrix[0])):
                # Kiểm tra xem người chơi được chọn có đá trong ô hiện tại không
                Minimax.evaluate_directions(board_matrix, i, j, for_black, players_turn, evaluations)
            Minimax.evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

        return evaluations[2]

    # Hàm này tính điểm bằng cách đánh giá các vị trí đá theo hướng dọc
	# Quy trình tương tự như tính toán theo chiều ngang.
    @staticmethod
    def evaluate_vertical(board_matrix, for_black, players_turn):
        evaluations = [0, 2, 0] # [0] -> số lượng liên tiếp, [1] -> số lần bị chặn, [2] -> điểm số

        for j in range(len(board_matrix[0])):
            for i in range(len(board_matrix)):
                Minimax.evaluate_directions(board_matrix, i, j, for_black, players_turn, evaluations)
            Minimax.evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

        return evaluations[2]

    # Hàm này tính điểm bằng cách đánh giá các vị trí đá theo các hướng chéo
	# Quy trình tương tự như tính toán theo chiều ngang.
    @staticmethod
    def evaluate_diagonal(board_matrix, for_black, players_turn):
        evaluations = [0, 2, 0] # [0] -> số lượng liên tiếp, [1] -> số lần bị chặn, [2] -> điểm số
		# Từ dưới-trái đến trên-phải theo đường chéo

        for k in range(2 * len(board_matrix) - 1):
            i_start = max(0, k - len(board_matrix) + 1)
            i_end = min(len(board_matrix) - 1, k)
            for i in range(i_start, i_end + 1):
                Minimax.evaluate_directions(board_matrix, i, k - i, for_black, players_turn, evaluations)
            Minimax.evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

        # Từ trên-trái đến dưới-phải theo đường chéo
        for k in range(1 - len(board_matrix), len(board_matrix)):
            i_start = max(0, k)
            i_end = min(len(board_matrix) + k - 1, len(board_matrix) - 1)
            for i in range(i_start, i_end + 1):
                Minimax.evaluate_directions(board_matrix, i, i - k, for_black, players_turn, evaluations)
            Minimax.evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

        return evaluations[2]

    @staticmethod
    def evaluate_directions(board_matrix, i, j, is_bot, bots_turn, eval):
        # Kiểm tra xem người chơi được chọn có đá trong ô hiện tại không
        if board_matrix[i][j] == (2 if is_bot else 1):
            # Tăng số lượng đá liên tiếp
            eval[0] += 1
        # Kiểm tra xem ô có trống không
        elif board_matrix[i][j] == 0:
            # Kiểm tra xem có đá liên tiếp nào trước ô trống này không
            if eval[0] > 0:
                # Tập hợp liên tiếp không bị chặn bởi đối thủ, giảm số lần bị chặn
                eval[1] -= 1
                # Lấy điểm của tập hợp liên tiếp
                eval[2] += Minimax.get_consecutive_set_score(eval[0], eval[1], is_bot == bots_turn)
                # Đặt lại số lượng đá liên tiếp
                eval[0] = 0
                # Ô hiện tại trống, tập hợp liên tiếp tiếp theo sẽ có tối đa 1 bên bị chặn.

            # Không có đá liên tiếp.
			# Ô hiện tại trống, tập hợp liên tiếp tiếp theo sẽ có tối đa 1 bên bị chặn.
            eval[1] = 1

        # Ô bị chiếm bởi đối thủ
		# Kiểm tra xem có đá liên tiếp nào trước ô trống này không    
        elif eval[0] > 0:
                # Lấy điểm của tập hợp liên tiếp
                eval[2] += Minimax.get_consecutive_set_score(eval[0], eval[1], is_bot == bots_turn)
                # Đặt lại số lượng đá liên tiếp
                eval[0] = 0
                # Ô hiện tại bị chiếm bởi đối thủ, tập hợp liên tiếp tiếp theo có thể có 2 bên bị chặn
                eval[1] = 2
        else: 
            eval[1] = 2

    @staticmethod
    def evaluate_directions_after_one_pass(eval, is_bot, players_turn):
        # Kết thúc hàng, kiểm tra xem có đá liên tiếp nào trước khi chúng ta đạt đến biên phải không
        if eval[0] > 0:
            eval[2] += Minimax.get_consecutive_set_score(eval[0], eval[1], is_bot == players_turn)
        
        # Đặt lại số lượng đá liên tiếp và số lần bị chặn
        eval[0] = 0
        eval[1] = 2

    # Hàm này trả về điểm của một tập hợp đá liên tiếp nhất định.
	# count: Số lượng đá liên tiếp trong tập hợp
	# blocks: Số bên bị chặn của tập hợp (2: cả hai bên bị chặn, 1: một bên bị chặn, 0: cả hai bên đều trống)
    @staticmethod
    def get_consecutive_set_score(count, blocks, current_turn):
        win_guarantee = 1_000_000
        # Nếu cả hai bên của tập hợp bị chặn, tập hợp này không có giá trị gì, trả về 0 điểm.
        if blocks == 2 and count < 5:
            return 0
        # 5 đá liên tiếp sẽ thắng trò chơi
        if count == 5:
            return Minimax.WIN_SCORE
        # 4 đá liên tiếp trong lượt của người dùng đảm bảo thắng.
		# (Người dùng có thể thắng trò chơi bằng cách đặt viên đá thứ 5 sau tập hợp)
        elif count == 4:
            if current_turn:
                return win_guarantee
            # Lượt của đối thủ
			# Nếu không bị chặn bên nào, 4 đá liên tiếp đảm bảo thắng trong lượt tiếp theo.

			# Nếu chỉ một bên bị chặn, 4 đá liên tiếp giới hạn nước đi của đối thủ
			# (Đối thủ chỉ có thể đặt một viên đá sẽ chặn bên còn lại, nếu không trò chơi sẽ thua
			# trong lượt tiếp theo). Vì vậy, điểm số tương đối cao được đưa ra cho tập hợp này.
            else:
                return win_guarantee // 4 if blocks == 0 else 200
        # 3 đá liên tiếp
        elif count == 3:
            if blocks == 0:
                # Không bị chặn bên nào.
				# Nếu là lượt của người chơi hiện tại, đảm bảo thắng trong 2 lượt tiếp theo.
				# (Người dùng đặt một viên đá khác để tạo thành tập hợp 4 liên tiếp, đối thủ chỉ có thể chặn một bên)
				# Tuy nhiên, đối thủ có thể thắng trò chơi trong lượt tiếp theo do đó điểm số này thấp hơn
				# điểm đảm bảo thắng nhưng vẫn rất cao.

				# Nếu là lượt của đối thủ, tập hợp này buộc đối thủ phải chặn một bên của tập hợp.
				# Vì vậy, điểm số tương đối cao được đưa ra cho tập hợp này.
                return 50_000 if current_turn else 200
            else:
                #  Một bên bị chặn.
			    # Điểm số tạo cơ hội
                return 10 if current_turn else 5
        # 2 đá liên tiếp
		# Điểm số tạo cơ hội
        elif count == 2:
            return 7 if blocks == 0 and current_turn else 5 if blocks == 0 else 3
        elif count == 1:
            return 1
        # Nhiều hơn 5 đá liên tiếp?
        return Minimax.WIN_SCORE * 2
