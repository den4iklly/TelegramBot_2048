from random import randint


def CanMove(values):
    for row in values:
        if ' ' in row:
            return True
    for i in range(len(values)):
        for j in range(len(values[0])):
            if j < len(values[0]) - 1 and values[i][j] == values[i][j + 1]:
                return True
            if i < len(values) - 1 and values[i][j] == values[i + 1][j]:
                return True
    return False


def CheckWin(values):
    for row in values:
        if '2048' in row:
            return True
    return False


def CreateMap(size):
    rows, cols = size
    values = [[' ' for c in range(cols)] for r in range(rows)]
    return values


def AddTile(values, tile_counts):
    for tile in range(tile_counts):
        empty_tile = False
        for row in range(len(values)):
            if ' ' in values[row]:
                empty_tile = True
                break
        if empty_tile:
            while True:
                rnd_row, rnd_col = randint(0, len(values) - 1), randint(0, len(values[0]) - 1)
                if values[rnd_row][rnd_col] != ' ':
                    continue
                if randint(1, 100) <= 90:
                    values[rnd_row][rnd_col] = '2'
                    break
                else:
                    values[rnd_row][rnd_col] = '4'
                    break
    return values


def DrawMap(game_map, values):
    format_values = [item.rjust(4) for row in values for item in row]
    drawn_map = game_map.format(*format_values)
    return drawn_map


def MoveTiles(direction, values):
    changed = False

    if direction == "left":
        for row in values:
            new_row = [col for col in row if col != ' ']
            merged_row = []
            skip = False
            for i in range(len(new_row)):
                if skip:
                    skip = False
                    continue
                if i < len(new_row) - 1 and new_row[i] == new_row[i + 1]:
                    merged_row.append(str(int(new_row[i]) * 2))
                    skip = True
                    changed = True
                else:
                    merged_row.append(new_row[i])
            merged_row += [' '] * (len(row) - len(merged_row))
            if merged_row != row:
                changed = True
            row[:] = merged_row

    elif direction == "right":
        for row in values:
            new_row = [col for col in row if col != ' ']
            merged_row = []
            skip = False
            for i in range(len(new_row) - 1, -1, -1):
                if skip:
                    skip = False
                    continue
                if i > 0 and new_row[i] == new_row[i - 1]:
                    merged_row.append(str(int(new_row[i]) * 2))
                    skip = True
                    changed = True
                else:
                    merged_row.append(new_row[i])
            merged_row = [' '] * (len(row) - len(merged_row)) + merged_row[::-1]
            if merged_row != row:
                changed = True
            row[:] = merged_row

    elif direction == "up":
        for col in range(len(values[0])):
            new_col = [values[row][col] for row in range(len(values)) if values[row][col] != ' ']
            merged_col = []
            skip = False
            for i in range(len(new_col)):
                if skip:
                    skip = False
                    continue
                if i < len(new_col) - 1 and new_col[i] == new_col[i + 1]:
                    merged_col.append(str(int(new_col[i]) * 2))
                    skip = True
                    changed = True
                else:
                    merged_col.append(new_col[i])
            merged_col += [' '] * (len(values) - len(merged_col))
            for i in range(len(values)):
                if values[i][col] != merged_col[i]:
                    changed = True
                values[i][col] = merged_col[i]

    elif direction == "down":
        for col in range(len(values[0])):
            new_col = [values[row][col] for row in range(len(values)) if values[row][col] != ' ']
            merged_col = []
            skip = False
            for i in range(len(new_col) - 1, -1, -1):
                if skip:
                    skip = False
                    continue
                if i > 0 and new_col[i] == new_col[i - 1]:
                    merged_col.append(str(int(new_col[i]) * 2))
                    skip = True
                    changed = True
                else:
                    merged_col.append(new_col[i])
            merged_col = [' '] * (len(values) - len(merged_col)) + merged_col[::-1]
            for i in range(len(values)):
                if values[i][col] != merged_col[i]:
                    changed = True
                values[i][col] = merged_col[i]
    return values, changed


def main():
    size = (int(n) for n in input("Введите размеры (4 4): ").split())
    game_map, values = CreateMap(size)
    values = AddTile(values, 2)
    while True:
        print(DrawMap(game_map, values))
        if CheckWin(values):
            print("Вы победили!")
        if CanMove(values):
            while True:
                direction = input("Введите направление: ").lower()
                if direction in ['left', 'right', 'up', 'down']:
                    values, changed = MoveTiles(direction, values)
                    break
                else:
                    print("Введено некорректное направление")
            if changed:
                values = AddTile(values, 1)
        else:
            print("Вы проиграли!")
            break


if __name__ == "__main__":
    main()