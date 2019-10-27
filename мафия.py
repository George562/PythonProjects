import random
players = int(input('игроков: '))
man = 1 if players > 7 else 0
lub = 1 if players > 9 else 0
jur = 1 if players > 11 else 0
print(f'{players-2-man-lub-jur} ролей под мирных и мафию')
mir = int(input('мирных: '))
maf = players-2-man-lub-jur-mir
roles = ['мир']*mir+['ком', 'док']+['маф']*maf+['ман']*man+['люб']*lub+['жур']*jur
random.shuffle(roles)
for i, role in enumerate(roles):
    print(i+1, ':', role)
input()
