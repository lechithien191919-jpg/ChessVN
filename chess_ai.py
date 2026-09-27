import random

VALUE = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}
KN = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
DIRB = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
DIRR = [(1, 0), (-1, 0), (0, 1), (0, -1)]

PST = {
    'P': [0,0,0,0,0,0,0,0, 50,50,50,50,50,50,50,50, 10,10,20,30,30,20,10,10, 5,5,10,25,25,10,5,5, 0,0,0,20,20,0,0,0, 5,-5,-10,0,0,-10,-5,5, 5,10,10,-20,-20,10,10,5, 0,0,0,0,0,0,0,0],
    'N': [-50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,0,0,0,-20,-40, -30,0,10,15,15,10,0,-30, -30,5,15,20,20,15,5,-30, -30,0,15,20,20,15,0,-30, -30,5,10,15,15,10,5,-30, -40,-20,0,5,5,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50],
    'B': [-20,-10,-10,-10,-10,-10,-10,-20, -10,0,0,0,0,0,0,-10, -10,0,5,10,10,5,0,-10, -10,5,5,10,10,5,5,-10, -10,0,10,10,10,10,10,0, -10,10,10,10,10,10,10,-10, -10,5,0,5,5,0,5,-10, -20,-10,-10,-10,-10,-10,-10,-20],
    'R': [0,0,0,0,0,0,0,0, 5,10,10,10,10,10,10,5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, 0,0,0,5,5,0,0,0, 0,0,0,0,0,0,0,0],
    'Q': [-20,-10,-10,-5,-5,-10,-10,-20, -10,0,0,0,0,0,0,-10, -10,0,5,5,5,5,0,-10, -5,0,5,5,5,5,0,-5, 0,0,5,5,5,5,0,-5, -10,5,5,5,5,5,0,-10, -10,0,5,0,0,0,0,-10, -20,-10,-10,-5,-5,-10,-10,-20],
    'K': [-30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10, 20,20,0,0,0,0,20,20, 20,30,10,0,0,10,30,20]
}

def col(p):
    if not p: return None
    return 'w' if p.isupper() else 'b'

def opp(c): return 'b' if c == 'w' else 'w'
def inside(r, c): return 0 <= r < 8 and 0 <= c < 8
def clone_board(b): return [row[:] for row in b]

def king_pos(b, c):
    k_char = 'K' if c == 'w' else 'k'
    for r in range(8):
        for x in range(8):
            if b[r][x] == k_char: return [r, x]
    return None

def attacked(b, r, c, by):
    for rr in range(8):
        for cc in range(8):
            p = b[rr][cc]
            if not p or col(p) != by: continue
            t = p.upper()
            dr, dc = r - rr, c - cc
            if t == 'P' and dr == (-1 if by == 'w' else 1) and abs(dc) == 1: return True
            if t == 'N' and [dr, dc] in KN: return True
            if t == 'K' and max(abs(dr), abs(dc)) == 1: return True
            dirs = DIRB if t == 'B' else (DIRR if t == 'R' else (DIRB + DIRR if t == 'Q' else None))
            if dirs:
                for sr, sc in dirs:
                    a, d = rr + sr, cc + sc
                    while inside(a, d):
                        if a == r and d == c: return True
                        if b[a][d]: break
                        a += sr; d += sc
    return False

def check(b, c):
    k = king_pos(b, c)
    return not k or attacked(b, k[0], k[1], opp(c))

def pseudo(b, r, c, co, castle, ep):
    p = b[r][c]
    if not p or col(p) != co: return []
    t = p.upper()
    out = []
    if t == 'P':
        d = -1 if co == 'w' else 1
        start = 6 if co == 'w' else 1
        if inside(r + d, c) and not b[r + d][c]:
            out.append([r + d, c])
            if r == start and not b[r + 2 * d][c]: out.append([r + 2 * d, c])
        for dc in [-1, 1]:
            rr, cc = r + d, c + dc
            if inside(rr, cc):
                if b[rr][cc] and col(b[rr][cc]) != co and b[rr][cc].upper() != 'K': out.append([rr, cc])
                if ep and ep == [rr, cc]: out.append([rr, cc])
    elif t == 'N':
        for dr, dc in KN:
            rr, cc = r + dr, c + dc
            if inside(rr, cc) and col(b[rr][cc]) != co and (b[rr][cc] is None or b[rr][cc].upper() != 'K'):
                out.append([rr, cc])
    elif t in ['B', 'R', 'Q']:
        dirs = DIRB if t == 'B' else (DIRR if t == 'R' else DIRB + DIRR)
        for dr, dc in dirs:
            rr, cc = r + dr, c + dc
            while inside(rr, cc):
                if not b[rr][cc]:
                    out.append([rr, cc])
                else:
                    if col(b[rr][cc]) != co and b[rr][cc].upper() != 'K': out.append([rr, cc])
                    break
                rr += dr; cc += dc
    elif t == 'K':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if not dr and not dc: continue
                rr, cc = r + dr, c + dc
                if inside(rr, cc) and col(b[rr][cc]) != co and (b[rr][cc] is None or b[rr][cc].upper() != 'K'):
                    out.append([rr, cc])
        # Nhập thành
        row = 7 if co == 'w' else 0
        king_side = 'K' if co == 'w' else 'k'
        queen_side = 'Q' if co == 'w' else 'q'
        enemy = opp(co)
        if r == row and c == 4 and not check(b, co):
            if castle.get(king_side) and not b[row][5] and not b[row][6] and not attacked(b, row, 5, enemy) and not attacked(b, row, 6, enemy):
                out.append([row, 6])
            if castle.get(queen_side) and not b[row][1] and not b[row][2] and not b[row][3] and not attacked(b, row, 3, enemy) and not attacked(b, row, 2, enemy):
                out.append([row, 2])
    return out

def apply_move(b, r, c, rr, cc, co, castle, ep, promo):
    nb = clone_board(b)
    p = nb[r][c]
    t = p.upper()
    dest = nb[rr][cc]
    nb[r][c] = None
    nb[rr][cc] = (promo if promo else p) if co == 'w' else (promo.lower() if promo else p.toLowerCase() if hasattr(p, 'toLowerCase') else p.lower())
    
    nep = None
    ncast = dict(castle)
    if t == 'P' and ep and [rr, cc] == ep and not dest:
        nb[rr + (1 if co == 'w' else -1)][cc] = None
    if t == 'P' and abs(rr - r) == 2:
        nep = [(r + rr) // 2, c]
    if t == 'K':
        ncast[ 'K' if co == 'w' else 'k' ] = False
        ncast[ 'Q' if co == 'w' else 'q' ] = False
        if abs(cc - c) == 2:
            rc = 7 if cc > c else 0
            tc = 5 if cc > c else 3
            nb[rr][tc] = nb[rr][rc]
            nb[rr][rc] = None
    if t == 'R':
        if r == 7 and c == 0: ncast['Q'] = False
        if r == 7 and c == 7: ncast['K'] = False
        if r == 0 and c == 0: ncast['q'] = False
        if r == 0 and c == 7: ncast['k'] = False
    return {'board': nb, 'castle': ncast, 'ep': nep}

def legal_moves(b, r, c, co, castle, ep):
    p = b[r][c]
    if not p or col(p) != co: return []
    out = []
    for rr, cc in pseudo(b, r, c, co, castle, ep):
        z = apply_move(b, r, c, rr, cc, co, castle, ep, None)
        if not check(z['board'], co): out.append([rr, cc])
    return out

def all_moves(b, co, castle, ep):
    a = []
    for r in range(8):
        for c in range(8):
            if col(b[r][c]) == co:
                for rr, cc in legal_moves(b, r, c, co, castle, ep):
                    a.append([r, c, rr, cc])
    return a

def evaluate(b):
    score = 0
    for r in range(8):
        for c in range(8):
            p = b[r][c]
            if not p: continue
            t = p.upper()
            v = VALUE[t]
            pst_row = r if p.isupper() else (7 - r)
            bonus = PST[t][pst_row * 8 + c] if t in PST else 0
            score += (1 if p.isupper() else -1) * (v + bonus)
    return score

def order_moves(b, moves):
    return sorted(moves, key=lambda m: (VALUE[b[m[2]][m[3]].upper()] if b[m[2]][m[3]] else 0), reverse=True)

def minimax(b, co, depth, alpha, beta, castle, ep):
    moves = all_moves(b, co, castle, ep)
    if depth == 0 or not moves:
        if not moves:
            return -99999 if check(b, co) else 0
        return evaluate(b)
    
    moves = order_moves(b, moves)
    if co == 'b':
        best = -float('inf')
        for m in moves:
            promo = 'Q' if b[m[0]][m[1]].upper() == 'P' and m[2] == 0 else None
            z = apply_move(b, m[0], m[1], m[2], m[3], co, castle, ep, promo)
            v = minimax(z['board'], 'w', depth - 1, alpha, beta, z['castle'], z['ep'])
            best = max(best, v)
            alpha = max(alpha, v)
            if beta <= alpha: break
        return best
    else:
        best = float('inf')
        for m in moves:
            promo = 'Q' if b[m[0]][m[1]].upper() == 'P' and m[2] == 7 else None
            z = apply_move(b, m[0], m[1], m[2], m[3], co, castle, ep, promo)
            v = minimax(z['board'], 'b', depth - 1, alpha, beta, z['castle'], z['ep'])
            best = min(best, v)
            beta = min(beta, v)
            if beta <= alpha: break
        return best

def get_ai_move(board, level, castle, ep):
    depth = 1 if level == 1 else (2 if level == 2 else (3 if level == 3 else 4))
    moves = all_moves(board, 'b', castle, ep)
    if not moves: return None
    
    # Kho khai cuộc đơn giản cho máy (nếu ở nước đầu)
    if len(moves) > 25 and level >= 3:
        common_openings = [[[1, 4, 3, 4], [1, 3, 3, 3], [1, 6, 2, 5]]]
        valid_openings = [m for m in common_openings[0] if m in moves]
        if valid_openings and random.random() < 0.6:
            m = random.choice(valid_openings)
            return {'from': [m[0], m[1]], 'to': [m[2], m[3]], 'promo': 'q'}

    moves = order_moves(board, moves)
    best_move = moves[0]
    best_v = -float('inf')
    
    for m in moves:
        promo = 'q' if board[m[0]][m[1]].upper() == 'P' and m[2] == 0 else None
        z = apply_move(board, m[0], m[1], m[2], m[3], 'b', castle, ep, promo)
        v = minimax(z['board'], 'w', depth - 1, -float('inf'), float('inf'), z['castle'], z['ep'])
        if v > best_v:
            best_v = v
            best_move = m
            
    promo_char = 'q' if board[best_move[0]][best_move[1]].upper() == 'P' and best_move[2] == 0 else None
    return {'from': [best_move[0], best_move[1]], 'to': [best_move[2], best_move[3]], 'promo': promo_char}

