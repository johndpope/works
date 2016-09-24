from Component2 import *
#fps = 25

def main():
    global fpsclock, displaysurf, basicfont, bigfont
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode( (width,height))
    basicfont = pygame.font.Font('freesansbold.ttf',18)
    bigfont = pygame.font.Font('freesansbold.ttf',100)
    pygame.display.set_caption('Tetromino')
    #showTextScreen('Tetromino')
    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1,0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    import copy
    #mb.generateNewPiece()
    mb = Board()
    #fallfreq = 30 * (1.0/fps)
    lastfalltime = time.time()
    showStartLevel(level=1)
    while True:
        checkForQuit()
        if not mb.isValidPosition(mb.fallingpiece,None):
            print mb.fallingpiece.boardpos.x, mb.fallingpiece.boardpos.y
            print 'Game Over'
            return
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT and mb.isValidPosition(mb.fallingpiece,left):
                    mb.movePiece(left)
                elif event.key == K_RIGHT and mb.isValidPosition(mb.fallingpiece,right):
                    mb.movePiece(right)
                elif event.key == K_DOWN and mb.isValidPosition(mb.fallingpiece,down):
                    mb.movePiece(down)
                elif event.key == K_UP and mb.isValidPosition(mb.fallingpiece,up):
                    print 'rotating..'
                    mb.fallingpiece.rotate()
                elif event.key == K_SPACE:
                    while True:
                        if not mb.isValidPosition(mb.fallingpiece,down):
                            break
                        mb.movePiece(down)
            # move the piece fall faster with the down key
            # add code here ...
            if event.type == KEYUP:
                move = None
        # drawing everything on the screen
        if time.time() - lastfalltime > mb.fallfreq:
            if mb.isValidPosition(mb.fallingpiece,down):
                mb.movePiece(down)
            else: # landed
                mb.addToBoard(mb.fallingpiece)
                mb.removeCompleteLines()
                mb.generateNextPieces()
            if mb.completeLevel():
                level = mb.level + 1
                showStartLevel(level)
                mb = Board(level)
            lastfalltime = time.time()
                #mb.fallingpiece = None

        displaysurf.fill(bgcolor)
        mb.draw(displaysurf)
        pygame.display.update()
        fpsclock.tick(fps)
        #fpsclock.tick(15)

def terminate():
    pygame.quit(); sys.exit()

def checkForQuit():
    for e in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for e in pygame.event.get(KEYUP): # get all the KEYUP events
        if e.key == K_ESCAPE:
            terminate()
        pygame.event.post(e)
def showTextScreen(text):
    print text
    pygame.time.wait(5000)
def showStartLevel(level):
    bigfont = pygame.font.Font('freesansbold.ttf',50)
    textsurf = bigfont.render('Level %s' %level,True,blue)
    textrect = textsurf.get_rect()
    textrect.topleft = width/2 - 100,height/2-50
    displaysurf.fill(bgcolor)
    displaysurf.blit(textsurf,textrect)
    pygame.display.update()
    pygame.time.wait(5000)

if __name__ == '__main__':
    main()


