import pygame
import math
import os
pygame.init()


def font(fnum, text, colour=(255, 255, 255)):
    usefont = myFont15 if fnum == 15 else myFont20 if fnum == 20 else 25
    return usefont.render(str(text), True, colour)


def rect(colour, w, h, alpha, text):
    surf = pygame.Surface((w, h))
    surf.fill(colour)
    surf.blit(text, [(w-text.get_width())/2, (h-text.get_height())/2])
    surf.set_alpha(alpha)
    return surf


class ChoiceMenu:
    def __init__(self):
        self.line = [
            1,
            rect(white, 95, 25, 50, font(20, 'line', black)),
            rect(white, 95, 25, 150, font(20, 'line', black))
        ]
        self.point = [
            0,
            rect(white, 95, 25, 50, font(20, 'point', black)),
            rect(white, 95, 25, 150, font(20, 'point', black))
        ]
        self.polygon = [
            0,
            rect(white, 95, 25, 50, font(20, 'polygon', black)),
            rect(white, 95, 25, 150, font(20, 'polygon', black))
        ]

    def draw(self):
        sc.blit(self.line[self.line[0]+1], [750, 10])
        sc.blit(self.point[self.point[0]+1], [750, 40])
        sc.blit(self.polygon[self.polygon[0]+1], [750, 70])

    def udate(self):
        if 750 <= mPos[0] <= 845 and 10 <= mPos[1] <= 35:
            self.line[0] = True
            self.point[0] = False
            self.polygon[0] = False
            return True
        if 750 <= mPos[0] <= 845 and 40 <= mPos[1] <= 65:
            self.line[0] = False
            self.point[0] = True
            self.polygon[0] = False
            return True
        if 750 <= mPos[0] <= 845 and 70 <= mPos[1] <= 95:
            self.line[0] = False
            self.point[0] = False
            self.polygon[0] = True
            return True
        return False


def save():
    with open(f'{fileName}.txt', 'w') as data:
        for i in linePoints:
            data.write(f'{i}  ')
        data.write('\n')
        for i in controlPoints:
            data.write(f'{i}  ')
        data.write('\n')
        for i in polygonPoints:
            data.write(f'{i}  ')
        print(f'файл "{fileName}""  сохранён')


def decode(plist):
    arr=[[], [], []]
    plist = plist.split('\n')
    print(*plist, sep='\n')
    lines = plist[0].split('  ')
    lines.remove('')
    for point in lines:
        point = point[2:-2].split(', ')
        arr[0].append([[int(point[0]), int(point[1][:-1])], [int(point[2][1:]), int(point[3])]])
    points = plist[1].split('  ')
    points.remove('')
    for point in points:
        point = point[1:-1].split(', ')
        arr[1].append([int(point[0]), int(point[1])])
    polygons = plist[2].split('  ')
    polygons.remove('')
    for polygon in polygons:
        arr[2].append([])
        print(polygon[2:-2].split('], ['))
        for point in polygon[2:-2].split('], [')[:-1]:
            point = point.split(', ')
            arr[2][-1].append([int(point[0]), int(point[1])])
    return arr


def background(blocks: int, place: list, rad: int):
    global backList
    bh = rad*0.4
    bw = rad//4
    x, y = place
    alpha = pi2/(blocks*2)
    outside = [[round(math.cos(-alpha*b)*(rad+bh)+x), round(math.sin(-alpha*b)*(rad+bh)+y)] for b in range(blocks*2)]
    inside = [[round(math.cos(-alpha*(b*2-0.5))*(rad-bw)+x), round(math.sin(-alpha*(b*2-0.5))*(rad-bw)+y)] for b in range(blocks)]
    for i in range(blocks):
        pygame.draw.aaline(sc, colors[0], outside[2*i], outside[2*i+1], 2)
        pygame.draw.aaline(sc, colors[1], outside[2*i+1], inside[i-blocks+1], 2)
        pygame.draw.aaline(sc, colors[2], inside[i-1], inside[i], 2)
        pygame.draw.aaline(sc, colors[3], inside[i], outside[2*i], 2)
    backList = outside+inside+[place]


def new_point():
    for li in allPoints:
        if math.hypot(li[0]-mPos[0], li[1]-mPos[1]) <= 7:
            return [*li]
    if showMainLine:
        for li in backList:
            if math.hypot(li[0]-mPos[0], li[1]-mPos[1]) <= 7:
                return [int(li[0]), int(li[1])]
    return [-10, -10]


def findInPolygon(point, fillingHelpPoint=False, points=[]):
    global helpPoints
    if not fillingHelpPoint:
        for polygon in polygonPoints:
            for p in polygon:
                if p == point:
                    return True
        return False
    else:
        for polygon in polygonPoints:
            thisPolygon = True
            for p in points:
                if p not in polygon:
                    thisPolygon = False
                    break
            if thisPolygon:
                for p in polygon:
                    if p not in helpPoints:
                        helpPoints.append(p)
                break


def polygon_del():
    for polygon in polygonPoints:
        thisPolygon = True
        for p in delPoint:
            if p not in polygon:
                thisPolygon = False
                break
        if thisPolygon and len(delPoint) == len(polygon)-1:
            for point in  polygon:
                allPoints.remove(point)
            polygonPoints.remove(polygon)
            delPoint.clear()
            helpPoints.clear()
            break


def line_del():
    global delPoint, controlPoints, linePoints
    if len(delPoint) == 1:
        for point in linePoints:
            if delPoint[0] == point[0] and point[1] not in helpPoints:
                helpPoints.append(point[1])
            if delPoint[0] == point[1] and point[0] not in helpPoints:
                helpPoints.append(point[0])
    elif len(delPoint) == 2 and not findInPolygon(delPoint[0]) and not findInPolygon(delPoint[1]):
        if delPoint[0] == delPoint[1] and delPoint[0] in controlPoints:
            controlPoints.remove(delPoint[0])
            allPoints.remove(delPoint[0])
        x, y = delPoint
        if [x, y] in linePoints or [y, x] in linePoints:
            allPoints.remove(x)
            allPoints.remove(y)
            linePoints.remove([x, y] if [x, y] in linePoints else [y, x])
        activePoint = new_point()
        delPoint = [] if activePoint == [-10, -10] else [activePoint]
        helpPoints.clear()
    elif len(delPoint) != 0:
        findInPolygon([], True, delPoint)
        polygon_del()


def txt_find(arr=[]):
    for file in os.listdir(os.getcwd()):
        if file.endswith('.txt'):
            arr.append(file[:-4])
    return arr


def drawAllPoints():
    for point in allPoints.copy().remove(delPoint) if delPoint in allPoints else allPoints:
        if point not in delPoint:
            pygame.draw.circle(sc, green, point, 7, 1)
    if showMainLine:
        for point in backList.copy().remove(delPoint) if delPoint in backList else backList:
            pygame.draw.circle(sc, green, point, 7, 1)


def fillAllPoint(point):
    allPoints.append(point)


scW, scH = 850, 650
pi_2 = math.pi/2
pi2 = math.pi*2
myFont15 = pygame.font.SysFont('verdana', 15)
myFont20 = pygame.font.SysFont('verdana', 20)
myFont25 = pygame.font.SysFont('verdana', 25)
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
delPoint = []
helpPoints = []
linePoints = []
multiPoint = []
polygonPoints = [[]]

fileName = txt_find()
print('0 - новый рисунок')
for name in range(len(fileName)):
    print(f'{name+1} - {fileName[name]}')
dataFile = int(input(f'Какой рисунок хотите загрузить?\n>'))
if dataFile != 0:
    fileName = fileName[dataFile-1]
    with open(f'{fileName}.txt', 'r') as data:
        data = data.read()
        if data != '':
            linePoints, controlPoints, polygonPoints = decode(data)
            if len(polygonPoints) == 0:
                polygonPoints.append([])
            for line in linePoints:
                fillAllPoint(line[0])
                fillAllPoint(line[1])
            for point in controlPoints:
                fillAllPoint(point)
            for polygon in polygonPoints:
                for point in polygon:
                    fillAllPoint(point)
else:
    fileName = input('назовите ваш рисунок\n>')
    data = open(f'{fileName}.txt', 'w')
    data.close()
print(f'файл "{fileName}" '+('загружен' if dataFile != 0 else 'создан'))

sc = pygame.display.set_mode((scW, scH))
pygame.display.set_caption(fileName)
numBlocks = 4
choiceMenu = ChoiceMenu()
clock = pygame.time.Clock()
activePoint = [-10, -10]
showMainLine = True
showAllPoints = False
added = False
done = False
while not done:
    sc.fill(black)
    mPos = pygame.mouse.get_pos()
    mods = pygame.key.get_mods()
    choiceMenu.draw()
    if showMainLine:
        background(numBlocks, [325, 325], 220)
    line_del()
    activePoint = new_point()
    for li in linePoints:
        if li[0] == li[1]:
            linePoints.remove(li)
            allPoints.remove(li[0])
            allPoints.remove(li[0])
            break
    for polygon in range(len(polygonPoints)-1):
        pygame.draw.polygon(sc, gray[50], polygonPoints[polygon])
    if len(polygonPoints[-1]) != 0:
        for point in range(len(polygonPoints[-1])-1):
            pygame.draw.line(sc, white, polygonPoints[-1][point], polygonPoints[-1][point+1], 2)
        else:
            pygame.draw.line(sc, white, polygonPoints[-1][-1], mPos, 2)
    if not showAllPoints:
        pygame.draw.circle(sc, red, activePoint, 7, 1)
        for point in helpPoints:
            pygame.draw.circle(sc, green, point, 7, 1)
    for point in multiPoint:
        pygame.draw.line(sc, white, point[0], mPos, 2)
    for li in linePoints:
        if li == linePoints[-1] and added:
            pygame.draw.line(sc, white, li[0], mPos, 2)
        else:
            pygame.draw.aaline(sc, white, *li, 2)
    if showAllPoints:
        drawAllPoints()
    for li in delPoint:
        pygame.draw.circle(sc, blue, li, 7, 1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == 9:
                showAllPoints = not showAllPoints
            if event.key == 27:
                done = True
            if event.key == 32:
                showMainLine = not showMainLine
            if event.key == 115 and mods & pygame.KMOD_LCTRL:
                save()
            if event.key == 122 and mods & pygame.KMOD_LCTRL:
                if len(linePoints) != 0:
                    allPoints.remove(linePoints[-1][0])
                    allPoints.remove(linePoints.pop()[1])
            if event.key == 127:
                linePoints.clear()
                allPoints.clear()
        if event.type == pygame.MOUSEBUTTONDOWN:
            newAddPoint = [*mPos] if activePoint == [-10, -10] else activePoint
            if event.button == 1:
                delPoint.clear()
                helpPoints.clear()
                if not choiceMenu.udate():
                    if choiceMenu.line[0]:
                        if mods & pygame.KMOD_LALT:
                            multiPoint.append([newAddPoint, []])
                        elif len(multiPoint) == 0:
                            linePoints.append([newAddPoint, []])
                            fillAllPoint(newAddPoint)
                            added = True
                    if choiceMenu.point[0]:
                        if newAddPoint not in controlPoints:
                            controlPoints.append(newAddPoint)
                            fillAllPoint(newAddPoint)
                    if choiceMenu.polygon[0]:
                        if len(polygonPoints[-1]) != 0 and newAddPoint == polygonPoints[-1][0]:
                            polygonPoints[-1].append(newAddPoint)
                            fillAllPoint(newAddPoint)
                            polygonPoints.append([])
                            for i in range(len(polygonPoints[-1])):
                                x, y = polygonPoints[i-1], polygonPoints[i]
                                if [x, y] in linePoints or [y, x] in linePoints:
                                    linePoints.remove([x, y] if [x, y] in linePoints else [y, x])
                        else:
                            polygonPoints[-1].append(newAddPoint)
                            fillAllPoint(newAddPoint)
            if event.button == 3:
                if choiceMenu.polygon[0] and len(polygonPoints[-1]) != 0:
                    allPoints.remove(polygonPoints[-1].pop())
                elif choiceMenu.line[0] and len(linePoints[-1][1]) == 0:
                    allPoints.remove(linePoints.pop()[0])
                    added = False
                else:
                    delPoint.append(activePoint)
                    print(delPoint)
            if event.button == 4:  # up
                numBlocks += 1
            if event.button == 5 and numBlocks > 1:  # down
                numBlocks -= 1
        if event.type == pygame.MOUSEBUTTONUP:
            newAddPoint = [*mPos] if activePoint == [-10, -10] else activePoint
            if event.button == 1:
                if not mods & pygame.KMOD_LALT:
                    if not choiceMenu.udate():
                        if choiceMenu.line[0]:
                            if len(multiPoint) != 0:
                                for point in multiPoint:
                                    fillAllPoint(point[0])
                                    linePoints.append([point[0], newAddPoint])
                                multiPoint.clear()
                                fillAllPoint(newAddPoint)
                            else:
                                added = False
                                if len(linePoints) != 0 and len(linePoints[-1][1]) == 0:
                                    linePoints[-1][1] = newAddPoint
                                    fillAllPoint(newAddPoint)
    clock.tick(30)
save()
