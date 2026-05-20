from cmu_graphics import *

from PIL import Image
import os
import random
'''Image Conversion'''
def loadPilImage(url):
    return Image.open(url)

def convertedImage(url):
    pilImage = loadPilImage(url)
    cmuIm = CMUImage(pilImage)
    return cmuIm
#Code adapted from https://www.cs.cmu.edu/~./112/notes/tp-related-demos/demo-pil-scaling.py


    

class Character:
    def __init__(self, app):
        self.app = app

        #Miner Character Sheet Link: https://www.deviantart.com/kostk2boss/art/custom-miner-sprites-252465211
        self.app.stepsPerSecond = 10
        self.app.currentDirection = 'down'
        self.app.imageIndex = 0
        
        self.app.isMoving = False
        

        self.app.moveSpeed = 10
        self.app.imageSwitchDelay = 1
        self.app.imageSwitchCounter = 0
        self.app.canPass = False
        self.app.isJumping = False
        self.app.posList = ['down']
        self.app.mined = False
        

    def passable(self, nextX, nextY):
    # Character size
        charWidth, charHeight = 55, 70
    
    # character's current position boundaries
        charLeft = nextX
        charRight = nextX + charWidth
        charTop = nextY
        charBottom = nextY + charHeight

    # Check if the character is within the grid's boundaries
        if charLeft < 0 or charRight > 1000 or charTop < 130 or charBottom > 1300:
            print(f"Out of bounds: ({nextX}, {nextY})")
            return False  # Block movement if out of bounds

    # Check for collisions with any block
        for row in self.app.grid:
            for block in row:
                blockLeft = block.x
                blockRight = block.x + 100
                blockTop = block.y
                blockBottom = block.y + 100

                isOverlapping = not (charRight <= blockLeft or 
                                 charLeft >= blockRight or 
                                 charBottom <= blockTop or 
                                 charTop >= blockBottom)

            # If overlapping with an impassable block, prevent movement
                if isOverlapping and not block.passable:
                    print(f"Collision detected with block at ({block.x}, {block.y}) - Type: {block.type}")
                    return False

        return True  

    
    def onStep(self):
        nextX, nextY = self.app.playerX, self.app.playerY

        if self.app.isMoving:
        # Update position based on direction
            
            if self.app.currentDirection == 'up':
                nextY -= self.app.moveSpeed
            elif self.app.currentDirection == 'down':
                nextY += self.app.moveSpeed
            elif self.app.currentDirection == 'left':
                nextX -= self.app.moveSpeed
            elif self.app.currentDirection == 'right':
                nextX += self.app.moveSpeed
        
       
            if not self.passable(nextX, nextY):
                print(f"Movement blocked at: ({nextX}, {nextY})")
                nextX, nextY = self.app.playerX, self.app.playerY  
          
            self.app.playerX, self.app.playerY = nextX, nextY

                
            self.app.imageSwitchCounter += 1
            if self.app.imageSwitchCounter >= self.app.imageSwitchDelay:
                self.app.imageIndex = 1 if self.app.imageIndex == 2 else 2
                self.app.imageSwitchCounter = 0

            

     
    def onKeyPress(self, key):
        
        if key == 'w':
            self.app.currentDirection = 'up'
            self.app.isMoving = True
        elif key == 's':
            self.app.currentDirection = 'down'
            self.app.imageIndex = 1
            self.app.isMoving = True
        elif key == 'a':
            self.app.currentDirection = 'left'
            self.app.imageIndex = 1
            self.app.isMoving = True
            self.app.posList.append('left')
        elif key == 'd':
            self.app.currentDirection = 'right'
            self.app.imageIndex = 1
            self.app.isMoving = True
            self.app.posList.append('right')
        elif key == 'space':
            self.app.mined = True
        
    def onKeyRelease(self, key):
        if key in ['w', 's', 'a', 'd']:
            
            if self.app.isJumping:
                self.app.playerY += 2*self.app.moveSpeed
                self.app.isJumping = False
            self.app.isMoving = False
            self.app.imageIndex = 0
      
    def draw(self):
        drawImage(self.app.sprite[self.app.currentDirection][self.app.imageIndex], self.app.playerX, self.app.playerY, width=55, height=70)


class Block:
    def __init__(self, app, x, y, blockType, passable, is_lowest):
        self.app = app
        self.x = x
        self.y = y
        self.type = blockType
        self.passable = passable
        self.is_lowest = is_lowest
 
    def draw(self):
        l = self.app.types
        for i in range(len(l)):
            if self.type == l[i]:
                
                drawImage(self.app.blocks[i], self.x,self.y,width = 100,height = 100)
                drawRect(self.x,self.y,100,100,fill=None, border='black',borderWidth=2)
       
      
    # Doors: https://www.dreamstime.com/opening-castle-door-animation-creating-video-games-opening-castle-door-animation-video-games-image141223792
    # Chests: https://www.pngitem.com/middle/JwomwR_pixel-art-chest-chest-pixel-art-hd-png/


class Item:
    def __init__(self, app,name, color, quantity):
        self.app = app
        self.name = name
        self.color = color
        self.quantity = quantity
    def update(self,change):
        self.quantity += change
    
 
'''Randomizing grid'''
def randomGrid(rows, cols):
    # Create the grid with all 'stone' blocks
    grid = [['stone' for _ in range(cols)] for _ in range(rows)]
    randBlock1 = random.randint(0,cols-1)
    randBlock2 = random.randint(0,cols-1)
    randBlock3 = random.randint(0,cols-1)

    
    r1b1 = -1
    r1b2 = -1
    r4b1 = -1
    r4b2 = -1
    r6b1 = -1
    r6b2 = -1

    for row in range(rows):
        for block in range(cols):
            #if abs(randBlock1-2) > 1 and abs(randBlock2-randBlock1) > 1 and abs(randBlock3-randBlock2) > 1
            if row == 0:
                if block == 1:
                    grid[row][block] = 'dirt'
            if row == 1:
                if grid[row-1][block] == 'dirt':
                    r1b1 = block
                    grid[row][block] = 'dirt'
            if row == 2:
                if block == randBlock1:
                    grid[row][block] = 'door1'
                    r1b2 = block
                    grid[row-1][block] = 'dirt'
                
                for block in range(2,randBlock1):
                    grid[row-1][block] = 'dirt'
            if row == 3:
                if grid[row-1][block] == 'door1':
                    r4b1 == block
                    grid[row][block] = 'dirt'
            if row == 4:
                if grid[row-1][block] == 'dirt':
                    grid[row][block] = 'dirt'
                for block in range(randBlock1,randBlock2):
                    grid[row][block] = 'dirt'
            if row == 5:
                if block == randBlock2:
                    grid[row][block] = 'door2'
                    
                    grid[row-1][block] = 'dirt'
            if row == 6:
                if grid[row-1][block] == 'door2':
                    grid[row][block] = 'dirt'
                for block in range(randBlock2,randBlock3):
                    grid[row][block] = 'dirt'
            if row == 7:
                if block == randBlock3:
                    grid[row][block] = 'locked'
                    grid[row-1][block] = 'dirt'
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'stone' and row > 0 and row != 2 and row != 5:
                num = random.choice([1,2,4,6,8])
                if num % 2 ==0:
                    grid[row][col] = 'dirt'
                elif num % 2 == 1:
                    grid[row][col] = 'stone'
    return grid
                

'''Game Setup'''

def onAppStart(app):
    game_reset(app)
    store_reset(app)
    inventory_reset(app)
    start_reset(app)
def help_reset(app):
    app.width = 600
    app.height = 600
def start_reset(app):
    app.width = 600
    app.height = 600
    app.buttonWidth = 300
    app.buttonHeight = 75
    app.startCenter = (300, 240)
    app.helpCenter = (300, 400)
    app.startMessage = "Start"
def inventory_reset(app):

    app.width = 1000
    app.height = 1000
    app.padding = 300
    app.startX = 250
    app.startY = 200
    app.invQuant1=0
    app.invQuant2=0
    app.invQuant3=0 
    app.invQuant4=0
    app.inventory = [
        Item(app,"Key 1", "brown",app.invQuant1 ),
        Item(app,"Key 2", "silver", app.invQuant2),
        Item(app,"Key 3", "gold", app.invQuant3),
        Item(app,"Time", "yellow", app.invQuant4)
    ]
def store_reset(app):
    app.strbackground = 'lightblue'
    app.currency = 0
    app.cost1 = 50
    app.cost2 = 100
    app.cost3 = 200
    app.strQuant1 = 1
    app.strQuant2 = 1
    app.strQuant3 = 1
    app.stocked1 = True
    app.stocked2 = True
    app.stocked3 = True
    app.insufficientFunds = False
    
def game_reset(app):
    app.width = 1000
    app.height = 1000
    app.timerSH = 0
    app.timerS = 0
    app.timerM = 0
    app.timerOn = False
    
    app.count = 0
    app.playerX = 260
    app.playerY = 130
    app.visitedSquares = []
    app.isMined = False
    app.status = 100
    app.gotTreasure = False
    app.hasKey1 = False
    app.hasKey2 = False
    app.hasKey3 = False

    

    '''Image Initialization'''
    app.baseUrl = '/Users/kevin/Desktop/Final Draft/src/'
    app.sprite = {
        'up': [convertedImage(f'{app.baseUrl}MinerU{i}.png') for i in range(3)],
        'down': [convertedImage(f'{app.baseUrl}MinerD{i}.png') for i in range(3)],
        'left': [convertedImage(f'{app.baseUrl}MinerL{i}.png') for i in range(3)],
        'right': [convertedImage(f'{app.baseUrl}MinerR{i}.png') for i in range(3)]
            
        }
    app.types = ['dirt','stone','mined','door1','door1opened',
            'door2','door2opened','locked','unlocked']
    app.blocks = [convertedImage(f'{app.baseUrl}{i}.png') for i in app.types]
    app.store = convertedImage(f'{app.baseUrl}Store2.png')
    app.entrance = convertedImage(f'{app.baseUrl}Entrance.png')
    app.sky = convertedImage(f'{app.baseUrl}Sky.png')
    app.backpack = convertedImage(f'{app.baseUrl}Backpack.png')
    app.title1 = convertedImage(f'{app.baseUrl}Title.png') #generated using https://textcraft.net/
    


    '''Links for images: 
    Store2:https://www.freepik.com/premium-vector/pixel-art-shop-store-front-with-awning-vector-build-8bit-game-white-background_26026635.html
    Entrance: https://www.pngkit.com/bigpic/u2w7e6q8e6o0e6i1/
    Stone:https://www.shutterstock.com/image-vector/pixel-art-stones-seamless-texture-1674347002
    Dirt: https://www.pinterest.com/pin/dirt-and-grass-tiles--852728510670823141/
    Mined: https://www.shutterstock.com/image-vector/pixel-minecraft-style-stone-block-background-1907532325?irclickid=ye9xt6W9txyKU04XKz2CIwXFUkCVVQQO0XdmQ80&irgwc=1&pl=77643-108110&utm_campaign=TinEye&utm_content=108110&utm_medium=Affiliate&utm_source=77643&utm_term=
    Sky: https://www.istockphoto.com/vector/pixel-art-game-background-grass-sky-and-clouds-gm1212239734-351853038
    Backpack: https://www.pixilart.com/art/backpack-32x32-a16d2c3e6e3881f
    '''
    
    app.placement = randomGrid(8,10)
    app.grid = [[Block(app,j*100,i*100 + 200,app.placement[i][j],False,True) 
                for j in range(10)] 
                for i in range (8)]
    app.miner = Character(app)
    
'''Game Functions'''


def game_drawGrid(app):
    for row in app.grid:
        for block in row:
            # Check if the player is currently on this block
            # (block.x <= app.playerX < block.x + 100) and (block.y <= app.playerY < block.y + 100)
            if (block.x, block.y) not in app.visitedSquares:
                block.draw() 
            else:
                if block.type == 'dirt' and app.isMined:
                    block.type = 'mined'
                    block.passable = True
                    
                    
                elif block.type == 'door1' and app.isMined and app.hasKey1:
                    block.type = 'door1opened'
                    block.passable = True
                elif block.type == 'door2' and app.isMined and app.hasKey2:
                    block.type = 'door2opened'
                    block.passable = True
                elif block.type == 'locked' and app.isMined and app.hasKey3:
                    block.type = 'unlocked'
                    block.passable = True
                block.draw()
                 
def game_checkVisited(app):
    size = 100

    for row in app.grid:
        for block in row:
            if (
                (
                (app.miner.app.currentDirection == 'down' and block.y >= app.playerY + 70 and block.y - app.playerY <= 100 and app.playerX >= block.x and app.playerX + 55 <= block.x + 100) or
                (app.miner.app.currentDirection == 'up' and app.playerY >= block.y + 100 and app.playerY - block.y <= 150 and app.playerX >= block.x and app.playerX + 55 <= block.x + 100 ) or
                (app.miner.app.currentDirection == 'left' and app.playerY >= block.y and app.playerY + 70 <= block.y + 100 and app.playerX - block.x <= 150 and app.playerX > block.x) or
                (app.miner.app.currentDirection == 'right' and app.playerY >= block.y and app.playerY + 70 <= block.y + 100 and block.x - app.playerX <= 100 and app.playerX < block.x )) 
                and (block.x,block.y) not in app.visitedSquares and app.isMined):
                app.visitedSquares.append((block.x,block.y))
                if block.type == 'dirt':
                    app.currency += 10
                elif block.type == 'locked' and app.hasKey3:
                    app.gotTreasure = True
                    app.inventory[3].update(1)
                    app.timerOn = False
                    setActiveScreen('inventory')
                
                #print(app.visitedSquares)
def timer(app):
    if app.timerOn:
        app.timerSH += 1
        if app.timerSH == 10:
            app.timerS += 1
            app.timerSH = 0
        if app.timerS == 60:
            app.timerM += 1
            app.timerS = 0
                       
def game_onStep(app):
    app.miner.onStep()
    game_checkVisited(app)
    enterStore(app)   
    app.count += 1
    if app.count == 60:
        changeSetting(app)
    timer(app)     

def game_drawSetting(app):
    if app.status > 0:
        drawImage(app.sky,0,0,width = 1000,height = 200) # sky
        drawImage(app.entrance, 60, 120, height=100, width=200) #cave entrance
        game_drawGrid(app)
        drawImage(app.store, 700, 55, width=200, height=150) #store
        drawImage(app.backpack,0,0,width = 50,height = 60)# inventory
        drawImage(app.title1, 500,40,align='center',width = 450,height=70)
        drawCircle(960,40,35,fill='grey',border='white')
        drawLabel('II',960,40,align = 'center',size=50,fill='white')
        drawRect(160,40,200,50,align='center',fill="white",border="grey",borderWidth = 2)
        drawLabel(f'Timer: {app.timerM:02d}:{app.timerS:02d}', 160, 40, size=30, bold=True)

        app.miner.draw()
    
def changeSetting(app):
    app.placement = randomGrid(8,10)
    app.grid = [
    [
        Block(
            app,j * 100,i * 100 + 200,
            "mined" if (
                app.playerX < (j + 1) * 100 and 
                app.playerX + 55 > j * 100 and 
                app.playerY < (i + 1) * 100 + 200 and 
                app.playerY + 70 > i * 100 + 200
            and app.placement[i][j] != 'stone') else app.placement[i][j],
            True if (
                app.playerX < (j + 1) * 100 and 
                app.playerX + 55 > j * 100 and 
                app.playerY < (i + 1) * 100 + 200 and 
                app.playerY + 70 > i * 100 + 200 and app.placement[i][j] != 'stone'
            ) else False,
            True
        )
        for j in range(10)
    ]
    for i in range(8)
    ]
    app.visitedSquares = []
    app.count = 0
def game_onKeyPress(app, key):
    app.miner.onKeyPress(key)
    if key == 'r':
        game_reset(app)
        store_reset(app)
        inventory_reset(app)
        start_reset(app)

        setActiveScreen('start')
    if key == 'space':
        app.isMined = True
    game_checkVisited(app)


def game_onKeyRelease(app, key):
    app.miner.onKeyRelease(key)
    if key == 'space':
        app.isMined = False
def enterStore(app):
    #Entering Store
     if (app.playerX >= 700 and app.playerX + 55 <= 900 and app.playerY + 70 <= 200 and app.isMined):
        print("Entering store")
        setActiveScreen('store')
        app.isMined = False
        app.miner.app.isMoving = False

def game_onMousePress(app,mouseX,mouseY):
    #Entering Inventory
    if mouseX >= 0 and mouseX <= 50 and mouseY >= 0 and mouseY <= 60:
        print("Entering inventory")
        setActiveScreen("inventory")
    if mouseX >= 920 and mouseX <= 1000 and mouseY >= 0 and mouseY <= 80:
        print("Entering pause")
        setActiveScreen('start')
        app.startMessage = "Resume"
        app.width = 600
        app.height = 600

'''Store Functions'''
def drawKey(x, y, color):
    # Draw the handle of the key
    drawRect(x - 30, y, 40, 40, fill=None, align='center', border=color,borderWidth = 6)  
    # Draw the pin of the key
    drawRect(x + 10, y, 50, 20, fill=color, align='center', border=color)  


#draw the store screen
def drawStore(app):
    # Header
    drawRect(0, 0, 1000, 100, fill='darkblue')
    drawLabel("Miner's Store", 500, 50, fill='white', size=40, bold=True)
    drawRect(0,0,40,1000,fill='darkblue')
    drawRect(960,0,40,1000,fill='darkblue')
    drawRect(0,980,1000,40,fill='darkblue')
    # Currency display
    
    
    currColor = 'red' if app.insufficientFunds else 'black'
    drawLabel(f"Currency: $ {app.currency}", 500, 150, size=32, bold=True, fill = currColor)
    # Out of stock
    if not app.stocked1:
        drawLabel(f"Key 1 is out of stock", 500, 250, size=32, fill='red',bold=True)
    if not app.stocked2:
        drawLabel(f"Key 2 is out of stock", 500, 250, size=32, fill='red',bold=True)
    if not app.stocked3:
        drawLabel(f"Key 3 is out of stock", 500, 250, size=32, fill='red',bold=True)
    # Items for sale
    drawLabel(f'Key 1: ${app.cost1}  Quantity: {app.strQuant1}', 400, 300, size=28, bold=True)
    drawKey(150, 300, 'brown')
    drawLabel(f'Key 2: ${app.cost2}  Quantity: {app.strQuant2}', 400, 500, size=28, bold=True)
    drawKey(150, 500, 'silver')
    drawLabel(f'Key 3: ${app.cost3}  Quantity: {app.strQuant3}', 400, 700, size=28, bold=True)
    drawKey(150, 700, 'gold')

    # Buttons
    drawRect(750, 280, 200, 80, fill='green',border='black')
    drawLabel('Buy Item 1', 850, 320, fill='silver', bold=True, size=24)

    drawRect(750, 480, 200, 80, fill='green',border='black')
    drawLabel('Buy Item 2', 850, 520, fill='silver', bold=True, size=24)

    drawRect(750, 680, 200, 80, fill='green',border='black')
    drawLabel('Buy Item 3', 850, 720, fill='silver', bold=True, size=24)

    drawRect(400, 900, 200, 80, fill='red',border='black')
    drawLabel('Exit Store', 500, 940, fill='silver', bold=True, size=24)

def store_onMousePress(app, mouseX, mouseY):
    
    if 750 <= mouseX and mouseX <= 950:
        if 280 <= mouseY and mouseY <= 360 and app.strQuant1 == 1:
            if app.currency >= app.cost1:
                app.strQuant1 -= 1
                app.inventory[0].update(1)
                app.currency -= app.cost1 
                app.hasKey1 = True
            else:
                app.insufficientFunds = True
        elif 280 <= mouseY and mouseY <= 360 and app.strQuant1 != 1:
            app.stocked1 = False
            print('Item 1 out of stock')
        elif 480 <= mouseY and mouseY <= 560 and app.strQuant2 == 1:
            if app.currency >= app.cost2:
                app.strQuant2 -= 1
                app.inventory[1].update(1)
                app.currency -= app.cost2 if app.currency > 0 else 0
                app.hasKey2 = True
            else:
                app.insufficientFunds = True
        elif 480 <= mouseY and mouseY <= 560 and app.strQuant2 != 1:
            app.stocked2 = False
            print('Item 2 out of stock')
        elif 680 <= mouseY and mouseY <= 760 and app.strQuant3 == 1:
            if app.currency >= app.cost3:
                app.strQuant3 -= 1
                app.inventory[2].update(1)
                app.currency -= app.cost3 if app.currency > 0 else 0
                app.hasKey3 = True
            else:
                app.insufficientFunds = True
        elif 680 <= mouseY and mouseY <= 760 and app.strQuant3 != 1:
            app.stocked3 = False
            print('Item 3 out of stock')
        
        
    elif 400 <= mouseX and mouseX <= 600 and 900 <= mouseY and mouseY <= 980:
        print('Exiting store...')
        setActiveScreen("game")

def store_onMouseRelease(app,mouseX,mouseY):
    app.insufficientFunds = False
    app.stocked1 = True
    app.stocked2 = True
    app.stocked3 = True
    

    app.stocked1 = True
    app.stocked2 = True
    app.stocked3 = True


'''Inventory Functions'''
def drawItem(app,x, y, item):
    drawRect(x, y, 200, 200, fill='white', border='black', borderWidth=2)
    if item:
        if item.name.startswith("Key"):
            drawKey(x + 100, y + 100, item.color)
        elif item.name == "Time":
            if app.gotTreasure:
                drawLabel(f"{app.timerM:02d}:{app.timerS:02d}", x + 100, y + 100, size=50, bold=True, fill='darkgray') 
                drawLabel('Please press "r" to reset game', 500,140,size = 40, bold=True,fill='darkgray')
                # Learned about timers from this link: https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
            else:
                drawLabel("?", x + 100, y + 100, size=50, bold=True, fill='darkgray')
        drawLabel(item.name, x + 100, y + 160, size=16, align="center", bold=True)
        drawLabel(f"x{item.quantity}", x + 100, y + 180, size=14, align="center")

def drawInventory(app):
    drawRect(0, 0, 1000, 100, fill='darkblue')
    drawLabel("Player Inventory", 500, 50, fill='white', size=40, bold=True)
    drawLabel(f"Currency: ${app.currency}", 900, 120, size=24, bold=True)
    startX, startY, padding = app.startX,app.startY, app.padding
    for i in range(2):
        for j in range(2):
            index = i * 2 + j
            item = app.inventory[index] if index < len(app.inventory) else None
            drawItem(app, startX + j * padding, startY + i * padding, item)
    drawRect(400, 850, 200, 80, fill='red') # Back to Game sign
    drawLabel('Back to Game', 500, 890, fill='white', bold=True, size=24)

def inventory_onMousePress(app, mouseX, mouseY):
    if 400 <= mouseX <= 600 and 850 <= mouseY <= 930:
        print('Back to game...')
        setActiveScreen('game')
def inventory_onKeyPress(app,key):
    if key == 'r':
        game_reset(app)
        store_reset(app)
        inventory_reset(app)
        start_reset(app)
        setActiveScreen('start')

'''Start Screen Functions'''
def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='brown')
    drawRect(300,120,400,80,align='center',fill='blue',border='white')
    drawImage(app.title1,300,120,width=400,height=80,align='center')
    
    for i in range(0,15):
        if i%2 == 0:
            drawRect(i*40,0,40,40,fill = "grey",border="white")
            drawRect(i*40,560,40,40,fill = "grey",border="white")
            drawRect(0,i*40,40,40,fill = "grey",border="white")
            drawRect(560,i*40,40,40,fill = "grey",border="white")
            
        else:
            drawRect(i*40,0,40,40,fill = "blue",border="white")
            drawRect(i*40,560,40,40,fill = "blue",border="white")
            drawRect(0,i*40,40,40,fill = "blue",border="white")
            drawRect(560,i*40,40,40,fill = "blue",border="white")
    #Start
    drawRect(app.startCenter[0],
             app.startCenter[1],
             app.buttonWidth, app.buttonHeight,align='center',
             fill='green', border='white', borderWidth=3)
    drawLabel(app.startMessage, app.startCenter[0], app.startCenter[1],
              size=30, fill='silver',font = 'monospace',bold=True)
    #Help
    drawRect(app.helpCenter[0],
             app.helpCenter[1],
             app.buttonWidth, app.buttonHeight,align='center',
             fill='blue', border='white', borderWidth=3)
    drawLabel('Help', app.helpCenter[0], app.helpCenter[1],
              size=30, fill='silver',font = 'monospace',bold=True)
    
def start_onMousePress(app, mouseX, mouseY):

    if ( 150 <= mouseX and mouseX <= 450 and
            203 <= mouseY and mouseY <= 278):
        
        setActiveScreen('game')
        app.timerOn = True
        app.width=1000
        app.height=1000
       
    elif (150 <= mouseX and mouseX <= 450 and
            363 <= mouseY and mouseY <= 438):
        setActiveScreen('help')  
def start_onKeyPress(app,key):
    if key == 'r':
        game_reset(app)
        store_reset(app)
        inventory_reset(app)
        start_reset(app)
        setActiveScreen('start')


'''Help Functions'''
def drawHelpScreen(app):
    drawRect(0,0,app.width,app.height,fill='lightblue')
    for i in range(0,15):
        if i%2 == 0:
            drawRect(i*40,0,40,40,fill = "grey",border="white")
            drawRect(i*40,560,40,40,fill = "grey",border="white")
            drawRect(0,i*40,40,40,fill = "grey",border="white")
            drawRect(560,i*40,40,40,fill = "grey",border="white")
            
            
        else:
            drawRect(i*40,0,40,40,fill = "blue",border="white")
            drawRect(i*40,560,40,40,fill = "blue",border="white")
            drawRect(0,i*40,40,40,fill = "blue",border="white")
            drawRect(560,i*40,40,40,fill = "blue",border="white")
    
    drawLabel('Help',300,100,size = 40,bold = True,fill='gray')
    drawLabel('Use "w","a","s","d" to move your character',300,160,size=16,align='center')
    drawLabel('Use space bar to mine or interact with objects',300,220,size =16,align='center')
    drawLabel('If stuck in row with a door, press "r" to reset',300,280,size=16,align='center')
    drawLabel('Remember, your goal is to reach the treasure as fast as possible',300,340,size=16,align='center')
    drawLabel('Be sure to constantly move around as to not get stuck in the wall',300,400,size=16,align='center')
    drawLabel('Last, but not least, have fun!',300,460,size=16,align='center')
    drawRect(200, 495, 200, 50, fill='green', border='black',borderWidth=3)
    drawLabel("Back to Menu",300,520,size=20,fill="white",align='center',bold=True)

def help_onMousePress(app,mouseX,mouseY):
    if mouseX >= 200 and mouseX <= 400 and mouseY >= 495 and mouseY <= 545:
        setActiveScreen('start')


    
'''redrawAll functions'''
def game_redrawAll(app):
    game_drawSetting(app)
def store_redrawAll(app):
    drawStore(app)
def inventory_redrawAll(app):
    drawInventory(app)
def start_redrawAll(app):
    drawStartScreen(app)
def help_redrawAll(app):
    drawHelpScreen(app)

def main():
    runAppWithScreens(initialScreen = 'start')

main()
cmu_graphics.run()