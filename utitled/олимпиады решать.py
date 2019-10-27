# 1
# a = int(input())-int(input())+int(input())
# a = a-24 if a >= 24 else a+24 if a < 0 else a
# print(a)

# 2
# first, last = int(input()), int(input())
# chet_first, chet_last = first+(first % 2), last-(last % 2)
# len_chet = (chet_last-chet_first)//2+1
# sum_chet = len_chet*(chet_last+chet_first)//2
# ne_chet_first, ne_chet_last = first+1-(first % 2), last-1+(last % 2)
# len_ne_chet = (ne_chet_last-ne_chet_first)//2+1
# sum_ne_chet = len_ne_chet*(ne_chet_last+ne_chet_first)//2
# print(sum_chet-sum_ne_chet)

# 3
# a, b, i = int(input()), int(input()), 1
# maximum = (a+b+abs(a-b))//2
# if a == maximum:
#     while (a*i+1) % b != b-1:
#         i += 1
#     print(a*i+1)
# else:
#     while (b*i-1) % a != 1:
#         i += 1
#     print(b*i-1)

# 4
# a = list(input())
# N = len(a)
# i = -1
# answer = -1
# was = False
# while i != (N-1)//2:
#     i += 1
#     if a[i] != a[-1-i]:
#         if not was:
#             if i == 0:
#                 if a[1] == a[-1]:
#                     answer = 1
#                 elif a[0] == a[-2]:
#                     answer = N
#                 else:
#                     print(0)
#                     break
#             else:
#                 if a[i+1] == a[-1-i]:
#                     answer = i+1
#                 elif a[i] == a[-2-i]:
#                     answer = N-i
#                 else:
#                     print(0)
#                     break
#             if answer != -1:
#                 a.pop(answer-1)
#                 was = True
#         else:
#             print(0)
#             break
# else:
#     print(answer)