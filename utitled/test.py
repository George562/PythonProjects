# def zoomer(arr: list, param, center: list):
#     x, y = center
#     a = []
#     for i in range(len(arr)):
#         a.append([(arr[i][0]-x)*param+x, (arr[i][1]-y)*param+y])
#     return a


# def polygon(seq, n, k=-1, arr=None):
#     if len(seq) < n:
#         raise Exception('sequence length does not allow %s-object permutation' % n)
#     if n == 0:
#         print(*arr)
#         return
#     arr = arr or []
#     for i in range(k+1, len(seq)-n+1):
#         polygon(seq, n-1, i, arr+[seq[i]])


# def calc_rect(dots: list):
#     n = len(dots)
#     ans = 0
#     k = 0
#     for j in range(1, n-2):
#         k += j+((j-1)*j)//2
#         ans += k
#     print(ans)
#     rects = []
#     for a in range(n-3):  # берем последний элемент и вставляем на 2-е место (двигаем последовательность)
#         for b in range(a+1, n-2):
#             for c in range(b+1, n-1):
#                 for d in range(c+1, n):
#                     rects += [[dots[a], dots[b], dots[c], dots[d]]]
#     print(*rects)


# # polygon([[int(i) for i in input().split()] for j in range(int(input()))], 4)
# polygon([1, 2, 3, 4], 2)
# input()

# import pygame
# win = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# dots = [[x*10, y*10] for x in range(1, 30) for y in range(1, 30)]
# f_dots = dots.copy()
# for dot in f_dots:
#     pygame.draw.circle(win, (255, 255, 255), dot, 5)
# pygame.display.flip()
# done = False
# zoom = 1
# ch_zoom = 0.2
# while not done:
#     win.fill((0, 0, 0))
#     for e in pygame.event.get():
#         if e.type == pygame.KEYDOWN:
#             if e.key == pygame.K_ESCAPE:
#                 done = True
#         if e.type == pygame.MOUSEBUTTONDOWN:
#             if 4 <= e.button <= 5:
#                 pos = pygame.mouse.get_pos()
#                 if e.button == 4:  # up
#                     f_dots = zoomer(f_dots, 1+ch_zoom, pos)
#                     zoom *= 1+ch_zoom
#                 elif e.button == 5 and zoom > 1:  # down
#                     f_dots = zoomer(f_dots, 1/(1+ch_zoom), pos)
#                     zoom /= 1+ch_zoom
#                 for dot in f_dots:
#                     pygame.draw.circle(win, (255, 255, 255), [round(dot[0]), round(dot[1])], 5)
#                 pygame.display.flip()


def combin(seq, step=0, arr=None, self_list=None):
    self_list = []
    arr = arr or []
    if step == len(seq):
        return [arr]
    for j in 0, seq[step]:
        self_list += combin(seq, step+1, arr+[j])
    return self_list


end = combin([1, 2, 3])
print(*end, sep='\n')
input()
