import pygame, random, time, math

SCR_SIZE = 850
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
DRED = [180, 0, 0]
DBLUE = [0, 0, 150]
DGREEN = [0, 180, 0]
DYELLOW = [180, 180, 0]
AQUA = [0, 255, 255]
GREY = [150, 150, 150]
BLACK = [0, 0, 0]
BACKGROUND = [255, 223, 163]
farbenW = [[255, 100, 100], [100, 100, 255], [100, 255, 100], [255, 255, 100]]

winner = None
farben = ["ROT", "BLAU", "GRÜN", "GELB"]
# 0 - rot
# 1 - blau
# 2 - grün
# 3 - gelb

radField = 30
distBorder = 75
distField = 70
radFigur = 20
wuerfelSize = 60
wuerfelZahl = 0

zZeit = 1
running = True
turn = 0
wTurns = []

movePrio = []

PLAYER = 0

class Feld:
    def __init__(self, pos, art, ind):
        self.pos = pos
        self.art = art
        self.ind = ind

class Figur:
    def __init__(self, feld, farbe):
        self.feld = feld
        self.farbe = farbe
        self.selected = False
        self.prio = 0

    # festlegen, welche Priorität Figur hat, nur wenn keine andere Figur eine höhere hat kann sie bewegt werden
    def setPrio(self, wZahl):
        if not self.canMove(wuerfelZahl) or turn % 4 != self.farbe:
            self.prio = 0
            return 0

        match self.feld.art:
            case "feld":
                if self.feld == sPos[self.farbe]:
                    self.prio = 3
                    return 3
                else:
                    if self.feld.ind < sPos[self.farbe].ind <= self.feld.ind + wuerfelZahl:
                        if wuerfelZahl - (sPos[self.farbe].ind - self.feld.ind) < len(zFelder[self.farbe]):
                            self.prio = 1
                            return 1
                    if sPos[self.farbe].ind == 0:
                        if 0 < wZahl - (len(felder) - self.feld.ind) < len(zFelder[self.farbe]):
                            self.prio = 1
                            return 1
                    for i in range(4):
                        for fig in figuren[i]:
                            if fig.farbe == self.farbe:
                                continue
                            elif self.feld.ind + wuerfelZahl < len(felder):
                                if fig.feld == felder[self.feld.ind + wuerfelZahl]:
                                    self.prio = 2
                                    return 2
                            elif fig.feld == felder[self.feld.ind - len(felder) + wuerfelZahl]:
                                self.prio = 2
                                return 2
                self.prio = 1
                return 1
            case "ZIEL":
                self.prio = 1
                return 1
            case "START":
                self.prio = 4
                return 4
        return 0

    # Figur bewegen, evtl. andere schlagen                
    def move(self, wZahl):
        global turn
        
        nFeld = None
        match self.feld.art:
            case "START":
                if wZahl == 6:
                    nFeld = sPos[self.farbe]
            case "feld":
                if self.feld.ind + wZahl < len(felder):
                    if self.feld.ind < sPos[self.farbe].ind <= self.feld.ind + wZahl:
                        if wZahl - (sPos[self.farbe].ind - self.feld.ind) < len(zFelder[self.farbe]):
                            nFeld = zFelder[self.farbe][wZahl - (sPos[self.farbe].ind - self.feld.ind)]
                        else:
                            nFeld = None
                    else:
                        nFeld = felder[self.feld.ind + wZahl]
                else:
                    if sPos[self.farbe].ind == 0:
                        if wZahl - (len(felder) - self.feld.ind) < len(zFelder[self.farbe]):
                            nFeld = zFelder[self.farbe][wZahl - (len(felder) - self.feld.ind)]################
                    else:
                        nFeld = felder[self.feld.ind - len(felder) + wZahl]
            case "ZIEL":
                if self.feld.ind + wZahl < len(zFelder[self.farbe]):
                    nFeld = zFelder[self.farbe][self.feld.ind + wZahl]

        if not self.canMove(wuerfelZahl):
            nFeld = None
        
        for p in movePrio:
            if p > self.prio:
                return False
        
        for i in range(4):
            for f in figuren[i]:
                if f.feld == nFeld:
                    if f.farbe == self.farbe:
                        nFeld = None
                        break
                    else:
                        i = 0
                        for j in range(4):
                            for fig in figuren[f.farbe]:
                                if fig.feld == sFelder[f.farbe][i]:
                                    i += 1
                        f.feld = sFelder[f.farbe][i]
                        break
                    
        if nFeld != None: # nFeld ist das neue Feld der Figur, wenn nFeld == None wird die Figur nicht bewegt
            self.feld = nFeld
            self.selected = False
            if wuerfelZahl != 6:
                global img
                turn += 1
                img = font.render("", True, BLACK)
            else:
                wTurns.remove(turn)
                
                    
    # überprüfen ob die Figur sich bewegen kann
    def canMove(self, wZahl):

        match self.feld.art:
            case "START":
                if wZahl == 6:
                    for fig in figuren[self.farbe]:
                        if fig.feld == sPos[self.farbe]:
                            return False
                    return True
                else:
                    return False
            case "feld":
                
                if sPos[self.farbe].ind == 0:
                    if 0 < wZahl - (len(felder) - self.feld.ind) >= len(zFelder[self.farbe]):
                        return False
                    elif 0 < wZahl - (len(felder) - self.feld.ind) < len(zFelder[self.farbe]):
                        for fig in figuren[self.farbe]:
                            if zFelder[self.farbe][wZahl - (len(felder) - self.feld.ind)] == fig.feld:
                                return False
                            
                if self.feld.ind < sPos[self.farbe].ind <= self.feld.ind + wuerfelZahl:
                    if wuerfelZahl - (sPos[self.farbe].ind - self.feld.ind) >= len(zFelder[self.farbe]):
                        return False
                    for fig in figuren[self.farbe]:
                            if zFelder[self.farbe][wuerfelZahl - (sPos[self.farbe].ind - self.feld.ind)] == fig.feld:
                                return False
                    
                for i in range(4):                    
                    for fig in figuren[i]:
                        if self.feld.ind < sPos[self.farbe].ind <= self.feld.ind + wuerfelZahl and 0 < wuerfelZahl - (sPos[self.farbe].ind - self.feld.ind):
                            if fig.feld == zFelder[self.farbe][wuerfelZahl - (sPos[self.farbe].ind - self.feld.ind)]:
                                return False
                        if sPos[self.farbe].ind == 0 and 0 < wuerfelZahl - (len(felder) - self.feld.ind) < len(zFelder[self.farbe]):
                            if fig.feld == zFelder[self.farbe][wuerfelZahl - (len(felder) - self.feld.ind)]:
                                return False
                        if self.feld.ind + wuerfelZahl < len(felder):
                            if fig.feld == felder[self.feld.ind + wuerfelZahl] and fig.farbe == self.farbe:
                                return False
                        else:
                            if fig.feld == felder[self.feld.ind - len(felder) + wuerfelZahl] and fig.farbe == self.farbe:
                                return False
                return True
            case "ZIEL":
                if self.feld.ind + wuerfelZahl < len(zFelder[self.farbe]):
                    for i in range(wZahl):
                        for fig in figuren[self.farbe]:
                            if zFelder[self.farbe][self.feld.ind + i + 1] == fig.feld:
                                return False
                    return True
                else:
                    return False


felder = []
figuren = [[], [], [], []]
sFelder = [[], [], [], []]
zFelder = [[], [], [], []]
sPos = [None, None, None, None]


pygame.init()
screen = pygame.display.set_mode([SCR_SIZE, SCR_SIZE])

screen.fill(BACKGROUND)

wuerfel = pygame.Rect(SCR_SIZE / 2 - wuerfelSize / 2, SCR_SIZE / 2 - wuerfelSize / 2, wuerfelSize, wuerfelSize)
font = pygame.font.SysFont(None, 24)
img = font.render('Würfeln', True, BLACK)

x = 0
y = 0


def initFeld(rng, liste, var, direction, art, lInt): # Reihe von Feldern erstellen in vorgegebene Richtung
    global x, y
    for i in range(rng):
        liste.append(Feld([x, y], art, lInt))
        if direction == "+":
            if var == "x":
                x += distField
            elif var == "y":
                y += distField
        elif direction == "-":
            if var == "x":
                x -= distField
            elif var == "y":
                y -= distField
        lInt += 1
    return lInt


def initField():
    global x, y
    x = distBorder
    y = distBorder + 4 * distField

    lInt = 0
    # normale Felder erstellen
    lInt = initFeld(4, felder, "x", "+", "feld", lInt)
    lInt = initFeld(4, felder, "y", "-", "feld", lInt)
    lInt = initFeld(2, felder, "x", "+", "feld", lInt)
    lInt = initFeld(4, felder, "y", "+", "feld", lInt)
    lInt = initFeld(4, felder, "x", "+", "feld", lInt)
    lInt = initFeld(2, felder, "y", "+", "feld", lInt)
    lInt = initFeld(4, felder, "x", "-", "feld", lInt)
    lInt = initFeld(4, felder, "y", "+", "feld", lInt)
    lInt = initFeld(2, felder, "x", "-", "feld", lInt)
    lInt = initFeld(4, felder, "y", "-", "feld", lInt)
    lInt = initFeld(4, felder, "x", "-", "feld", lInt)
    lInt = initFeld(2, felder, "y", "-", "feld", lInt)

    # Startfelder erstellen
    lInt = 0
    x = 75
    y = 75
    lInt = initFeld(2, sFelder[0], "y", "+", "START", lInt)
    x = 75 + distField
    y = 75
    lInt = initFeld(2, sFelder[0], "y", "+", "START", lInt)

    lInt = 0
    x = SCR_SIZE - 75 - distField
    y = 75
    lInt = initFeld(2, sFelder[1], "y", "+", "START", lInt)
    x = SCR_SIZE - 75
    y = 75
    lInt = initFeld(2, sFelder[1], "y", "+", "START", lInt)

    lInt = 0
    x = SCR_SIZE - 75 - distField
    y = SCR_SIZE - 75 - distField
    lInt = initFeld(2, sFelder[2], "y", "+", "START", lInt)
    x = SCR_SIZE - 75
    y = SCR_SIZE - 75 - distField
    lInt = initFeld(2, sFelder[2], "y", "+", "START", lInt)

    lInt = 0
    x = 75
    y = SCR_SIZE - 75 - distField
    lInt = initFeld(2, sFelder[3], "y", "+", "START", lInt)
    x = 75 + distField
    y = SCR_SIZE - 75 - distField
    lInt = initFeld(2, sFelder[3], "y", "+", "START", lInt)

    # Zielfelder erstellen
    lInt = 0
    x = 75 + distField
    y = 75 + 5 * distField
    lInt = initFeld(4, zFelder[0], "x", "+", "ZIEL", lInt)

    lInt = 0
    x = 75 + 5 * distField
    y = 75 + distField
    lInt = initFeld(4, zFelder[1], "y", "+", "ZIEL", lInt)

    lInt = 0
    x = 75 + 9 * distField
    y = 75 + 5 * distField
    lInt = initFeld(4, zFelder[2], "x", "-", "ZIEL", lInt)

    lInt = 0
    x = 75 + 5 * distField
    y = 75 + 9 * distField
    lInt = initFeld(4, zFelder[3], "y", "-", "ZIEL", lInt)

    # sPos ist das Startfeld für die jeweiligen Farben
    global sPos
    sPos[0] = felder[0]
    sPos[1] = felder[10]
    sPos[2] = felder[20]
    sPos[3] = felder[30]


def initFiguren():
    for i in range(4):
        figuren[0].append(Figur(sFelder[0][i], 0))
    for i in range(4):
        figuren[1].append(Figur(sFelder[1][i], 1))
    for i in range(4):
        figuren[2].append(Figur(sFelder[2][i], 2))
    for i in range(4):
        figuren[3].append(Figur(sFelder[3][i], 3))


def zeichneFeld():
    for Feld in felder:
        pygame.draw.circle(screen, WHITE, Feld.pos, radField)

    for Feld in sFelder[0]:
        pygame.draw.circle(screen, RED, Feld.pos, radField)
    for Feld in sFelder[1]:
        pygame.draw.circle(screen, BLUE, Feld.pos, radField)
    for Feld in sFelder[2]:
        pygame.draw.circle(screen, GREEN, Feld.pos, radField)
    for Feld in sFelder[3]:
        pygame.draw.circle(screen, YELLOW, Feld.pos, radField)

    for Feld in zFelder[0]:
        pygame.draw.circle(screen, RED, Feld.pos, radField)
    for Feld in zFelder[1]:
        pygame.draw.circle(screen, BLUE, Feld.pos, radField)
    for Feld in zFelder[2]:
        pygame.draw.circle(screen, GREEN, Feld.pos, radField)
    for Feld in zFelder[3]:
        pygame.draw.circle(screen, YELLOW, Feld.pos, radField)

    pygame.draw.circle(screen, RED, sPos[0].pos, radField)
    pygame.draw.circle(screen, BLUE, sPos[1].pos, radField)
    pygame.draw.circle(screen, GREEN, sPos[2].pos, radField)
    pygame.draw.circle(screen, YELLOW, sPos[3].pos, radField)

    for i in range(len(figuren)):
        for fig in figuren[i]:
            match i:
                case 0:
                    pygame.draw.circle(screen, DRED, fig.feld.pos, radFigur)
                case 1:
                    pygame.draw.circle(screen, DBLUE, fig.feld.pos, radFigur)
                case 2:
                    pygame.draw.circle(screen, DGREEN, fig.feld.pos, radFigur)
                case 3:
                    pygame.draw.circle(screen, DYELLOW, fig.feld.pos, radFigur)

            if fig.selected:
                pygame.draw.circle(screen, BLACK, fig.feld.pos, radFigur, width=6)
            else:
                pygame.draw.circle(screen, BLACK, fig.feld.pos, radFigur, width=3)


initField()
initFiguren()

t = 0

while running:

    if not winner in farben:
        for i in range(4): # überprüfen ob es Gewinner gibt
            w = 0
            for fig in figuren[i]:
                if fig.feld.art == "ZIEL":
                    w += 1
            if w == 4:
                winner = farben[i]
                PLAYER == None
                    
        
    # Bot ist dran
    if turn % 4 != PLAYER:
        if not turn in wTurns: 
            wuerfelZahl = random.randint(1, 6)
            if winner == None: 
                img = font.render(str(wuerfelZahl), True, BLACK)
            else:
                img = font.render(winner + "\nGEWINNT", True, BLACK)

            pygame.draw.rect(screen, farbenW[turn % 4], wuerfel)
            screen.blit(img, (SCR_SIZE / 2 - wuerfelSize / 2, SCR_SIZE / 2 - 8))
            pygame.display.update()
            time.sleep(zZeit)

            wTurns.append(turn)
            movePrio.clear()
            for i in range(len(figuren)): # Prioritäten von Figuren festlegen
                for fig in figuren[i]:
                    movePrio.append(fig.setPrio(wuerfelZahl))
                
            c = 0
            for fig in figuren[turn%4]:#
                if not fig.canMove(wuerfelZahl): 
                    c += 1

            if c < 4:
                t = 0
                c = 0
                playable = [] # # #
                for i in range(len(figuren)):
                    for fig in figuren[i]:
                        playable.append(fig)
                        for p in movePrio:
                            if p > fig.prio:
                                playable.remove(fig)
                                break

                first = None
                abst = len(felder)
                for fig in playable:
                    if fig.feld.ind < sPos[fig.farbe].ind:
                        if sPos[fig.farbe].ind - fig.feld.ind < abst:
                            first = fig
                    elif len(felder) - fig.feld.ind + sPos[fig.farbe].ind < abst:
                        first = fig
                if first == None:
                    first = random.choice(playable)
                first.move(wuerfelZahl)

            elif c == 4 and t < 2: # wenn keine Figur bewegen kann, wird nochmal gewürfelt
                wTurns.remove(turn)
                t += 1
                c = 0
            elif t == 2: # wenn 3 mal gewürfelt wurde, geht es weiter
                turn += 1
                img = font.render("", True, BLACK)
                t = 0
                c = 0
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if wuerfel.x <= pygame.mouse.get_pos()[0] <= wuerfel.x + wuerfel.width and wuerfel.y <= pygame.mouse.get_pos()[1] <= wuerfel.y + wuerfel.height: # wenn der Würfel geklickt wird
                if turn % 4 == PLAYER and not turn in wTurns:
                    wuerfelZahl = random.randint(1, 6)
                    img = font.render(str(wuerfelZahl), True, BLACK)
                    wTurns.append(turn)
                    movePrio.clear()
                    for fig in figuren[turn % 4]:
                        movePrio.append(fig.setPrio(wuerfelZahl))
                        
                    c = 0
                    for fig in figuren[turn % 4]:#
                        if not fig.canMove(wuerfelZahl):
                            c += 1
                    if c < 4:
                        t = 0
                        c = 0
                    elif c == 4 and t < 2:
                        wTurns.remove(turn)
                        t += 1
                        c = 0
                    elif t == 2:                        
                        pygame.draw.rect(screen, farbenW[turn % 4], wuerfel)
                        screen.blit(img, (SCR_SIZE / 2 - wuerfelSize / 2, SCR_SIZE / 2 - 8))
                        pygame.display.update()
                        time.sleep(zZeit)
                        img = font.render("", True, BLACK)
                        turn += 1
                        pygame.draw.rect(screen, farbenW[turn % 4], wuerfel)
                        screen.blit(img, (SCR_SIZE / 2 - wuerfelSize / 2, SCR_SIZE / 2 - 8))
                        pygame.display.update()
                        t = 0
                        c = 0
                        
            else:
                for i in range(4):
                    for fig in figuren[i]: # wenn eine Figur geklickt wird
                        if fig.feld.pos[0] - radFigur <= pygame.mouse.get_pos()[0] <= fig.feld.pos[0] + radFigur and fig.feld.pos[1] - radFigur <= pygame.mouse.get_pos()[1] <= fig.feld.pos[1] + radFigur:
                            if turn in wTurns:
                                for i in range(4):
                                    for FigurD in figuren[i]:
                                        FigurD.selected = False
                                if turn % 4 == fig.farbe:
                                    fig.selected = True
                                    fig.move(wuerfelZahl)
                            break

        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()

    for fig in figuren[PLAYER]: # Figur wird bei hovern markiert, wenn sie bewegbar ist
        if math.dist([fig.feld.pos[0], fig.feld.pos[1]], [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]) <= radFigur:
            if turn in wTurns:
                for i in range(4):
                    for FigurD in figuren[i]:
                        FigurD.selected = False 
                if turn % 4 == fig.farbe:
                    fig.selected = True
                    for p in movePrio:
                        if p > fig.prio:
                            fig.selected = False
                    

    # Spielfeld und Würfel wird gezeichnet
    zeichneFeld()
    if not turn in wTurns:
        if not winner == None:
            img = font.render(winner + " GEWINNT", True, BLACK)
    pygame.draw.rect(screen, farbenW[turn % 4], wuerfel)
    screen.blit(img, (SCR_SIZE / 2 - wuerfelSize / 2, SCR_SIZE / 2 - 8))
    
    pygame.display.update()
    
