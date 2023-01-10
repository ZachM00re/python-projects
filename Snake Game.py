"""
Original version:
https://www.edureka.co/blog/snake-game-with-pygame/

Improved(?) by Geoffrey Matthews, 2022

Additional edits by Zachary Moore
CSCI 111, Fall 2022

Zach's Additions Include:
1. Poison apple mode
2. Editable starting snake length
3. 2-player mode (with game continuing after single loser)
4. Attempt to avoid food-snake overlap (occasionally misses one)

"""

import pygame
import random
 
# GLOBAL VARIABLES

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
gray = (100,100,100)
red = (213, 50, 80)
lightRed = (255,71,114)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128,0,128)

snake1HeadColor = red
snake1BodyColor = lightRed
player1Color = 'Red'
snake2HeadColor = black
snake2BodyColor = gray
player2Color = 'Black'
foodColor = green
poisonColor = purple
displayWidth = 666
displayHeight = 333

# Time & Visuals
cellSize = 20
speed = 8
pygame.init() # must be called before calling pygame methods:
clock = pygame.time.Clock()
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Modified Snake Game by Edureka')
gameOverFont = pygame.font.SysFont("bahnschrift", 25)
scoreFont = pygame.font.SysFont("comicsansms", 35)

# Game States
START = 'Start mode'
PLAYING = 'Playing mode'
MENU = 'Menu mode'
LOSER = 'Both Players Loser mode'
QUIT = 'Quit mode'
gameMode = START


def initialize(gameStart=True):
    global snake1,snake2,startSnakeLength,nSnakes,poisonCount,poisonOn,poisonApples,poisonWord
    global START, PLAYING, MENU, LOSER, QUIT, loser1, loser2
    global x1,y1,x2,y2,x1Change,y1Change,x2Change,y2Change
    global foodx, foody, displayWidth, displayHeight

    x1 = midCell(displayWidth)  # snake 1 starting position
    y1 = midCell(displayHeight) // 2

    x2 = midCell(displayWidth)  # snake 2 starting position
    y2 = midCell(displayHeight) + midCell(displayHeight) // 2

    startSnakeLength = 5
    nSnakes = 1
    
    x1Change = cellSize  # snake 1 initialized moving to right at start (avoids error discussed in lab instructions)
    y1Change = 0

    x2Change = -cellSize # snake 2 initialized moving to left at start (avoids error discussed in lab instructions)
    y2Change = 0
 
    snake1 = [(x1,y1)]
    snake2 = [(x2,y2)]
 
    poisonOn = False
    poisonApples = False
    poisonWord = 'No'
    poisonCount = random.randint(10*speed,20*speed)

    loser1 = False  # true when player 1 has lost
    loser2 = False  # true when player 2 has lost


def loser(n):
    global loser1, loser2, snake1, snake2
    
    if n == 1:
        loser1 = True
        snake1 = []

    if n == 2:
        loser2 = True
        snake2 = []

def itemSnakeOverlap(itemx,itemy):   # places food/poison apples where not overlapping with snake body (works most of the time, but still occasionally get overlap)
    global snake1,snake2
    
    if nSnakes == 1 and ( (itemx,itemy) not in snake1 ):
        x = itemx
        y = itemy
        
    elif nSnakes == 2 and (itemx,itemy) not in snake1 and (itemx,itemy) not in snake2:
        x = itemx
        y = itemy
        
    else:
        x = randomCell(displayWidth)
        y = randomCell(displayHeight)
        itemSnakeOverlap(x,y)

    return x,y

    
def createInitialSnake(length):
    global snake1,snake2,x1,x2,y1,y2
    
    x1Next = x1 - cellSize
    x2Next = x2 + cellSize
    
    for i in range(length):  # initializes snakes in opposing directions
        snake1.insert(0,(x1Next,y1))
        x1Next = x1Next - cellSize
        snake2.insert(0,(x2Next,y2))
        x2Next = x2Next + cellSize

    
def drawScore(score,side,snakeColor,teamName):
    global display

    value = scoreFont.render(teamName + " Score: " + str(score),
                              True,   # antialias
                              snakeColor) # color
    if side == 'LEFT':
        display.blit(value, [0, 0])
        
    if side == 'RIGHT':
        display.blit(value, [displayWidth // (3/2), 0])


def drawCircle(pos, color):
    global cellSize, display
    
    radius = cellSize//2
    pos = (pos[0]+radius, pos[1]+radius)
    pygame.draw.circle(display, color, pos, radius)

 
def drawSnake(snake,headColor,bodyColor):
    
    for pos in snake:
        drawCircle(pos,bodyColor)
    drawCircle(pos,headColor)


def drawFood(x, y, color):
    drawCircle((x,y), color)

 
def message(firstLine,menuLine,snakeLengthLine,snakeNumberLine,poisonAppleLine,playGameLine,quitLine,color):
    global display, displayWidth, displayHeight

    mesg = gameOverFont.render(firstLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3])

    mesg = gameOverFont.render(menuLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3 + cellSize])

    mesg = gameOverFont.render(snakeLengthLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3 + 2*cellSize])

    mesg = gameOverFont.render(snakeNumberLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3 + 3*cellSize])

    mesg = gameOverFont.render(poisonAppleLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3 + 4*cellSize])

    mesg = gameOverFont.render(playGameLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3 + 5*cellSize])

    mesg = gameOverFont.render(quitLine, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3 + 6*cellSize])


def randomCell(totalSize):
    global cellSize
    
    return cellSize*random.randint(0,(totalSize//cellSize)-1)


def midCell(totalSize):
    global cellSize
    
    n = (totalSize//cellSize)//2
    return cellSize*n


def onBoard(x, y):
    global displayWidth, displayHeight
    
    onWidth = 0 <= x < displayWidth
    onHeight = 0 <= y < displayHeight
    return onWidth and onHeight


def drawMenu(display,firstLine,menuline,snakeLengthLine,snakeNumberLine,poisonAppleLine,playGameLine,quitLine,snake1Score,snake2Score,prevGame2Players):
    display.fill(blue)
    message(firstLine,menuline,snakeLengthLine,snakeNumberLine,poisonAppleLine,playGameLine,quitLine,black)
    
    if snake1Score != ' ':
        drawScore(snake1Score,'LEFT',snake1HeadColor,player1Color)
    
    if snake2Score != ' ' and prevGame2Players == True:  # only displays player two score if previous game 2-player
        drawScore(snake2Score,'RIGHT',snake2HeadColor,player2Color)


def gameLoop():
    global gameMode,snake1,snake2,startSnakeLength,nSnakes,prevGame2Players,poisonCount,poisonOn,poisonApples,poisonWord,poisonX,poisonY
    global START, PLAYING, MENU, LOSER, QUIT, loser1,loser2
    global x1,x2,y1,y2,x1Change,y1Change,x2Change,y2Change,snake1Score,snake2Score
    global foodx, foody, display, speed, cellSize, foodColor
        
    while gameMode != QUIT:
        clock.tick(speed)

        # HANDLING USER INPUT

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameMode = QUIT

            if event.type == pygame.KEYDOWN:
                        
                if gameMode == PLAYING:
                    
                    if loser1 == False:   # shuts off player 1 controls when they lose
                        
                        if event.key == pygame.K_LEFT:
                            x1Change = -cellSize
                            y1Change = 0
                        elif event.key == pygame.K_RIGHT:
                            x1Change = cellSize
                            y1Change = 0
                        elif event.key == pygame.K_UP:
                            y1Change = -cellSize
                            x1Change = 0
                        elif event.key == pygame.K_DOWN:
                            y1Change = cellSize
                            x1Change = 0
                            
                    if loser2 == False:   # shuts off player 2 control when they lose
                        
                        if event.key == pygame.K_a:
                            x2Change = -cellSize
                            y2Change = 0
                        elif event.key == pygame.K_d:
                            x2Change = cellSize
                            y2Change = 0
                        elif event.key == pygame.K_w:
                            y2Change = -cellSize
                            x2Change = 0
                        elif event.key == pygame.K_s:
                            y2Change = cellSize
                            x2Change = 0
                
                if gameMode == MENU:
                    
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_LEFT:
                            
                            if startSnakeLength > 1:  # minimum initialized snake length is 1 (+ head)
                                startSnakeLength = startSnakeLength - 1
                                
                        elif event.key == pygame.K_RIGHT:
                            
                            if startSnakeLength < (displayWidth // cellSize) // 2:  # limits snake length in order to fit on screen
                                startSnakeLength = startSnakeLength + 1
                                
                        elif event.key == pygame.K_s:
                            
                            if nSnakes == 1:
                                nSnakes = 2
                            else:
                                nSnakes = 1
                                
                        elif event.key == pygame.K_p:
                            poisonOn = not poisonOn
                            
                            if poisonApples == True:
                                poisonApples == False
                            else:
                                poisonApples = True
                                
                            if poisonWord == 'No':
                                poisonWord = 'Yes'
                            else:
                                poisonWord = 'No'
    
                        elif event.key == pygame.K_c:
                            createInitialSnake(startSnakeLength)
                            snake1Score = startSnakeLength 
                            snake2Score = startSnakeLength

                            if nSnakes == 1:  # determines whether to include snake 2 score in menu mode
                                prevGame2Players = False
                            else:
                                prevGame2Players = True

                            foodx = randomCell(displayWidth)  # sets initial food location
                            foody = randomCell(displayHeight)
                            foodx,foody = itemSnakeOverlap(foodx,foody)
                            
                            if poisonApples == True: # sets initial poison apple location
                                poisonX = randomCell(displayWidth)
                                poisonY = randomCell(displayHeight)
                                poisonX,poisonY = itemSnakeOverlap(poisonX,poisonY)
                                
                            gameMode = PLAYING
                            
                        elif event.key == pygame.K_q:
                            gameMode = QUIT



        # GAME STATES
        
        if gameMode == QUIT:
            return()
        
        if gameMode == PLAYING:

            # Determining When All Players Have Lost

            if nSnakes == 1 and loser1 == True:
                gameMode = LOSER
                continue
            
            if loser1 == True and loser2 == True:
                gameMode = LOSER
                continue


            # Snake 1 Losing Conditions in 1-Player Mode

            if loser1 == False:
                if not onBoard(x1, y1):  # player 1 loses if snake 1 hits edge
                    loser(1)
                
                for x in snake1[:-1]:   # player 1 loses if head of snake 1 runs into body of snake 1
                    if x == snake1[-1]:
                        loser(1)
                        break


            # Updating Snake 1 Position
            
            x1 += x1Change 
            y1 += y1Change
            snake1.append((x1,y1))


            # Snake 1 Food Interaction

            if (x1 == foodx and y1 == foody):   # increases snake 1 length when it collects food
                foodx = randomCell(displayWidth)
                foody = randomCell(displayHeight)
                foodx,foody = itemSnakeOverlap(foodx,foody)

            else:
                 del snake1[0]   # retains snake 1 length

                 
            # Managing 2-Player Games
            
            if nSnakes == 2:
                
                if loser1 == False and loser2 == False:
        
                    if snake1[-1] == snake2[-2] and snake1[-2] == snake2[-1]:  # both players lose if a head-on collision occurs (found relationship by printing head coords)
                        loser(1)
                        loser(2)

                    for x in snake1[:-1]:    # player 2 loses if head of snake 2 runs into body of snake 1
                        if x == snake2[-1]:
                            loser(2)
                            break
                    
                    for x in snake2[:-1]:   # player 1 loses if head of snake 1 runs into body of snake 2
                        if x == snake1[-1]:
                            loser(1)
                            break
                        

                # Snake 2 Losing Conditions
                
                if loser2 == False:
                    if not onBoard(x2, y2):  # player 2 loses if snake 2 hits edge
                        loser(2)

                    for x in snake2[:-1]:    # player 2 loses if head of snake 2 runs into body of snake 2
                        if x == snake2[-1]:
                            loser(2)
                            break


                    # Updating Snake 2 Position
                    
                    x2 += x2Change
                    y2 += y2Change
                    snake2.append((x2,y2))

                    
                    # Snake 2 Food Interaction

                    if (x2 == foodx and y2 == foody):   # increases snake 2 length by 1 when it collects food
                        foodx = randomCell(displayWidth)
                        foody = randomCell(displayHeight)
                        foodx,foody = itemSnakeOverlap(foodx,foody)
        
                    else:
                        del snake2[0]  # retains snake 2 length



            # Handling Poison Apple Behavior

            poisonCount = poisonCount - 1  # determines poison apple life cycle
            
            if poisonOn == True and poisonApples == True:  # true when user has selected poison apple mode and time for poison apple to appear 

            
                if loser1 == False and snake1[-1] == (poisonX,poisonY):  # player 1 loses if snake 1 hits poison apple
                    poisonOn = not poisonOn  # poison apple disappears after being hit
                    loser(1)

                if loser2 == False and nSnakes == 2:
                    if snake2[-1] == (poisonX,poisonY):  # player 2 loses if snake 2 hits poison apple
                        poisonOn = not poisonOn  # poison apple disappears after being hit
                        loser(2)

            if poisonCount == 0:
                poisonX = randomCell(displayWidth)
                poisonY = randomCell(displayHeight)
                poisonX,poisonY = itemSnakeOverlap(poisonX,poisonY)
                poisonCount = random.randint(10*speed,20*speed) # creates pseudo-random lifetime for poison apples
                poisonOn = not poisonOn



            # Updating Game Visuals 
            
            display.fill(blue)
            drawFood(foodx,foody,foodColor)

            if loser1 == False:  # sets score to body length of snake (not including head, as decided by code given in lab instructions)
                snake1Score = len(snake1)-1
                
            if loser2 == False:
                snake2Score = len(snake2)-1
                
            drawScore(snake1Score,'LEFT',snake1HeadColor,player1Color)

            if nSnakes == 2:
                drawScore(snake2Score,'RIGHT',snake2HeadColor,player2Color)
            
            if poisonOn == True and poisonApples == True:
                drawFood(poisonX,poisonY,poisonColor)
                
            if loser1 == False:
                drawSnake(snake1,snake1HeadColor,snake1BodyColor)
                
            if nSnakes == 2 and loser2 == False:
                drawSnake(snake2,snake2HeadColor,snake2BodyColor)
        
            pygame.display.update()
            

        # Initializing Visuals for Start Screen (before first game)

        if gameMode == START:
            firstLine = 'Welcome to Snake! '
            snake1Score = ' '
            snake2Score = ' '
            prevGame2Players = False
            gameMode = MENU


        # Updating Menu Visuals
        
        if gameMode == MENU:
            menuLine = 'Menu:'
            snakeLengthLine = '(L/R Arrows) Change Snake Length: ' + str(startSnakeLength)
            snakeNumberLine = '(S) Change Number of Snakes: ' + str(nSnakes)
            poisonAppleLine = '(P) Poison Apples: ' + poisonWord
            playGameLine = '(C) Play Game'
            quitLine = '(Q) Quit'

            drawMenu(display,firstLine,menuLine,snakeLengthLine,snakeNumberLine,poisonAppleLine,playGameLine,quitLine,snake1Score,snake2Score,prevGame2Players)
            pygame.display.update()

            
        if gameMode == LOSER:
            firstLine = 'Game Over'
            gameMode = MENU
            initialize()
        

def main():
    initialize()
    gameLoop()
    
if __name__ == '__main__':
    
    try:
        main()
    finally:
        pygame.quit()
        
