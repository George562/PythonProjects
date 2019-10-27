x, y, z = input().split()
rez = int(x)-int(y)
if rez == 0:
    print('0' if z == '0' else '?')
if rez > 0:
    print('+' if int(z) < rez else '?')
if rez < 0:
    print('-' if int(z) < -rez else '?')
