# Kienen Wayrynen
# Connect 4
# November 18, 2014

from random import *
from tkinter import *
from time import *

WIDTH = 650
HEIGHT = 580
DIAMETER = 90

class Board:
    """ a datatype representing a C4 board
        with an arbitrary number of rows and cols
    """
    def __init__(self,width,height,window):
        
        #THIS WILL BE THE BOARD
        
        self.width = width
        self.height = height
        self.data = []
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.draw = Canvas(window, width=WIDTH,height=HEIGHT, bg='yellow')
        self.draw.bind("<Button-1>", self.mouse)
        self.draw.pack()        
        
        #QUIT BUTTON
        
        self.qButton = Button(self.frame, text = "Quit", fg="red", \
                              command=self.quitGame)
        self.qButton.pack(side=RIGHT)
        
        #NEW GAME BUTTON
        
        self.newGameButton = Button(self.frame, text = "New Game", fg="red",\
                                    command = self.clear)
        self.newGameButton.pack(side=RIGHT)
        
        #DIFFICULTY SLIDER
        
        self.difficultySlider = Scale(self.frame, \
	                              orient=HORIZONTAL, variable=IntVar,\
	                              showvalue=0, from_=1,\
	                              to=6, tickinterval=1, length=200, \
	                              label="Easy <---------------------> Hard", \
	                              command=self.changePly)
        self.difficultySlider.set(3)
        self.difficultySlider.pack(side=TOP)
        
        
        self.message = self.draw.create_text(90, HEIGHT-5, text="Place four connecting checkers in a row to win. Black First!", \
                                              anchor="w", font="Courier 15")        
        
        for row in range( self.height ): # 6
            boardRow = []
            for col in range( self.width ): # 7
                boardRow += [' ']   # add a space to this row
            self.data += [boardRow]        

        #LINES
	
        """self.line1 = self.draw.create_line(110,0,110,480,fill="black",width=3)
        self.line2 = self.draw.create_line(220,0,220,480,fill="black",width=3)
        self.line3 = self.draw.create_line(330,0,330,480,fill="black",width=3)
        self.line4 = self.draw.create_line(440,0,440,480,fill="black",width=3)
        self.line5 = self.draw.create_line(550,0,550,480,fill="black",width=3)
        self.line6 = self.draw.create_line(660,0,660,480,fill="black",width=3)
        self.line7 = self.draw.create_line(0,480,775,480,fill="black",width=3)
        self.line8 = self.draw.create_line(0,18,775,18,fill="black",width=3)
        self.line9 = self.draw.create_line(767,18,767,480,fill="black",width=3)
        self.line10 = self.draw.create_line(19,18,19,480,fill="black",width=3)"""        
        
        #CIRCLES

        initialColor = "white"
        y = 15
        self.circles = []
        self.colors = []
        self.gameOver = False
        for row in range(self.height):
            x = 12
            d = 100
            cRow = []
            colorRow = []
            for col in range(self.width):
                cRow += [self.draw.create_oval(x,y,x+DIAMETER,y+DIAMETER,
                                               fill=initialColor)]
                colorRow += [initialColor]
                x += DIAMETER
            self.circles += [cRow]
            self.colors += [colorRow]
            y += DIAMETER
            
    def changePly(self, ply):
        self.aiPlayer.ply = self.difficultySlider.get()
        self.clear()
        
    def playGUI(self,aiPlayer):
        self.aiPlayer = aiPlayer
                
    def quitGame(self):
        self.window.destroy()
    
    def mouse(self,event):        
        #self.window.bell()
        #print("x = %i, y = %i" % (event.x,event.y))
        col = int(event.x/DIAMETER)
        if self.gameOver == False:
            if self.allowsMove(col):
                row = self.addMove(col,"X")
                self.draw.itemconfig(self.circles[row][col], fill= "black")
                self.draw.itemconfig(self.message,text="Checker added, place another")
                if self.winsFor("X"):
                    self.draw.itemconfig(self.message,text = "Black Wins!")
                    self.gameOver = True
                    return
                if self.isFull():
                    self.draw.itemconfig(self.message,text = "Tie, board is full")
                    self.gameOver = True
                    return
                self.window.update()
                sleep(.1)
                RedMove = self.aiPlayer.nextMove(self)
                row = self.addMove(RedMove,"O")
                self.draw.itemconfig(self.circles[row][RedMove], fill= "red")
                if self.winsFor("O"):
                    self.draw.itemconfig(self.message,text = "Red Wins!")
                    self.gameOver = True
                    return
                if self.isFull():
                    self.draw.itemconfig(self.message,text = "Tie, board is full")
                    self.gameOver = True
                    return
            else:
                self.draw.itemconfig(self.message,text = "Unallowed Move")
                self.window.update()    

    def __repr__(self):
        #print out rows & cols
        s = ''   # the string to return
        for row in range( self.height ):
            s += '|'   # add the spacer character
            for col in range( self.width ):
                s += self.data[row][col] + '|'
            s += '\n'
        #print out separator
        s+= '--'*self.width + '-\n'
        # print out indices of each column
        # using mod if greater than 9,
        # for spacing issues
        for col in range( self.width ):
            s += ' ' + str(col % 10)
        s += '\n'
        return s       # return it        
		 
    def addMove(self, col, ox):
        if self.allowsMove(col):
            for row in range( self.height ):
                if self.data[row][col] != ' ':
                    self.data[row-1][col] = ox
                    return row - 1		
            self.data[self.height-1][col] = ox
            return self.height-1
        
    def delMove(self, col):
        for row in range(self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                return
       
    def clear(self):
        for row in range(0, self.height ):
            for col in range(0,self.width ):
                self.data[row][col] = ' '
                self.draw.itemconfig(self.circles[row][col],fill="white")
                self.draw.itemconfig(self.message,text="Place four connecting checkers in a row to win. Black First!")
                self.gameOver = False                
    
    def allowsMove(self,col):
        col=int(col)
        if 0 <= col < self.width:
            return self.data[0][col]=='   
    
    def scoresFor ( self , b , ox , ply ):
        score = []
        for col in range (s.width):
            if b.allowsMove(col):
                b.addMove (col,ox)    # make move
                if b.winsFor(ox):     # check did I win
                    score += [100]
                elif ply == 1 :       # if ply = 1
                    score += [50]
                else:                 # op = opposite player
                    if ox =="X":
                        op = "O"
                    else:
                        op = "X"
                    oplist = []
                    oplist = self.scoresFor(b,op,ply-1)
                    score += [100 - max(oplist)]
                b.delMove(col)       #remove move
            else:
                score += [-1]
        return score    
    
    def winsFor(self, ox):
    # check for horizontal wins
        for row in range(0,self.height):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                    return True
		
    # check for vertical wins
        for col in range(0,self.width):
            for row in range(0,self.height-3):
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    return True
   
    # check for slanted wins (NW -> SE)
        for row in range(3,self.height):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row-1][col+1] == ox and \
                self.data[row-2][col+2] == ox and \
                self.data[row-3][col+3] == ox:
                    return True
    
    # check for slanted wins (NE -> SW)
        for row in range(0,self.height-3):
            for col in range(3,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    return True  
        return False

    def isFull(self):
        for col in range(0, self.width):
            if self.allowsMove(col):
                    return False
        return True   

class Player:
    
    ''' generates AI moves given a board'''
        
    def __init__(self,ox,ply):
        self.ply = ply
        #self.tbt = tbt
        self.ox = ox
    
    def oppCh(self,ox): # opposing checker
        if ox == "x":
            next = "o"
        else:
            next = "x"
        return next
    
    def scoresFor ( self , s , ox , ply ):
        score = []
        for col in range (s.width):
            if s.allowsMove(col):
                s.addMove (col,ox)    # make move
                if s.winsFor(ox):     # check did I win
                    score += [100]
                elif ply == 1 :       # if ply = 1
                    score += [50]
                else:                 # op = opposite player
                    if ox =="X":
                        op = "O"
                    else:
                        op = "X"
                    oplist = []
                    oplist = self.scoresFor(s,op,ply-1)
                    score += [100 - max(oplist)]
                s.delMove(col)       #remove move
            else:
                score += [-1]
        return score
        
    def tieBreakMove(self,score):      # tbt Tie Break Type
        if self.tbt == 'LEFT':
            return
        if self.tbt == 'RIGHT':
            return
        if self.tbt == 'RANDOM':
            return
    
    def nextMove (self,b):
        L = self.scoresFor(b,self.ox,self.ply)
        print(L)
        highScore = max(L)
        columnList = []
        for i in range(b.width):
            if L[i] == highScore:
                columnList.append(i)
        print(L)
        print(highScore)
        return choice(columnList)
       
	# to play the game with your self uncomment this code
    """def hostGame(self):
        while True:    
            print(self)
            print ('Player X choose a column:')
            col = input()
            col = int(col)
            self.addMove(col,'X')
            if self.winsFor('X') == True:
                print (self)
                print ("X wins")
                break
            if self.isFull() == True:
                print ("Tie")
                break
            print(self)
            print ("Player O choose a column:")
            col=int(input())
            self.addMove(col,'O')
            if self.winsFor('O') == True:
                print(self)
                print ("O wins")
                break
            if self.isFull() == True:
                print (self)   
                print ("Tie")
                break"""    

    def playGameWith(self,aiPlayer):
        while True:    
            print(self)
            print ('Player X choose a column')
            col = input()
            col = int(col)
            self.addMove(col,'X')
            if self.winsFor('X') == True:
                print (self)
                print ("X wins")
                break
            if self.isFull() == True:
                print ("Tie")
                break
            print(self)
            oMove = aiPlayer.nextMove(self) # get the move 
            print("O moves in column",oMove)
            self.addMove(oMove,'O')         # make the move
                        # (where self is the board object)
            if self.winsFor('O') == True:
                print(self)
                print ("O wins")
                break
            if self.isFull() == True:
                print(self)
                print ("Tie")
                break
            oMove = aiPlayer.nextMove(self)        
	
def runMyScreen():
    root = Tk()
    root.title("Connect 4")
    b = Board(7,6,root)
    aiPlayer = Player('O', 3)
    b.playGUI(aiPlayer)
    root.mainloop()
    
runMyScreen()
