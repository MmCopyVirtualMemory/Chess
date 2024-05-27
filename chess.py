class fen_t:
    def __init__(self, fen_string:str):
        position, turn, castling, enpassant, halfmove, fullmove = fen_string.split()
        self.position = position
        self.turn = turn
        self.castling = castling
        self.enpassant = enpassant
        self.halfmove = int(halfmove)
        self.fullmove = int(fullmove)
    def __str__(self):
        return self.position + " " + self.turn + " " + self.castling + " " + self.enpassant + " " + str(self.halfmove) + " " + str(self.fullmove)
def position_to_board(position):
    for num in range(1, 9):
        str_num = str(num)
        while position.find(str_num) != -1:
            replacement_string = ""
            for i in range(num):
                replacement_string += " "
            position = position.replace(str_num, replacement_string)
    return position.split("/")
def board_to_position(board):
    position = ""
    for row in board:
        position += row + "/"
    position = position[:-1]
    for num in range(8, 0, -1):
        space_string = ""
        for i in range(num):
            space_string += " "
        while position.find(space_string) != -1:
            position = position.replace(space_string, str(len(space_string)))
    return position
def move_to_board_coord(chess_move):
    return [8 - int(chess_move[1]), ord(chess_move[0]) - ord('a')]
def board_coord_to_move(coord):
    return chr(ord('a') + coord[1]) + str(8 - coord[0])
def get_move(old_position, new_position):
    board1 = position_to_board(old_position)
    board2 = position_to_board(new_position)
    differences = []
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if board1[i][j] != board2[i][j]:
                differences.append((i, j))
    from_square = to_square = moved_piece = taken_piece = " "
    #normal move
    if len(differences) == 2: 
        for difference in differences:
            i, j = difference
            if board2[i][j] == " ":
                from_square = board_coord_to_move((i,j))
                moved_piece = board1[i][j]
            else:
                to_square = board_coord_to_move((i,j))
                taken_piece = board1[i][j]
    #castle
    elif len(differences) == 4: 
        for difference in differences:
            i, j = difference
            if board1[i][j].lower() != "k" and board2[i][j].lower() != "k":
                continue

            if board2[i][j] == " ":
                from_square = board_coord_to_move((i,j))
                moved_piece = board1[i][j]
            else:
                to_square = board_coord_to_move((i,j))
                taken_piece = board1[i][j]
    #enpassant
    elif len(differences) == 3:
        #perhaps rewrite this; couldn't think of a better way at the time
        for difference in differences:
            i, j = difference
            if board2[i][j] != " ":
                to_square = board_coord_to_move((i,j))
                moved_piece = board2[i][j]
        #determine which remaining square is which
        for difference in differences:
            i, j = difference
            if board2[i][j] == " ":
                #different files
                if move_to_board_coord(to_square)[1] == j:
                    from_square = board_coord_to_move((i,j))
                #same file
                else:
                    taken_piece = board1[i][j]
    #not consecutive moves??
    else:
        pass
    return [from_square, to_square, moved_piece, taken_piece]
def get_new_fen(fen_string, new_position):
    fen = fen_t(fen_string)
    from_square, to_square, moved_piece, taken_piece = get_move(fen.position, new_position)
    #handle turn
    new_turn = "w"
    if fen.turn == "w":
        new_turn = "b"
    #handle castling
    new_castling = fen.castling
    #no queenside castle for white
    if from_square == "a1" or to_square == "a1":
        new_castling = new_castling.replace("Q", "")
    #no kingside castle for white
    if from_square == "h1" or to_square == "h1":
        new_castling = new_castling.replace("K", "")
    #no queenside castle for black
    if from_square == "a8" or to_square == "a8":
        new_castling = new_castling.replace("q", "")
    #no kingside castle for black
    if from_square == "h8" or to_square == "h8":
        new_castling = new_castling.replace("k", "")
    #white king moved
    if moved_piece == "K":
        new_castling = new_castling.replace("K", "").replace("Q", "")
    #black king moved
    if moved_piece == "k":
        new_castling = new_castling.replace("k", "").replace("q", "")
    #put castling back in proper fen
    if new_castling == "":
        new_castling = "-"
    #handle enpassant
    new_enpassant = "-"
    i1 = int(from_square[1])
    i2 = int(to_square[1])
    #if the piece moved is a pawn and it's moved up 2
    if moved_piece.lower() == "p" and abs(i2 - i1) == 2: 
        #set enpassant legal
        new_enpassant = from_square[0] + str(int((i2 + i1) / 2))
    #handle halfmove
    new_halfmove = fen.halfmove + 1
    if moved_piece.lower() == "p" or taken_piece != " ":
        new_halfmove = 0
    #handle fullmove
    new_fullmove = fen.fullmove
    if fen.turn == "b":
        new_fullmove = new_fullmove + 1
    return str(new_position + " " + new_turn + " " + new_castling + " " + new_enpassant + " " + str(new_halfmove) + " " + str(new_fullmove))
def guess_fen(position, turn):
    if position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR":
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = position_to_board(position)
    castling = ""
    a, b = move_to_board_coord("e1")
    if board[a][b] == "K":
        i, j = move_to_board_coord("h1")
        if board[i][j] == "R":
            castling += "K"
        k, l = move_to_board_coord("a1")
        if board[k][l] == "R":
            castling += "Q"
    c, d = move_to_board_coord("e8")
    if board[c][d] == "k":
        m, n = move_to_board_coord("h8")
        if board[m][n] == "r":
            castling += "k"
        o, p = move_to_board_coord("a8")
        if board[o][p] == "r":
            castling += "q"
    if castling == "":
        castling = "-"
    return str(position + " " + turn + " " + castling + " - 0 1")