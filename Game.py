from Minimax import *

class Game:
    board = None
    isPlayersTurn = True
    gameFinished = False
    minimaxDepth = 4
    aiStarts = True # AI makes the first move
    ai = None
    cacheFile = "score_cache.ser"
    winner = 0 # 0: There is no winner yet, 1: AI Wins, 2: Human Wins, 3: Draw
    
    def __init__(self, board):
        self.board = board
        self.ai = Minimax(board)
        self.winner = 0
        
    def start(self):
        # If the AI is making the first move, place a white stone in the middle of the board.
        if self.aiStarts:
            self.playMove(self.board.get_board_size()//2, self.board.get_board_size()//2, False)
            self.isPlayersTurn = True
        # Now it's human player's turn.
        else:
            print("Your move is ?: ")
            posX = input("Index of the row: ")
            posY = input("Index of the column: ")
            self.playMove(posX, posY, True)
            self.isPlayersTurn = False
        
    # Sets the depth of the minimax tree. (i.e. how many moves ahead should the AI calculate.
    def setAIDepth(self, depth):
        self.minimaxDepth = depth
    
    def setAIStarts(self, aiStarts):
        self.aiStarts = aiStarts
        
    def run(self):
        self.start()
        self.board.printBoard()
        while not self.gameFinished:
            if self.isPlayersTurn:
                print("Your move is ?: ")
                posX = int(input("Index of the row: "))
                posY = int(input("Index of the column: "))
                self.playMove(posX, posY, True)
                self.isPlayersTurn = False
            else:
                print("AI is thinking...")
                
                # Make the AI instance calculate a move.
                aiMove = self.ai.calculate_next_move(self.minimaxDepth)
                print(aiMove)
                if (aiMove == None):
                    print("No possible moves left. Game Over.")
                    self.gameFinished = True
                    return
                
                self.playMove(aiMove[1], aiMove[0], False)
                print("Black: ", Minimax.get_score(self.board,True,True), " White: ",  Minimax.get_score(self.board,False,True))
                self.isPlayersTurn = True
            self.board.printBoard()
            self.checkWinner()
        
    
    def checkWinner(self):
        if (Minimax.get_score(self.board, True, False) >= Minimax.get_win_score()):
            return 2
        if (Minimax.get_score(self.board, False, True) >= Minimax.get_win_score()):
            return 1
        return 0
    
    def playMove(self, posX, posY, black):
        return self.board.add_stone(posX, posY, black)
    