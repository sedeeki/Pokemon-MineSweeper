from functools import reduce
from itertools import product
from operator import add
from random import sample
from tkinter import *
from typing import Set, Tuple
from PIL import Image
from PIL import ImageTk
import random
import time

class StatusBar(Frame): # status bar class 
    def __init__(self,master,attempted,left,time):
        self.master = master
        self.attempted = attempted
        self.left = left
        self.time = time
        self.restart = None
        self.new = None
        self.canvas = Canvas(self.master,height = 80, width = 440,bg = "white")
        self.canvas.pack()
        self.drawBar()

        
    def drawBar(self):
        """ draws bar onto canvas """ 
        
        string = str(self.attempted) + " attempted catches"
        self.canvas.create_text(120,30,fill="black",font="Times 8",
                           text= string)
        string = str(self.left) + " pokeballs left"
        self.canvas.create_text(110,45,fill="black",font="Times 8",
                           text= string)
        self.canvas.create_text(280,30,fill="black",font="Times 8",
                           text= "Time elapsed")
        minutes = int(self.time/60)
        seconds = self.time - (minutes * 60)
        string = str(minutes) + "m " + str(seconds) + "s" 
        self.canvas.create_text(280,45,fill="black",font="Times 8",
                           text= string)
        self.new = Button(self.master,text = "New Game")
        self.restart = Button(self.master,text = "Restart Game")
        self.canvas.create_window(390,20,window = self.new)
        self.canvas.create_window(390,60,window = self.restart)
        self.pic = PhotoImage(file = 'full_pokeball.png')
        self.canvas.create_image(10,10,image = self.pic, anchor = NW)
        self.clock = PhotoImage(file = 'clock.png')
        self.canvas.create_image(190,10,image = self.clock, anchor = NW)
        self.canvas.update
        


class PokemonGameV2():
    
    def __init__(self,master,grid_size = 10, num_pokemon = 15):
        """ images that store all adjacent squares with no of pokemon surrounding in them"""
        self.images = [] 
        image = Image.open("zero_adjacent.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("one_adjacent.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("two_adjacent.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("three_adjacent.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("four_adjacent.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("five_adjacent.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("six_adjacent.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("seven_adjacent.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        image = Image.open("eight_adjacent.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.images.append(image2)
        
        """ stores pokeball image """
        image = Image.open("pokeball.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokeball = image2
        
        """ stores dark undiscovered image """ 
        image = Image.open("unrevealed.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.dark = image2
        
        """ array of pokemon images all 6 """
        image = Image.open("pikachu.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokemon = []
        self.pokemon.append(image2)
        image = Image.open("cyndaquil.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokemon.append(image2)
        image = Image.open("charizard.png")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokemon.append(image2)
        image = Image.open("togepi.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokemon.append(image2)
        image = Image.open("umbreon.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokemon.append(image2)
        image = Image.open("psyduck.gif")
        image = image.resize((44,40), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image)
        self.pokemon.append(image2)
        self.master = master
        self.size = grid_size
        self.pokemonSize = num_pokemon
        self.canvas = Canvas(master,height = 400, width = 440)
        self.canvas.pack()
        self.buttons = []
        self.show = []
        self.array = []
        self.location = []
        self.items = num_pokemon
        self.exit = False
        self.stopTime = False
        for i in range(grid_size): 
            """ initializing all the variables"""
            #self.buttons.append([])
            self.show.append([])
            self.array.append([])
            self.location.append([])
            for j in range(grid_size):
                #self.buttons[i].append(Button(master,image=self.dark))
                self.show[i].append(0)
                self.array[i].append(0)
                self.location[i].append(0)
        self.bar = StatusBar(self.master,0,num_pokemon,0)
        self.initialize()
        self.initUI()
    
    def countPokemon(self,x,y): 
        """ count no of pokemon surrounding one square tile """ 
        count = 0
        if (y > 0 and self.array[x][y-1] == -1):
            count = count + 1
        if (x > 0 and y > 0 and self.array[x-1][y-1] == -1):
            count = count + 1
        if (x > 0 and self.array[x-1][y] == -1):
            count = count + 1
        if (x > 0 and y < self.size - 1 and self.array[x-1][y+1] == -1):
            count = count + 1    
        if (y < self.size - 1 and self.array[x][y+1] == -1):
            count = count + 1
        if (x < self.size - 1 and y < self.size - 1 and self.array[x+1][y+1] == -1):
            count = count + 1
        if (x < self.size - 1 and self.array[x+1][y] == -1):
            count = count + 1
        if (x < self.size - 1 and y > 0 and self.array[x+1][y-1] == -1):
            count = count + 1       
        return count
     
    def buttonClicked(self,event,i,j): 
        """ left button click event """ 
        if (self.array[i][j] == -1): 
            print("You lose")
            self.showPokemon()
            self.stopTime = True
            #self.exitGame()
        else:
            self.show[i][j] = 1
            self.initUI()
            
    def showPokemon(self): 
        """ shows all pokemons when player loses game """ 
        self.buttons = []
        for i in range(self.size):
            self.buttons.append([])
            for j in range(self.size):
                if (self.array[i][j] == -2):
                    self.buttons[i].append(Button(self.master,image=self.pokeball))
                elif(self.array[i][j] == -1):
                    self.buttons[i].append(Button(self.master,image=self.pokemon[random.randint(0,5)]))
                else:
                    self.buttons[i].append(Button(self.master,image=self.images[self.array[i][j]]))
        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_window(22 + (44*j),20 + (40*i),window=self.buttons[i][j])    
        
    def buttonClicked1(self,event,i,j): 
        """ right click event to add pokeball """ 
        if(self.bar.left > 0): 
            if (self.array[i][j] != -2):
                self.show[i][j] = 1
                self.array[i][j] = -2
                self.bar.attempted = self.bar.attempted + 1
                self.bar.left = self.bar.left - 1
                self.initUI()
            else:
                self.bar.attempted = self.bar.attempted - 1
                self.bar.left = self.bar.left + 1
                if (self.location[i][j] == 1):
                    self.show[i][j] = 0
                    self.array[i][j] = -1
                else:
                    self.array[i][j] = self.countPokemon(i, j)
                    self.show[i][j] = 0
                self.initUI()
            
        
    def initUI(self): 
        """ GUI of the game is here """
        self.buttons = []
        for i in range(self.size):
            self.buttons.append([])
            for j in range(self.size):
                if (self.show[i][j] == 0):
                    self.buttons[i].append(Button(self.master,image=self.dark))
                else:
                    if (self.array[i][j] == -2):
                        self.buttons[i].append(Button(self.master,image=self.pokeball))
                    else:
                        self.buttons[i].append(Button(self.master,image=self.images[self.array[i][j]]))
        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_window(22 + (44*j),20 + (40*i),window=self.buttons[i][j])
                self.buttons[i][j].bind("<Button-1>",lambda event, x = i,
                                y = j: self.buttonClicked(event,x,y))    
                self.buttons[i][j].bind("<Button-3>",lambda event, x = i,
                                y = j: self.buttonClicked1(event,x,y))
        self.bar.restart.bind("<Button-1>",self.restart) 
        self.bar.drawBar()

    def exitGame(self): 
        """ exit game when won """ 
        self.exit = True

    def restart(self): 
        """ restart game """
        print("Restarting")
        for i in range(self.size):
            for j in range(self.size):
                self.show[i][j] = 0
                if (self.location[i][j] == 1):
                    self.array[i][j] = -1
                else:
                    self.array[i][j] = self.countPokemon(i, j)
        self.initUI()

    def initialize(self): 
        """ initialize the tiles with pokemon and normal tiles """ 
        count = 0
        while (count != self.pokemonSize):
            x = random.randint(0,self.size-1)
            y = random.randint(0,self.size-1)
            if (self.array[x][y] != -1):
                self.array[x][y] = -1
                self.location[x][y] = 1
                count = count + 1
        for i in range(self.size):
            for j in range(self.size):
                if (self.array[i][j] != -1):
                    self.array[i][j] = self.countPokemon(i, j)
                    
    def timer(self): 
        """ timer function for time elapsed """ 
        self.bar.time = self.bar.time + 1  
        self.bar.canvas.delete("all")
        self.bar.drawBar() 
     
    def win(self): 
        """ check if all places are discovered and issue win condition """ 
        for i in range(self.size):
            for j in range(self.size):
                if (self.show[i][j] == 0):
                    return False
        return True
        
    def startGame(self): 
        """ the main loop for the game """ 
        
        self.master.protocol("WM_DELETE_WINDOW", self.exitGame)
        start = time.time()
        seconds = 1
        while self.exit == False:
            self.master.update_idletasks()
            self.master.update()
            if (time.time() - start > seconds and self.stopTime == False):
                seconds = seconds + 1
                self.timer()
            if (self.win() == True):
                print("You won")
                self.exit = True
      


class Model(object):
    """Creates a board and adds mines to it."""

    def __init__(self, width: int, height: int, num_mines: int):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = self.create_grid()
        self.add_mines()

    def create_grid(self):
        """Create a self.width by self.height grid of elements with value 0."""

        return [[0] * self.width for _ in range(self.height)]

    def add_mines(self):
        """Randomly adds the amount of self.num_mines to grid."""

        for x, y in sample(list(product(range(self.width), range(self.height))), self.num_mines):
            self.grid[x][y] = 'm'


class View(Frame):
    """Creates a main window and grid of button cells."""

    def __init__(self, master: Tk, width: int, height: int, num_mines: int):
        Frame.__init__(self, master)
        self.master = master
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.master.title('Pokemon: Got 2 Find Them All!')
        self.grid()
        self.top_panel = TopPanel(self.master, self.height, self.width, self.num_mines)
        self.buttons = self.create_buttons()

    def create_buttons(self):
        """Create cell button widgets."""

        def create_button(x, y):
            button = Button(self.master, width=8,height = 4, bg='green')
            button.grid(row=x + 1, column=y + 1)
            return button

        return [[create_button(x, y) for y in range(self.height)] for x in range(self.width)]

    def display_lose(self):
        """Display the lose label when lose condition is reached."""

        self.top_panel.loss_label.grid(row=0, columnspan=7)

    def display_win(self):
        """Display the win label when win condition is reached."""

        self.top_panel.win_label.grid(row=0, columnspan=7)

    def hide_labels(self, condition=None):
        """Hides labels based on condition argument."""

        if condition:
            self.top_panel.mines_left.grid_remove()
        else:
            self.top_panel.loss_label.grid_remove()
            self.top_panel.win_label.grid_remove()


class TopPanel(Frame):
    """Create top panel which houses reset button and win/lose and mines left labels."""

    def __init__(self, master: Tk, width: int, height: int, num_mines: int):
        Frame.__init__(self, master)
        self.master = master
        self.num_mines = num_mines
        self.grid()

        self.reset_button = Button(self.master, width=7, text='Reset')
        self.reset_button.grid(row=0, columnspan=int((width * 7) / 2))

        self.loss_label = Label(text='You Lose!', bg='red')
        self.win_label = Label(text='You Win!', bg='green')

        self.mine_count = StringVar()
        self.mine_count.set('Mines remaining: ' + str(self.num_mines))
        self.mines_left = Label(textvariable=self.mine_count)
        self.mines_left.grid(row=0, columnspan=5)


def get_adjacent(index: Tuple[int, int]) -> Set[Tuple[int, int]]:
    x, y = index

    return {
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
    }


class Controller(object):
    """Sets up button bindings and minesweeper game logic.

    The act of revealing cells is delegated to the methods: adjacent_mine_count(), reveal_cell(), reveal_adjacent(), and reveal_cont(). End conditions are handled by the lose() and win() methods.
    """

    def __init__(self, width: int, height: int, num_mines: int,task):
        self.task = task
        self.width = width
        self.height = height
        self.num_mines = num_mines
        if (self.task == "TASK_ONE"):   
            self.model = Model(self.width, self.height, self.num_mines)
            self.root = Tk()
            self.view = View(self.root, self.width, self.height, self.num_mines)
            # self.color_dict is used to assign colors to cells
            self.color_dict = {
                0: 'light green', 1: 'light green', 2: 'light green',
                3: 'light green', 4: 'light green', 5: 'light green',
                6: 'grey', 7: 'grey', 8: 'grey'
            }
            
            # self.count keeps track of cells with value of 0 so that they get revealed with self.reveal_cont call only once.
            self.count = set()
            self.cells_revealed = set()
            self.cells_flagged = set()
            self.game_state = None
            self.initialize_bindings()
            self.root.mainloop()
        elif(self.task == "TASK_TWO"):
            self.root = Tk()
            self.game = PokemonGameV2(self.root)
            self.game.startGame()

    def initialize_bindings(self):
        """Set up reveal cell and flag cell key bindings."""

        for x in range(self.height):
            for y in range(self.width):
                def closure_helper(f, index):
                    def g(_): f(index)

                    return g

                # Right click bind to reveal decision method
                self.view.buttons[x][y].bind('<Button-1>', closure_helper(self.reveal, (x, y)))

                # Left click bind to flag method
                self.view.buttons[x][y].bind('<Button-3>', closure_helper(self.flag, (x, y)))

        # Set up reset button
        self.view.top_panel.reset_button.bind('<Button>', lambda event: self.reset())

    def reset(self):
        """Resets game. Currently, game setup gets slower with each reset call, and window height slightly increases."""

        self.view.hide_labels()
        self.count = set()
        self.cells_revealed = set()
        self.cells_flagged = set()
        self.game_state = None
        self.model = Model(self.width, self.height, self.num_mines)
        self.view = View(self.root, self.width, self.height, self.num_mines)
        self.initialize_bindings()

    def reveal(self, index: Tuple[int, int]):
        """Main decision method determining how to reveal cell."""

        x, y = index
        val = self.adjacent_mine_count(index)

        if val in range(1, 9):
            self.reveal_cell(index)
            self.count.add(index)

        if self.model.grid[x][y] == 'm' and self.game_state != 'win' and self.view.buttons[x][y]['text'] != 'FLAG':
            self.game_state = 'Loss'
            self.lose()

        # Begin the revealing recursive method when cell value is 0
        if val == 0:
            self.reveal_cont(index)

    def adjacent_mine_count(self, index: Tuple[int, int]) -> int:
        """Returns the number of adjacent mines."""

        def is_mine(pos):
            try:
                return self.model.grid[pos[0]][pos[1]] == 'm'
            except IndexError:
                return False

        return reduce(add, map(is_mine, get_adjacent(index)))

    def reveal_cell(self, index: Tuple[int, int]):
        """Reveals cell value and assigns an associated color for that value."""

        x, y = index

        cells_unrevealed = self.height * self.width - len(self.cells_revealed) - 1

        if self.view.buttons[x][y]['text'] == 'FLAG':
            pass
        elif self.model.grid[x][y] == 'm':
            self.view.buttons[x][y].configure(bg='yellow')
        else:
            # Checks if cell is in the board limits
            if 0 <= x <= self.height - 1 and 0 <= y <= self.width - 1 and index not in self.cells_revealed:
                value = self.adjacent_mine_count(index)

                self.view.buttons[x][y].configure(text=value, bg='spring green')

                self.count.add(index)
                self.cells_revealed.add(index)

            # Removes cell from flagged list when the cell gets revealed
            if index in self.cells_flagged:
                self.cells_flagged.remove(index)
                self.update_mines()

            # Check for win condition
            if cells_unrevealed == self.num_mines and not self.game_state:
                self.win()

    def reveal_adjacent(self, index: Tuple[int, int]):
        """Reveals the 8 adjacent cells to the input cell index."""

        for pos in get_adjacent(index) | {index}:
            if 0 <= pos[0] <= self.height - 1 and 0 <= pos[1] <= self.width - 1:
                self.reveal_cell(pos)

    def reveal_cont(self, index: Tuple[int, int]):
        """Recursive formula that reveals all adjacent cells only if the selected cell has no adjacent mines. (meaning self.adjacent_mine_count(index) == 0)."""

        val = self.adjacent_mine_count(index)

        if val == 0:
            self.reveal_adjacent(index)

            for pos in get_adjacent(index):
                if (
                        0 <= pos[0] <= self.height - 1
                        and 0 <= pos[1] <= self.width - 1
                        and self.adjacent_mine_count(pos) == 0
                        and pos not in self.count
                ):
                    self.count.add(pos)
                    self.reveal_cont(pos)

    def win(self):
        """Display win."""

        self.view.hide_labels('mine')
        self.view.display_win()
        self.game_state = 'win'

    def lose(self):
        """Display lose. Reveal all cells when a mine is clicked."""

        self.view.hide_labels('mine')

        for x in range(self.height):
            for y in range(self.width):
                self.reveal_cell((x, y))

        self.view.display_lose()

    def flag(self, index: Tuple[int, int]):
        """Allows player to flag cells for possible mines. Does not reveal cell."""

        x, y = index

        button_val = self.view.buttons[x][y]

        if button_val['bg'] == 'green':
            button_val.configure(bg='red', text='FLAG')
            self.cells_flagged.add(index)
        elif button_val['text'] == 'FLAG':
            button_val.configure(bg='green', text='')
            self.cells_flagged.remove(index)

        self.update_mines()

    def update_mines(self):
        """Update mine counter."""

        mines_left = self.num_mines - len(self.cells_flagged)

        if mines_left >= 0:
            self.view.top_panel.mine_count.set(f'Mines remaining: {mines_left}')


def main():
    
    return Controller(16,16,40,"TASK_TWO") 

if __name__ == '__main__':
    main()