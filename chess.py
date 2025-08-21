board = [0]*64
piece = {0:" ", 1:"P", 2:"R", 3:"K", 4:"B", 5:"X", 6:"Q", 7:"P", 8:"R", 9:"K", 10:"B", 11:"X", 12:"Q"}
colors = ("\033[0m\b", "\033[31m\b", "\033[34m\b")
king_pos = [4, 60, True, True]
attackers = 0
attackers_pos = []
enps = []
casts = [0, 7, 56, 63]
g = [[], []]
def resetBoard():
    for i in range(8, 16):
        board[i] = 1
        board[63 - i] = 7
    for i in range(16, 46):
        board[i] = 0
    t1 = (0, 7, 1, 6, 2, 5, 3, 4, 56, 63, 57, 62, 58, 61, 59, 60)
    t2 = (2, 2, 3, 3, 4, 4, 6, 5, 8, 8, 9, 9, 10, 10, 12, 11)
    for i in range(16):
        board[t1[i]] = t2[i]
def displayBoard(p, q):
    for i in range(3 + int(int(49 - len(q)) / 2)):
        print(" ", end = "")
    print(q, end = "  ")
    graveyard(2)
    line()
    for i in range(8):
        print(i + 1, end = "  |  ")
        for j in range(8):
            index = (i * 8) + j
            if board[index] < 7:
                print(colors[1], piece.get(int(board[index])), colors[0], end = "  |  ")
            else:
                print(colors[2], piece.get(int(board[index])), colors[0], end = "  |  ")
        print("")
        line()
    print("      ", end = "")
    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for i in range(8):
        print(labels[i], end = "     ")
    print("")
    for i in range(3 + int(int(49 - len(p)) / 2)):
        print(" ", end = "")
    print(p, end = "  ")
    graveyard(1)
def valid(a, b, turn, king_pos):
    if turn:
        king = king_pos[1]
        ally = [7, 8, 9, 10, 11, 12]
    else:
        ally = [1, 2, 3, 4, 5, 6]
        king = king_pos[0]
    if (not board[a] in ally) or a == b or board[b] in ally or not board[a]:
        return False
    a_temp = board[a]
    b_temp = board[b]
    doing = False
    if a_temp == 7 and (b == a - 7 or b == a - 9) and not b_temp:
        c = b + 8
        c_temp = board[c]
        board[c] = 0
        doing = True
    if a_temp == 1 and (b == a + 7 or b == a + 9) and not b_temp:
        c = b - 8
        c_temp = board[c]
        board[c] = 0
        doing = True
    board[b] = board[a]
    board[a] = 0
    if (not (a_temp == 5 or a_temp == 11)) and isCheck(king, turn):
        board[a] = a_temp
        board[b] = b_temp
        if doing:
            board[c] = c_temp
        return False
    board[a] = a_temp
    board[b] = b_temp
    if doing:
        board[c] = c_temp
    line_from = int(a / 8)
    line_to = int(b / 8)
    dist = posi((a % 8) - (b % 8))
    same_line = line_from == line_to  
    match board[a]:
        case 1:
            if (not board[b] == 0) and (b == a + 8 or b == a + 16):
                return False
            if line_from == 1 and b == a + 16 and not board[a + 8]:
                enps.append([b, 0])
                return True
            if b == a + 8:
                return True
            if (not (ally.__contains__(board[b]) or board[b] == 0)) and (b == a + 7 or b == a + 9):
                if line_to == line_from +1:
                    return True
                return False
            l1 = [i[0] for i in enps]
            can_en = (b == a + 7 and a - 1 in l1) or (b == a + 9 and a + 1 in l1)
            if can_en:
                if b == a + 7:
                    board[a - 1] = 0
                else:
                    board[a + 1] = 0
                return True
        case 7:
            if (not board[b] == 0) and (b == a - 8 or b == a - 16):
                return False
            if line_from == 6 and b == a - 16 and not board[a - 8]:
                enps.append([b, 0])
                return True
            if b == a - 8:
                return True
            if (not (ally.__contains__(board[b]) or board[b] == 0)) and (b == a - 7 or b == a - 9):
                if line_to == line_from -1:
                    return True
                return False
            l1 = [i[0] for i in enps]
            can_en = (b == a - 7 and a + 1 in l1) or (b == a - 9 and a - 1 in l1)
            if can_en:
                if b == a - 7:
                    board[a + 1] = 0
                else:
                    board[a - 1] = 0
                return True
        case 2 | 8 | 4 | 10 | 6 | 12:
            road = path(a, b)
            if road:
                for i in road:
                    if board[i]:
                        return False
                isValid = True
            else:
                match board[a]:
                    case 4 | 10 | 6 | 12:
                        if dist == posi(line_from - line_to):
                            isValid = True
                    case 2 | 8 | 6 | 12:
                        if not (dist and posi(line_from - line_to)):
                            isValid = True
            if isValid:
                if board[a] == 2 or board[a] == 8:
                    if a in casts:
                        casts.remove(a)
                return True
            return False
        case 3 | 9:
            if dist == 2:
                if posi(line_from - line_to) == 1:
                    return True
            elif dist == 1:
                if posi(line_from - line_to) == 2:
                    return True
            return False
        case 5 | 11:
            p = posi(a - b) == 1
            r = posi(a - b) in range(7, 10)
            s = posi(line_from - line_to) == 1
            c = same_line and dist == 2 and not isCheck(king, turn)
            if (p and same_line) or (r and s):
                temp = board[a]
                board[a] = 0
                if isCheck(b, turn):
                    board[a] = temp
                    return False
                board[a] = temp
                if turn:
                    king_pos[1] = b
                    if king_pos[3]:
                        king_pos[3] = False
                else:
                    king_pos[0] = b
                    if king_pos[2]:
                        king_pos = False
                return True
            if c:
                if king_pos[turn + 2]:
                    if a == b - 2 and (63 in casts or 7 in casts):
                        if turn:
                            way = path(king, 63)
                            for i in way:
                                if board[i] or isCheck(i, turn):
                                    return False
                            board[63] = 0
                            board[61] = 8
                            return 2
                        else:
                            way = path(king, 7)
                            for i in way:
                                if board[i] or isCheck(i, turn):
                                    return False
                            board[7] = 0
                            board[5] = 2
                            return 2
                    if b == a - 2 and (0 in casts or 56 in casts):
                        if turn:
                            way = path(king, 56)
                            for i in way:
                                if board[i] or isCheck(i, turn):
                                    return False
                            board[56] = 0
                            board[59] = 8
                            return 2
                        else:
                            way = path(king, 0)
                            for i in way:
                                if board[i] or isCheck(i, turn):
                                    return False
                            board[0] = 0
                            board[3] = 2
                            return 2
            return False
def takeMove():
    temp = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8}
    while True:
        num0 = input("Enter position: ")
        num0 = num0.lower()
        if (num0.isalpha() or num0.isdecimal() or not len(num0) == 2 or not num0[0] in temp) and not num0 == "draw":
            print("Invalid move, try again.")
            continue
        if num0 == "draw":
            return 65
        num1 = temp.get(num0[0])
        num2 = int(num0[1])-1
        return ((num2 * 8) + num1 - 1)
def takeTurn(who):
    start = takeMove()
    if start == 65:
        if drawPrompt():
            return 2
        return False
    end = takeMove()
    a = valid(start, end, who, king_pos)
    if a:
        enPassant()
        if a == 2:
            king_pos[who] = end
            king_pos[who + 2] = not king_pos[who + 2]
        if board[start] == 7 and int(end / 8) == 0:
            genderBender(end, who)
        elif board[start] == 1 and int(end / 8) == 7:
            genderBender(end, who)
        else:
            if board[end] > 6:
                g[1].append(board[end])
            elif board[end] in range(1, 7):
                g[0].append(board[end])
            board[end] = board[start]
        board[start] = 0
        return True
    return False
def enPassant():
    for i in enps:
        i[1] += 1
        if i[1] == 2:
            enps.remove(i)
def genderBender(spot, turn):
    choice = 7
    if turn:
        options = (8, 9, 10, 12)
    else:
        options = (2, 3, 4, 6)
    while not choice in range(1, 5):
        print("1. Rook")
        print("2. Knight")
        print("3. Bishop")
        print("4. Queen")
        choice = int(input("Convert pawn to: "))
        if not choice in range(1, 5):
            print("Enter valid choice.")
            continue
        board[spot] = options[choice - 1]
def isCheck(pos, king, mode = 0):
    attackers_pos.clear()
    check = False
    if king:
        str_en = (2, 6)
        dia_en = (4, 6)
        kni = 3
        k = 5
    else:
        str_en = (8, 12)
        dia_en = (10, 12)
        kni = 9
        k = 11
    up = int(pos / 8)
    down = 7 - up
    left = pos % 8
    right = 7 - left
    for i in range(4):
        j = pos
        match i:
            case 0:
                val = (int((pos + 8) / 8) * 8) - 1
                while j < val:
                    j += 1
                    if board[j]:
                        if board[j] in str_en:
                            check = True
                            attackers_pos.append((board[j], j))
                        break
            case 1:
                val = int(pos / 8) * 8
                while j > val:
                    j -= 1
                    if board[j]:
                        if board[j] in str_en:
                            check = True
                            attackers_pos.append((board[j], j))
                        break
            case 2:
                while j > pos % 8:
                    j -= 8
                    if board[j]:
                        if board[j] in str_en:
                            check = True
                            attackers_pos.append((board[j], j))
                        break
            case 3:
                while j < 56 - (pos % 8):
                    j += 8
                    if board[j]:
                        if board[j] in str_en:
                            check = True
                            attackers_pos.append((board[j], j))
                        break
    for i in range(1, min(up, right) + 1):
        j = pos - (8 * i) + i
        if board[j]:
            if board[j] in dia_en:
                check = True
                attackers_pos.append((board[j], j))
            break
    for i in range(1, min(down, right) + 1):
        j = pos + (8 * i) + i
        if board[j]:
            if board[j] in dia_en:
                check = True
                attackers_pos.append((board[j], j))
            break
    for i in range(1, min(down, left) + 1):
        j = pos + (8 * i) - i
        if board[j]:
            if board[j] in dia_en:
                check = True
                attackers_pos.append((board[j], j))
            break
    for i in range(1, min(up, left) + 1):
        j = pos - (8 * i) - i
        if board[j]:
            if board[j] in dia_en:
                check = True
                attackers_pos.append((board[j], j))
            break
    if up > 1:
        if left:
            if board[pos - 17] == kni:
                check = True
                attackers_pos.append((board[pos - 17], pos - 17))
        if right:
            if board[pos - 15] == kni:
                check = True
                attackers_pos.append((board[pos - 15], pos - 15))
    if right > 1:
        if up:
            if board[pos - 6] == kni:
                check = True
                attackers_pos.append((board[pos - 6], pos - 6))
        if down:
            if board[pos + 10] == kni:
                check = True
                attackers_pos.append((board[pos + 10], pos + 10))
    if down > 1:
        if right:
            if board[pos + 17] == kni:
                check = True
                attackers_pos.append((board[pos + 17], pos + 17))
        if left:
            if board[pos + 15] == kni:
                check = True
                attackers_pos.append((board[pos + 15], pos + 15))
    if left > 1:
        if down:
            if board[pos + 6] == kni:
                check = True
                attackers_pos.append((board[pos + 6], pos + 6))
        if up:
            if board[pos - 10] == kni:
                check = True
                attackers_pos.append((board[pos - 10], pos - 10))
    if not mode:
        if board[pos] == 5 or board[pos] == 11:
            if king:
                if right and board[pos - 7] == 1:
                    check = True
                    attackers_pos.append((board[pos - 7], pos - 7))
                if left and board[pos - 9] == 1:
                    check = True
                    attackers_pos.append((board[pos - 9], pos - 9))
            else:
                if right and board[pos + 9] == 7:
                    check = True
                    attackers_pos.append((board[pos + 7], pos + 7))
                if left and board[pos + 7] == 7:
                    check = True
                    attackers_pos.append((board[pos + 9], pos + 9))
        if not mode == 3:
            step1 = squares(pos)
            if king_pos[not king] in step1:
                check = True
    else:
        if king:
            if up == 3 and board[pos - 16] == 1:
                board[pos - 16] = 0
                board[pos] = 1
                if isCheck(king_pos[0], not king):
                    board[pos - 16] = 1
                    board[pos] = 0
                    return False
                board[pos - 16] = 1
                board[pos] = 0
                return True
            if board[pos - 8] == 1:
                board[pos - 8] = 0
                board[pos] = 1
                if isCheck(king_pos[0], not king):
                    board[pos - 8] = 1
                    board[pos] = 0
                    return False
                board[pos - 8] = 1
                board[pos] = 0
                return True
        else:
            if down == 3 and board[pos + 16] == 7:
                board[pos + 16] = 0
                board[pos] = 7
                if isCheck(king_pos[1], not king):
                    board[pos + 16] = 7
                    board[pos] = 0
                    return False
                board[pos + 16] = 7
                board[pos] = 0
                return True
            if board[pos + 8] == 7:
                board[pos + 8] = 0
                board[pos] = 7
                if isCheck(king_pos[1], not king):
                    board[pos + 8] = 7
                    board[pos] = 0
                    return False
                board[pos + 8] = 7
                board[pos] = 0
                return True
    if check:
        return True
    return False
def isCheckmate(pos, king, atcks):
    all_en = []
    for i in enps:
        all_en.append(i[0])
    if atcks == 1 and attackers_pos[0][1] in all_en:
        pawn = attackers_pos[0][1]
        if board[pawn] == 1:
            a = board[pawn - 1] == 7 and int(pawn /8) == int((pawn - 1) / 8)
            b = board[pawn + 1] == 7 and int(pawn /8) == int((pawn + 1) / 8)
            if a or b:
                return False
        if board[pawn] == 7:
            a = board[pawn - 1] == 1 and int(pawn /8) == int((pawn - 1) / 8)
            b = board[pawn + 1] == 1 and int(pawn /8) == int((pawn + 1) / 8)
            if a or b:
                return False
    if atcks == 1:
        current = attackers_pos[0][1]
    if atcks == 1 and isCheck(attackers_pos[0][1], not king, 3):
        now = attackers_pos[0][1]
        temp1 = board[current]
        board[current] = 13
        temp2 = board[now]
        board[now] = 0
        if isCheck(pos, king):
            board[current] = temp1
            board[now] = temp2
            return True
        board[current] = temp1
        board[now] = temp2
        return False
    temp = board[pos]
    board[pos] = 0
    box = squares(pos)
    safe = False
    for spot in box:
        if (king and board[spot] < 7) or ((not king) and (board[spot] > 6) or board[spot] == 0):
            if not isCheck(spot, king):
                safe = True
                break
    board[pos] = temp
    if (not safe) and atcks > 1:
        return True
    if safe:
        return False
    temp = board[pos]
    board[pos] = 0
    if attackers_pos[0][0] in [2, 4, 6, 8, 10, 12]:
        road = path(pos, attackers_pos[0][1])
        if road:
            for i in road:
                if isCheck(i, not king, 1):
                    board[pos] = temp
                    return False
    board[pos] = temp
    return True
def play(p1, p2):
    w_turn = True
    ind = 1
    resetBoard()
    while 1:
        displayBoard(p1, p2)
        if w_turn:
            print(p1, "'s turn", sep = "")
        else:
            print(p2, "'s turn", sep = "")
        turn = takeTurn(w_turn)
        if turn:
            if turn == 2:
                print("Game drawn.")
                return
            w_turn = not w_turn
            ind = 1 - ind
            if isCheck(king_pos[ind], w_turn):
                attackers = len(attackers_pos)
                if isCheckmate(king_pos[ind], w_turn, attackers):
                    winner = not w_turn
                    break
    displayBoard(p1, p2)
    if winner:
        print(p1, "won.")
    else:
        print(p2, "won.")
def chess():
    choice = 'y'
    valids = ['y', 'n', 'Y', 'N']
    while not (choice == 'n' or choice == 'N'):
        if choice == 'Y' or choice == 'y':
            player1 = str(input("Player 1: "))
            player2 = str(input("Player 2: "))
            play(player1, player2)
        choice = str(input("Do you want to play again? Y/N: "))
        if not choice in valids:
            print("Enter a valid choice.")
def posi(num):
    if num < 0:
        return -num
    return num
def line():
    print("   ", end = "")
    for i in range(1, 10):   
        print('|', end = "")
        if i < 9:
            for j in range(5):
                print('-', end = "")
    print("")
def drawPrompt():
    choice = str(input("Accept the draw? y/n: "))
    valids = ['y', 'n', 'N', 'Y']
    while True:
        if choice in valids:
            if choice == 'y' or choice == 'Y':
                return True
            return
def path(a, b):
    line_from = int(a / 8)
    line_to = int(b / 8)
    dist = posi((a % 8) - (b % 8))
    st = line_from == line_to or not dist
    di = posi(line_from - line_to) == dist
    if not (st or di):
        return 0
    if di:
        if line_from > line_to:
            if a%8 > b%8:
                dir = 4
            else:
                dir = 1
        else:
            if a%8 > b%8:
                dir = 3
            else:
                dir = 2
        if dir % 2:
            diff = 7
        else:
            diff = 9
    way = []
    for i in range(1):
        if st:
            if line_from == line_to:
                for spot in range(min(a, b) + 1, max(a, b)):
                    way.append(spot)
                break
            for spot in range(min(a, b) + 8, max(a, b) - 7, 8):
                way.append(spot)
            break
        for spot in range(min(a, b) + diff, max(a, b) - diff, diff):
            way.append(spot)
        break
    return way
def graveyard(mode):
    g[0].sort()
    g[1].sort()
    match mode:
        case 1:
            for i in g[0]:
                print(colors[1], piece.get(i), colors[0], end = "  ")
        case 2:
            for i in g[1]:
                print(colors[2], piece.get(i), colors[0], end = "  ")
    print()
def squares(pos):
    up = int(pos / 8)
    down = 7 - up
    left = pos % 8
    right = 7 - left
    square = set({})
    if up:
        square.add(pos - 8)
        if left:
            square.add(pos - 9)
            square.add(pos - 1)
        if right:
            square.add(pos - 7)
            square.add(pos + 1)
    if down:
        square.add(pos + 8)
        if left:
            square.add(pos + 7)
            square.add(pos - 1)
        if right:
            square.add(pos + 9)
            square.add(pos + 1)
    return square
chess()
