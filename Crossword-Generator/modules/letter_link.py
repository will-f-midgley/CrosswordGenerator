import random as r
import copy


def initial_add(word, grid):
    for i in range(0, len(word)):
        grid[13][13 + i] = word[i]
    start = [403, len(word), "across"]
    return grid, start


def grid_add(word, grid):
    counter = 0
    checked = False
    added = False
    while not added:
        split = r.randint(0, len(word) - 1)
        letter = word[split]
        counter = counter + 1
        for row in grid:
            for element in row:
                if element == letter:
                    position = grid.index(row), row.index(element)
                    pre, post = word[0:split], word[split:len(word)]

                    pre = pre[::-1]
                    oldgrid = copy.deepcopy(grid)

                    newgrid, checked = vertical_check(oldgrid, position, pre, post)
                    direction = "across"
                    startPos = position[0], position[1] - len(pre)

                    if checked == False:
                        oldgrid = copy.deepcopy(grid)
                        newgrid, checked = horizontal_check(oldgrid, position, pre, post)
                        direction = "down"
                        startPos = position[0] - len(pre), position[1]

                    if checked == True:
                        grid = newgrid
                        start = direction + str(startPos)
                        start = [startPos[0] * 30 + startPos[1], len(word), direction]
                        return newgrid, checked, start
        if counter == 100:
            newgrid = "null"
            start = "null"
            checked = False
            return newgrid, checked, start

    return grid, wordDetails


def horizontal_check(grid, position, pre, post):
    newgrid = grid
    horizontal = True

    if len(pre) > position[0] or len(post) + position[0] > 29:
        horizontal = False

    for i in range(len(pre)):

        if ((grid[position[0] - i - 1][position[1]] != "*" and (
                grid[position[0] - i - 1][position[1] + 1] != "*" or grid[position[0] - i - 1][
            position[1] - 1] != "*")) and grid[position[0] - i - 1][position[1]] != pre[i]):
            horizontal = False

        newgrid[position[0] - i - 1][position[1]] = pre[i]
    for j in range(len(post)):
        try:
            if not ((grid[position[0] + j][position[1]] == post[j]) or (grid[position[0] + j][position[1]] == "*" and (
                    grid[position[0] + j][position[1] + 1] == "*" and grid[position[0] + j][
                position[1] - 1] == "*"))):
                horizontal = False

        except:
            horizontal = False
        try:
            newgrid[position[0] + j][position[1]] = post[j]
        except:
            horizontal = False
    try:
        if grid[position[0] - len(pre) - 1][position[1]] != "*" or grid[position[0] + len(post)][position[1]] != "*":
            horizontal = False

    except:
        horizontal = False
    return newgrid, horizontal


def vertical_check(grid, position, pre, post):
    newgrid = grid
    vertical = True

    for i in range(len(pre)):

        if ((grid[position[0]][position[1] - i - 1] != "*" and (
                grid[position[0] + 1][position[1] - i - 1] != "*" or grid[position[0] - 1][
            position[1] - i - 1] != "*")) and grid[position[0]][position[1] - i - 1] != pre[i]):
            vertical = False

        newgrid[position[0]][position[1] - i - 1] = pre[i]
    for j in range(len(post)):
        try:
            if not ((grid[position[0]][position[1] + j] == post[j]) or (grid[position[0]][position[1] + j] == "*" and (
                    grid[position[0] + 1][position[1] + j] == "*" and grid[position[0] - 1][
                position[1] + j] == "*"))):
                vertical = False

        except:
            vertical = False
        try:
            newgrid[position[0]][position[1] + j] = post[j]
        except:
            vertical = False

    try:
        if grid[position[0]][position[1] - len(pre) - 1] != "*" or grid[position[0]][position[1] + len(post)] != "*":
            vertical = False
    except:
        vertical = False

    if vertical:

        return newgrid, vertical
    else:
        return "no", vertical


def letter_link(words):
    grid = []
    for k in range(30):
        grid.append(["*"] * 30)
    grid, start = initial_add(words[0][0], grid)
    start.append(words[0][1])
    directions = [start]
    for i in range(1, len(words)):
        checked = False
        k = 0
        while not checked:

            newgrid, checked, start = grid_add(words[i][0], grid)
            if not checked:
                words.append(words.pop(i))
                k = k + 1
                if k > len(words):
                    break
        if checked:
            grid = newgrid
            start.append(words[i][1])
            directions.append(start)

    # [[403,7,"across","A big black primate"],[492,3,"across","funny lads who swing"]]

    directionsdown = []
    directionsacross = []
    for i in directions:
        if i[2] == "across":
            directionsacross.append(i)
        else:
            directionsdown.append(i)

    return grid, directionsdown, directionsacross
