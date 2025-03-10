import pygame as py
import chess

py.init()

width, height = 650, 650
rows, cols = 8, 8
square_size = width // 8
game_window = py.display.set_mode((width, height))
color_1 = (255, 255, 255)  # W
color_2 = (130, 130, 130)  # G
color_highlight = (255, 255, 0,100)  

move_sound = py.mixer.Sound('chessSound.wav')

board = chess.Board()

py.display.set_caption('Chess Game')
pieces = {
    'bishopW': py.image.load('chessphoto/bishopW.png'),
    'kingW': py.image.load('chessphoto/kingW.png'),
    'knightW': py.image.load('chessphoto/knightW.png'),
    'pawnW': py.image.load('chessphoto/pawnW.png'),
    'queenW': py.image.load('chessphoto/queenW.png'),
    'rookW': py.image.load('chessphoto/rookW.png'),
    'bishopB': py.image.load('chessphoto/bishopB.png'),
    'kingB': py.image.load('chessphoto/kingB.png'),
    'knightB': py.image.load('chessphoto/knightB.png'),
    'pawnB': py.image.load('chessphoto/pawnB.png'),
    'queenB': py.image.load('chessphoto/queenB.png'),
    'rookB': py.image.load('chessphoto/rookB.png'),
}
chess_Board = {
    (0,0): 'rookB', (1,0): 'knightB', (2,0): 'bishopB', (3,0): 'queenB',
    (4,0): 'kingB', (5,0): 'bishopB', (6,0): 'knightB', (7,0): 'rookB',
    (0,1): 'pawnB', (1,1): 'pawnB', (2,1): 'pawnB', (3,1): 'pawnB',
    (4,1): 'pawnB', (5,1): 'pawnB', (6,1): 'pawnB', (7,1): 'pawnB',
    (0,6): 'pawnW', (1,6): 'pawnW', (2,6): 'pawnW', (3,6): 'pawnW',
    (4,6): 'pawnW', (5,6): 'pawnW', (6,6): 'pawnW', (7,6): 'pawnW',
    (0,7): 'rookW', (1,7): 'knightW', (2,7): 'bishopW', (3,7): 'queenW',
    (4,7): 'kingW', (5,7): 'bishopW', (6,7): 'knightW', (7,7): 'rookW'
}

def print_board():
    for row in range(8):
        for col in range(8):
            color = color_1 if (row + col) % 2 == 0 else color_2
            py.draw.rect(game_window, color, (col * square_size, row * square_size, square_size, square_size))

def print_pieces():
    for (col, row), piece in chess_Board.items():
        game_window.blit(pieces[piece], (col * square_size + 10, row * square_size + 10))

def is_valid_turn(piece):
    return (current_turn == 'W' and piece.endswith('W')) or (current_turn == 'B' and piece.endswith('B'))

def pos_TO_NOTATION(pos):
    col, row = pos
    return col + (7 - row) * 8
def notation_to_pos(square):
    col = square % 8
    row = 7 - (square // 8)
    return (col, row)

def is_legal_move(from_pos, to_pos):
    from_sq = pos_TO_NOTATION(from_pos)
    to_sq = pos_TO_NOTATION(to_pos)  
    move = chess.Move(from_sq, to_sq)   #get next move in chess notation
    return move in board.legal_moves   #show if it legal in move list 
def get_legal_move(pos):#filter for highlight possible moves for only one piece 
    square=pos_TO_NOTATION(pos)
    legal_move=[]
    for move in board.legal_moves:
        if move.from_square==square:
            legal_move.append(notation_to_pos(move.to_square))
    return legal_move        
def highlight_square(pos):
    surface = py.Surface((square_size, square_size), py.SRCALPHA) 
    surface.fill(color_highlight)
    game_window.blit(surface, (pos[0] * square_size, pos[1] * square_size))
selected_piece = None
current_turn = 'W'  # Start W

running = True
while running:
    print_board()
    print_pieces()
    
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            x, y = py.mouse.get_pos()
            col = x // square_size
            row = y // square_size
            
            if selected_piece: 
               
                second_pos = (col, row)
                if second_pos != selected_piece and is_legal_move(selected_piece, second_pos):
                    py.mixer.Sound.play(move_sound)
                    piece = chess_Board[selected_piece]
                    if second_pos in chess_Board:  
                        del chess_Board[second_pos]   # eat piece
                    del chess_Board[selected_piece]
                    chess_Board[second_pos] = piece
                    board.push(chess.Move(pos_TO_NOTATION(selected_piece), pos_TO_NOTATION(second_pos)))
                    current_turn = 'B' if current_turn == 'W' else 'W'
                    print(f"Moved from {selected_piece} to {second_pos}, now {current_turn}'s turn")
                selected_piece = None
            elif (col, row) in chess_Board and is_valid_turn(chess_Board[(col, row)]):  # Select piec
                selected_piece = (col, row)
                print(f"Selected: {chess_Board[selected_piece]} at {selected_piece}")
    if selected_piece:
        highlight_square(selected_piece)
        legal_move= get_legal_move(selected_piece)
        for mov_pos in legal_move:
            highlight_square(mov_pos)
    py.display.flip()

py.quit()
