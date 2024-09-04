"""
Battleship Project
Name:MANDA AKSHAY KUMAR REDDY
Roll No:2023501060
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["board_size"] = 500
    data["cell_size"] = data["board_size"] // data["rows"]
    data["computer_ship"] = 5
    data["user_ship"] = 0
    data["computer_board"] = emptyGrid(data["rows"], data["cols"])
    data["user_board"] = emptyGrid(data["rows"], data["cols"])
    data["computer"] = addShips(data["computer_board"], data["computer_ship"])
    data["user"] = addShips(data["user_board"], data["user_ship"])
    data["winner"] = None
    data["temp_ship"] = []
    data["turns"]=0
    data["max_turns"]=50
    return data



'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,compCanvas,data["computer_board"],showShips=False)
    drawGrid(data,userCanvas,data["user_board"],showShips=True)
    drawShip(data, userCanvas, data["temp_ship"])                
    drawGameOver(data,canvas=userCanvas)                    
    return None


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return":
        makeModel(data)
    return None


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if board == "user":
        if data["user_ship"] < 5:  # Ensure the user can place ships
            cell = getClickedCell(data, event)
            if cell is not None:
                clickUserBoard(data, cell[0], cell[1])
        else:
            print("You've already placed 5 ships. Start playing the game!")
    elif board == "comp" and data["user_ship"]==5:
            cell=getClickedCell(data,event)
            if cell is not None:
                runGameTurn(data,cell[0],cell[1])
    

#### STAGE 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for _ in range(rows):
        L = []
        for _ in range(cols):
            L.append(EMPTY_UNCLICKED)
        grid.append(L)    
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    rows = random.randint(1,8)
    cols = random.randint(1,8)
    a=random.randint(0,1)
    l =[]
    if a==0:
        l.append([rows-1,cols])
        l.append([rows,cols])
        l.append([rows+1,cols])
    elif a==1:
        l.append([rows,cols-1])
        l.append([rows,cols])
        l.append([rows,cols+1])

    return l


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for x,y in ship:
        if grid[x][y] != EMPTY_UNCLICKED:
            return False
        
    return True
        
    


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while count<numShips:
        ship = createShip()
        if checkShip(grid,ship):
            for x,y in ship:
                grid[x][y] = SHIP_UNCLICKED
            count=count+1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):

    #function to draw grid for user and computer

    rows = data["rows"]
    cols = data["cols"]
    cell_size = data["cell_size"]
    for row in range(rows):
        for col in range(cols):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            if grid[row][col] == EMPTY_UNCLICKED:
                canvas.create_rectangle(x0,y0,x1,y1,fill = "blue", outline = "black")   

            elif grid[row][col] == SHIP_UNCLICKED and showShips == True:
                canvas.create_rectangle(x0,y0,x1,y1,fill = "yellow",outline = "black")  

            elif  grid[row][col] == SHIP_UNCLICKED and showShips == False :
                canvas.create_rectangle(x0,y0,x1,y1,fill = "blue",outline = "black")    

            elif grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(x0,y0,x1,y1,fill = "red",outline = "black")     

            elif grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(x0,y0,x1,y1,fill = "white",outline = "black")  
    canvas.pack()
    return 



### STAGE 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1] ==ship[1][1]==ship[2][1]:
        if abs(ship[0][0]-ship[1][0]) == abs(ship[1][0]-ship[2][0])== 1:
            return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[1][0]==ship[2][0]:
            if abs(ship[0][1]-ship[1][1])== abs(ship[1][1]-ship[2][1])==1: 
                return True
    return False        


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    rows = data["rows"]
    cols = data["cols"]
    cell_size = data["cell_size"]
    x,y = event.x,event.y
    for row in range(rows):
        for col in range(cols):

            x0 = col * cell_size              

            y0 = row * cell_size              

            x1 = x0 + cell_size               

            y1 = y0 + cell_size               

            if x0<= x <x1 and y0 <= y <y1:    

                return [row,col]
    return None
    


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    rows = data["rows"]
    cols = data["cols"]
    cell_size = data["cell_size"]
    for row,col in ship:
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        canvas.create_rectangle(x1,y1,x2,y2,fill = "white",outline = "black")  
    return None
    
    
'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
     if len(ship)!=3:               
        return False
     for row,col in ship:
        if grid[row][col] == SHIP_CLICKED:       
            return False
        if checkShip(grid,ship)== False or isVertical(ship)== False and isHorizontal(ship)== False:    
            return False 
        return True
     


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if data["user_ship"]==5:   
        return    
    else:   
        temp_ship = data["temp_ship"]
        if shipIsValid(data["user_board"],temp_ship):             
            for row,col in temp_ship:
                data["user_board"][row][col] = SHIP_UNCLICKED        
            data["user_ship"]+=1                                
            data["temp_ship"]=[]
        else:
            print("Invalid ship placement. Try again")        
            data["temp_ship"]=[]

    if data["user_ship"]==5:                            
        print("Start playing the game")
    
    return None




'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    temp_ship = data["temp_ship"]
    if  [row,col] in temp_ship:      
        return 
    
    temp_ship.append([row,col])

    if len(temp_ship)==3:             
        placeShip(data)

    return None


### STAGE 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[int(row)][int(col)]==SHIP_UNCLICKED:
       board[int(row)][int(col)]=SHIP_CLICKED
       if isGameOver(board):                     
           data["winner"] = player
    if board[int(row)][int(col)]==EMPTY_UNCLICKED:
       board[int(row)][int(col)]=EMPTY_CLICKED
    return
    


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["computer_board"][row][col]== SHIP_CLICKED or data["computer_board"][row][col]== EMPTY_CLICKED:
        return
    else: 
        updateBoard(data,data["computer_board"],row,col,player="user")

    cell = getComputerGuess(data["user_board"])
    updateBoard(data,data["user_board"],cell[0],cell[1],player="comp")
    data["turns"] +=1                                                       #
    if data["turns"] == data["max_turns"]:                                 
        data["winner"] = "draw"
    return

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row = random.randint(0, 9)  # Update to generate random indices between 0 and 9
        col = random.randint(0, 9)  # Update to generate random indices between 0 and 9

        if board[row][col] == SHIP_CLICKED or board[row][col] == EMPTY_CLICKED:
            continue
        else:
            return [row, col]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in board:
        for cell in row:
            if cell == SHIP_UNCLICKED:   
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] == "user":
        canvas.delete("all")
        canvas.create_text(300,40,text = "CONGRATULATIONS!!! YOU'VE WON THE GAME",fill = "red")
        canvas.create_text(300,80,text = "Press enter to play again",fill = "red")

    elif data["winner"] == "comp":
        canvas.delete("all")
        canvas.create_text(300,40,text = "SORRY, YOU LOST TO THE COMPUTER",fill = "red")
        canvas.create_text(300,80,text = "Press enter to play again",fill = "red")

    elif data["winner"] == "draw":
        canvas.delete("all")
        canvas.create_text(300,40,text = "YOU'RE OUT OF MOVES AND REACHED THE DRAW",fill = "red")
        canvas.create_text(300,80,text = "Press enter to play again",fill = "red")

    else:
        return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    test.stage1Tests()
    
    

    

    

    ## Uncomment these for STAGE 2 ##
    
    print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    test.stage2Tests()  

    ## Uncomment these for STAGE 3 ##
    
    print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    test.stage3Tests()


    

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
