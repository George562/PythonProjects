import pygame as pyg
import math
import os
import re
pyg.init()


def font(f_num: int, t, colour=(255, 255, 255)):
    return myFonts[f_num-5 if 5 <= f_num <= 45 else 10].render(str(t), True, colour)


def my_rect(bg, w: int, h: int, alpha: list, t):
    arr = []
    for i in alpha:
        surf = pyg.Surface((w, h))
        surf.fill(bg)
        if bg == black:
            pyg.draw.rect(surf, white, [1, 1, w-2, h-2], 1)
        surf.blit(t, [(w-t.get_width())/2, (h-t.get_height())/2])
        surf.set_alpha(i)
        arr.append(surf)
    return arr


class InfoMenu:
    def __init__(self):
        self.surf = pyg.Surface((200, 350))
        self.sZI = {
            'show': 0,
            'block': False,
            '0.25': my_rect(black, 55, 25, [255], font(18, '0.25'))[0],
            '1': my_rect(black, 55, 25, [255], font(18, '1'))[0],
            '4': my_rect(black, 55, 25, [255], font(18, '4'))[0],
            'change': 0.25
        }
        self.chObj = None

    def update(self):
        if mPos[0] in range(56) and mPos[1] in range(21):
            self.chObj = 'sNB'
            background(numBlocks, center, radius)
            return True
        if mPos[0] in range(55, 131) and mPos[1] in range(26):
            self.sZI['block'] = not self.sZI['block']
            return True
        if self.sZI['show'] and mPos[0] in range(135, 191) and mPos[1] in range(76):
            if mPos[1] in range(76):
                self.sZI['change'] = 0.25*4**(mPos[1]//25)
            return True
        if Menu.line['func']['choice']['active']:
            self.chObj = 'line'
        return False

    def draw(self):
        sc.blit(sNB, [0, 0])
        sc.blit(sZI, [55, 0])
        if mPos[0] in range(55, 131) and mPos[1] in range(26) or self.sZI['block']:
            self.sZI['show'] = 1
        elif self.sZI['show'] and not (mPos[0] in range(130, 191) and mPos[1] in range(76)):
            self.sZI['show'] = 0
        if self.sZI['show']:
            for num, i in [self.sZI['0.25'], 0], [self.sZI['1'], 1], [self.sZI['4'], 2]:
                sc.blit(num, [135, i*25])


class ChoiceMenu:
    def __init__(self):
        self.butX = scW-100
        self.funcX = scW-200
        self.line = {
            'active': 1,
            'button': my_rect(white, 95, 25, [50, 150], font(20, 'line', black)),
            'func': {
                'draw': self.button_object(1, 'draw', [self.funcX, 10]),
                'choice': self.button_object(0, 'choice', [self.funcX, 40]),
                'division': self.button_object(0, 'division', [self.funcX, 70]),
                'mirror': self.button_object(0, 'mirror', [self.funcX, 100]),
                'Alt': self.button_object(0, 'Alt', [self.funcX, 130]),
                'delete': self.button_object(0, 'delete', [self.funcX, 160]),
                'last place': 160
            }
        }
        self.point = {
            'active': 0,
            'button': my_rect(white, 95, 25, [50, 150], font(20, 'point', black)),
            'func': {
                'drop': self.button_object(1, 'drop', [self.funcX, 10]),
                'choice': self.button_object(0, 'choice', [self.funcX, 40]),
                'delete': self.button_object(0, 'delete', [self.funcX, 70]),
                'last place': 70
            }
        }
        self.polygon = {
            'active': 0,
            'button': my_rect(white, 95, 25, [50, 150], font(20, 'polygon', black)),
            'func': {
                'draw': self.button_object(1, 'draw', [self.funcX, 10]),
                'choice': self.button_object(0, 'choice', [self.funcX, 40]),
                'delete': self.button_object(0, 'delete', [self.funcX, 70]),
                'last place': 70
            }
        }
        self.objects = [self.line, self.point, self.polygon]
        self.nowAct = self.line
        self.shawAllObj = True

    def button_object(self, act: int, bt: str, pl: list):  # active, button text, place
        ans = {'active': act,
               'button': my_rect(white, 95, 25, [50, 150], font(20, bt, black)),
               'place': [pl, range(pl[1], pl[1]+26)]}
        return ans

    def activeObject(self):
        for obj in self.objects:
            if obj['active']:
                return obj

    def draw(self):
        """ draw all buttons """
        sc.blit(self.line['button'][self.line['active']], [self.butX, 10])
        sc.blit(self.point['button'][self.point['active']], [self.butX, 40])
        sc.blit(self.polygon['button'][self.polygon['active']], [self.butX, 70])

        for func in self.nowAct['func']:
            if type(self.nowAct['func'][func]) == dict:
                sc.blit(self.nowAct['func'][func]['button'][self.nowAct['func'][func]['active']],
                        self.nowAct['func'][func]['place'][0])

    def off_all_func(self, without=''):
        for func in self.nowAct['func']:
            if type(self.nowAct['func'][func]) == dict:
                self.nowAct['func'][func]['active'] = 0
        if without:
            self.nowAct['func'][without]['active'] = 1

    def update(self):
        """ check click on 'button' and return True if was click on button """
        if mPos[0] in range(self.funcX, self.butX+96):
            if mPos[0] in range(self.butX, self.butX+96):
                if 10 <= mPos[1] <= 35:
                    self.line['active'] = 1
                if 40 <= mPos[1] <= 65:
                    self.point['active'] = 1
                if 70 <= mPos[1] <= 95:
                    self.polygon['active'] = 1
            elif mPos[1] in range(5, self.nowAct['func']['last place']+26):
                for func in self.nowAct['func']:
                    if type(self.nowAct['func'][func]) == dict and mPos[1] in self.nowAct['func'][func]['place'][1]:
                        self.off_all_func(without=func)
            self.nowAct['active'] = 0
            if self.activeObject() is None:
                self.nowAct['active'] = 1
            else:
                self.nowAct = self.activeObject()
            return True
        return False


class AllLines:
    """ Object where all line and points of line, for ease of use """
    def __init__(self):
        self.lines = []
        self.r_lines = []  # reverse line
        self.points = []
        self.t_lines = []  # temporary lines
        self.f_line = []  # fake line
        self.alpha = 0

    def draw(self):
        if not Menu.line['func']['mirror']['active']:
            for dot in self.t_lines:
                pyg.draw.line(sc, white, mFP(zoomer(dot)), mPos, 2)
        else:
            start = -(math.atan2(*mRP(mPos))-pi_2)
            dist = math.hypot(*zoomer(mRP(mPos), reverse=True))
            for dot in range(len(self.t_lines)):
                sd = dist*math.cos(start+self.alpha*dot)
                ld = dist*math.sin(start+self.alpha*dot)
                pyg.draw.line(sc, white, *mFP(zoomer([self.t_lines[dot], [sd, ld]])), 2)
        for line in self.lines:
            pyg.draw.aaline(sc, white, *mFP(zoomer(line)), 2)

    def add_sp(self, sp, mirror=False):  # add start point
        if not mirror:
            self.t_lines.append(sp)
        else:
            self.alpha = pi2/numBlocks
            self.reflection(sp, True)

    def add_lp(self, lp: list, mirror=False):  # add last point
        if not mirror:
            for dot in self.t_lines:
                if [dot, lp] not in self.lines+self.r_lines and dot != lp:
                    self.lines.append([dot, lp])
                    self.r_lines.append([lp, dot])
                    fillAllPoint(lp, dot)
        else:
            self.reflection(lp, False)
        self.t_lines.clear()

    def reflection(self, p, loading):
        start = -(math.atan2(*p)-pi_2)
        dist = math.hypot(*p)
        for dot in range(numBlocks):
            sd = dist*math.cos(start+self.alpha*dot)
            ld = dist*math.sin(start+self.alpha*dot)
            if loading:
                self.t_lines.append([sd, ld])
            elif [sd, ld] not in self.lines+self.r_lines:
                self.lines.append([self.t_lines[dot], [sd, ld]])
                self.r_lines.append([[ld, sd], self.t_lines[dot]])
                fillAllPoint([ld, sd])


def save():
    """ save all points in file """
    with open(f'{self_folder}/{fileName}.txt', 'w') as new_data:
        for i in allLines.lines:
            new_data.write(f'{i}  ')
        new_data.write('\n')
        for i in controlPoints:
            new_data.write(f'{i}  ')
        new_data.write('\n')
        for i in polygonPoints:
            new_data.write(f'{i}  ')
        print(f'файл "{fileName}" сохранён')


def data_upload(plist):
    """ upload points from file.txt """
    arr = [[], [], []]
    plist = plist.split('\n')
    lines = plist[0].split('  ')
    for dot in lines[:-1]:
        dot = dot[2:-2].split(', ')
        arr[0].append([[float(dot[0]), float(dot[1][:-1])], [float(dot[2][1:]), float(dot[3])]])
    points = plist[1].split('  ')
    for dot in points[:-1]:
        dot = dot[1:-1].split(', ')
        arr[1].append([float(dot[0]), float(dot[1])])
    polygons = plist[2].split('  ')
    for pol in polygons[:-1]:
        arr[2].append([])
        for dot in pol[2:-2].split('], [')[:-1]:
            dot = dot.split(', ')
            arr[2][-1].append([float(dot[0]), float(dot[1])])
    return arr


def background(bl: int, pl: list, rad: int):  # blocks, place, radius
    global backList, outside, inside
    bl = bl if bl else 4
    bw = rad*0.525
    alpha = pi2/(bl*2)
    start_alpha = -pi_2
    outside = [[round(math.cos(start_alpha-alpha*b)*rad+pl[0]),
                round(math.sin(start_alpha-alpha*b)*rad+pl[1])] for b in range(bl*2)]
    inside = [[round(math.cos(start_alpha-alpha*(b*2-0.5))*bw+pl[0]),
               round(math.sin(start_alpha-alpha*(b*2-0.5))*bw+pl[1])] for b in range(bl)]
    backList = outside+inside+[pl]
    sNB.fill(black)
    pyg.draw.rect(sNB, white, [1, 1, sNB.get_width()-1, sNB.get_height()-1], 1)
    t = font(20, str(numBlocks)+('' if infoMenu.chObj != 'sNB' else '|'))
    sNB.blit(t, [(sNB.get_width()-t.get_width()) / 2, (sNB.get_height()-t.get_height())/2])


def new_point():
    for lin in allPoints:
        lin = mFP(lin)
        if math.hypot(lin[0]-mPos[0], lin[1]-mPos[1]) <= 5:
            return [*lin]
    if showMainLine:
        for lin in backList:
            if math.hypot(lin[0]-mPos[0], lin[1]-mPos[1]) <= 5:
                return [float(lin[0]), float(lin[1])]
    return []


def txt_find():
    arr = []
    if not os.path.exists(os.getcwd()+'/'+self_folder):
        os.mkdir(os.getcwd()+'/'+self_folder)
    for file in os.listdir(os.getcwd()+'/'+self_folder):
        if file.endswith('.txt'):
            arr.append(file[:-4])
    return arr


def draw_all_points():
    for dot in allPoints:
        pyg.draw.circle(sc, green, inter(mFP(zoomer(dot))), 5, 1)
    if showMainLine:
        for dot in backList:
            pyg.draw.circle(sc, green, inter(dot), 5, 1)


def fillAllPoint(*args):
    for dot in args:
        allPoints.append(dot)


def del_all_point(*args):
    for dot in args:
        try:
            allPoints.remove(dot)
        except ValueError:
            continue


def mRP(arr: list):  # makeRealPlace
    return [arr[0]-center[0], arr[1]-center[1]]


def mFP(arr: list):  # makeFakePlace
    new_arr = []
    if type(arr[0]) != list:
        new_arr = [arr[0]+center[0], arr[1]+center[1]]
    else:
        for dot in arr:
            new_arr.append([dot[0]+center[0], dot[1]+center[1]])
    return new_arr


def zoomer(arr: list, reverse=False):
    new_arr = []
    if type(arr[0]) != list:
        new_arr = [arr[0]*zoom, arr[1]*zoom] if not reverse else [arr[0]/zoom, arr[1]/zoom]
    else:
        for dot in arr:
            if not reverse:
                new_arr.append([dot[0]*zoom, dot[1]*zoom])
            else:
                new_arr.append([dot[0]/zoom, dot[1]/zoom])
    return new_arr


def inter(arr: list):
    return [int(arr[0]), int(arr[1])]


scW, scH = 1050, 695
pi_2 = math.pi/2
pi2 = math.pi*2
myFonts = [pyg.font.SysFont('verdana', i) for i in range(5, 46)]
white = (255, 255, 255)
gray = [(i, i, i) for i in range(256)]
black = (5, 10, 15)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
colors = [red, (170, 60, 0), (0, 170, 60), (60, 0, 170)]
allPoints = []
backList = []
controlPoints = []
helpPoints = []
allLines = AllLines()
polygonPoints = [[]]

outside = []
inside = []

self_folder = 'pics'
fileName = txt_find()
print('0 - новый рисунок')
for name in range(len(fileName)):
    print(f'{name+1} - {fileName[name]}')
dataFile = input(f'Какой рисунок хотите загрузить?\n>')
ex_answer = re.compile(r'^[0-9]+$')
while 1:
    if ex_answer.search(dataFile):
        dataFile = int(dataFile)
        if 0 <= dataFile <= len(fileName):
            break
        else:
            dataFile = input('введите число соответсвующее нужному рисунку или 0 чтобы создать новый\n>')
    else:
        dataFile = input('введите число соответсвующее нужному рисунку\n>')

if dataFile:
    print('подождите загрузки файла, это может занять время')
    fileName = fileName[dataFile-1]
    with open(f'{self_folder}/{fileName}.txt') as data:
        data = data.read()
        if data:
            allLines.lines, controlPoints, polygonPoints = data_upload(data)
            if len(polygonPoints) == 0:
                polygonPoints.append([])
            for line in allLines.lines:
                fillAllPoint(line[0], line[1])
            for point in controlPoints:
                fillAllPoint(point)
            for polygon in polygonPoints:
                for point in polygon:
                    fillAllPoint(point)
        print(f'файл "{fileName}" загружен')
else:
    fileName = input('назовите ваш рисунок\n>')
    new_data = open(f'{self_folder}/{fileName}.txt', 'w')
    new_data.close()
    print(f'файл "{fileName}" создан')

sc = pyg.display.set_mode((scW, scH))
pyg.display.set_caption(fileName)
infoMenu = InfoMenu()
ex_nums = '0123456789'
center = [425, 345]
radius = 330
numBlocks = 4
sNB = my_rect(black, 55, 20, [255], font(20, numBlocks))[0]  # surface Number Blocks
background(numBlocks, center, radius)
Menu = ChoiceMenu()
clock = pyg.time.Clock()
activePoint = []
zoom = 1
sZI = my_rect(black, 75, 20, [255], font(20, str(zoom) + 'x'))[0]  # surface Zoom Indicator
pyg.draw.rect(sZI, white, [1, 1, sZI.get_width()-1, sZI.get_height()-1], 1)
showMainLine = True
showAllPoints = False
added = False
done = False
while not done:
    sc.fill(black)
    mPos = pyg.mouse.get_pos()
    mods = pyg.key.get_mods()
    infoMenu.draw()
    Menu.draw()
    allLines.draw()
    if showMainLine:
        for i in range(numBlocks):
            pyg.draw.aaline(sc, colors[0], outside[2*i], outside[2*i+1], 2)
            pyg.draw.aaline(sc, colors[1], outside[2*i+1], inside[i-numBlocks+1], 2)
            pyg.draw.aaline(sc, colors[2], inside[i-1], inside[i], 2)
            pyg.draw.aaline(sc, colors[3], inside[i], outside[2*i], 2)
    activePoint = new_point()
    for polygon in range(len(polygonPoints)-1):
        pyg.draw.polygon(sc, gray[50], polygonPoints[polygon])
    if len(polygonPoints[-1]) != 0:
        for point in range(len(polygonPoints[-1])-1):
            pyg.draw.line(sc, white, polygonPoints[-1][point], polygonPoints[-1][point+1], 2)
        else:
            pyg.draw.line(sc, white, polygonPoints[-1][-1], mPos, 2)
    if not showAllPoints:
        if activePoint:
            pyg.draw.circle(sc, red, inter(activePoint), 5, 1)
        for point in helpPoints:
            pyg.draw.circle(sc, green, inter(point), 5, 1)
    if showAllPoints:
        draw_all_points()
    pyg.display.flip()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            done = True
        if event.type == pyg.KEYDOWN:
            print(event.key)
            if infoMenu.chObj == 'sNB' and event.key == 8:  # Backspace
                numBlocks = str(numBlocks)[0:-1]
                if numBlocks:
                    numBlocks = int(numBlocks)
                else:
                    numBlocks = 0
                background(numBlocks, center, radius)
            if event.key == 9:  # Tab
                showAllPoints = not showAllPoints
            if infoMenu.chObj == 'sNB' and event.key == 13:
                infoMenu.chObj = None
                background(numBlocks, center, radius)
            if event.key == 27:  # Esc
                done = True
            if event.key == 32:  # Space
                showMainLine = not showMainLine
            if infoMenu.chObj == 'sNB' and (48 <= event.key <= 57 or 256 <= event.key <= 265):  # numbers
                numBlocks = int(str(numBlocks)+ex_nums[event.key-(48 if event.key <= 57 else 256)])
                if numBlocks > 999:
                    numBlocks = 999
                background(numBlocks, center, radius)
            if event.key == 115 and mods & pyg.KMOD_LCTRL:
                save()
            if event.key == 122 and mods & pyg.KMOD_LCTRL:
                continue
            if event.key == 127:
                raise Exception('workaround to not save')
            if event.key == 308 and Menu.line['active']:
                Menu.off_all_func(without='Alt')
        if event.type == pyg.KEYUP:
            if event.key == 308 and Menu.line['active']:
                Menu.off_all_func(without='draw')
        if event.type == pyg.MOUSEBUTTONDOWN:
            newAddPoint = [*mPos] if not activePoint else activePoint
            newAddPoint = zoomer(mRP(newAddPoint), reverse=True)
            if event.button == 1:
                helpPoints.clear()
                if not (Menu.update() or infoMenu.update()):
                    if Menu.line['active']:
                        if Menu.line['func']['draw']['active']:
                            if not (added or allLines.t_lines):
                                allLines.add_sp(newAddPoint)
                            else:
                                allLines.add_lp(newAddPoint)
                        elif Menu.line['func']['mirror']['active']:
                            if not added:
                                allLines.t_lines.clear()
                                allLines.add_sp(newAddPoint, mirror=True)
                            else:
                                allLines.add_lp(newAddPoint, mirror=True)
                        elif Menu.line['func']['Alt']['active']:
                            allLines.add_sp(newAddPoint)
                            added = False
                        added = not added
                    if Menu.point['active']:
                        if newAddPoint not in controlPoints:
                            controlPoints.append(newAddPoint)
                            fillAllPoint(newAddPoint)
                    if Menu.polygon['active']:
                        if len(polygonPoints[-1]) != 0 and newAddPoint == polygonPoints[-1][0]:
                            polygonPoints[-1].append(newAddPoint)
                            fillAllPoint(newAddPoint)
                            polygonPoints.append([])
                            for i in range(len(polygonPoints[-1])):
                                x, y = polygonPoints[i-1], polygonPoints[i]
                        else:
                            polygonPoints[-1].append(newAddPoint)
                            fillAllPoint(newAddPoint)
            if event.button == 3:
                if Menu.line['active']:
                    if Menu.line['func']['mirror']['active']:
                        allLines.t_lines.clear()
                    else:
                        allLines.t_lines = allLines.t_lines[0:-1]
                    added = True if allLines.t_lines else False
            if event.button in [4, 5]:
                if event.button == 4:  # up
                    zoom += infoMenu.sZI['change']
                    if zoom > 100:
                        zoom = 100
                elif numBlocks > 1:  # down
                    zoom -= infoMenu.sZI['change']
                    if zoom < 0.25:
                        zoom = 0.25
                sZI.fill(black)
                pyg.draw.rect(sZI, white, [1, 1, sZI.get_width()-1, sZI.get_height()-1], 1)
                if int(zoom) == zoom:
                    zoom = int(zoom)
                text = font(18, str(zoom)+'x')
                sZI.blit(text, [(sZI.get_width()-text.get_width())/2, (sZI.get_height()-text.get_height())/2])
    clock.tick(30)
save()
