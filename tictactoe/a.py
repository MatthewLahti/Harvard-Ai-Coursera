def minimax_aux(board,max_score):
    if max_score:
        v = -2
    else:
        v = 2
    best_action = None
    for action in actions(board):
        ..........