def up(arr):
    s = 0
    for line in range(1, len(arr)):
        for num in range(len(arr[line])):
            if arr[line][num] != 0:
                for dl in range(line - 1, -1, -1):
                    if arr[dl][num] != 0:
                        if arr[dl][num] == arr[line][num]:
                            s += arr[dl][num]
                            arr[dl][num] *= 2
                            arr[line][num] = 0
                        elif dl + 1 != line:
                            arr[dl + 1][num], arr[line][num] = arr[line][num], 0
                        break
                    if arr[dl][num] == 0 and dl == 0:
                        arr[dl][num], arr[line][num] = arr[line][num], 0
    return s


def left(arr):
    s = 0
    for line in range(len(arr)):
        for num in range(1, len(arr[line])):
            if arr[line][num] != 0:
                for dn in range(num - 1, -1, -1):
                    if arr[line][dn] != 0:
                        if arr[line][dn] == arr[line][num]:
                            s += arr[line][dn]
                            arr[line][dn] *= 2
                            arr[line][num] = 0
                        elif dn + 1 != num:
                            arr[line][dn + 1], arr[line][num] = arr[line][num], 0
                        break
                    if arr[line][dn] == 0 and dn == 0:
                        arr[line][dn], arr[line][num] = arr[line][num], 0
    return s


def down(arr):
    s = 0
    for line in range(len(arr) - 2, -1, -1):
        for num in range(len(arr[line])):
            if arr[line][num] != 0:
                for dl in range(line + 1, len(arr)):
                    if arr[dl][num] != 0:
                        if arr[dl][num] == arr[line][num]:
                            s += arr[dl][num]
                            arr[dl][num] *= 2
                            arr[line][num] = 0
                        elif dl - 1 != line:
                            arr[dl - 1][num], arr[line][num] = arr[line][num], 0
                        break
                    if arr[dl][num] == 0 and dl == len(arr) - 1:
                        arr[dl][num], arr[line][num] = arr[line][num], 0
    return s


def right(arr):
    s = 0
    for line in range(len(arr)):
        for num in range(len(arr) - 2, -1, -1):
            if arr[line][num] != 0:
                for dn in range(num + 1, len(arr)):
                    if arr[line][dn] != 0:
                        if arr[line][dn] == arr[line][num]:
                            s += arr[line][dn]
                            arr[line][dn] *= 2
                            arr[line][num] = 0
                        elif dn - 1 != num:
                            arr[line][dn - 1], arr[line][num] = arr[line][num], 0
                        break
                    if arr[line][dn] == 0 and dn == len(arr) - 1:
                        arr[line][dn], arr[line][num] = arr[line][num], 0
    return s


place = [list(map(int, input().split())) for _ in range(4)]
a = up([[j for j in i] for i in place])
b = left([[j for j in i] for i in place])
c = down([[j for j in i] for i in place])
d = right([[j for j in i] for i in place])
print(max(a, b, c, d) * 2)
