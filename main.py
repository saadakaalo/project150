from tkinter import *
from gol import *

width = 720
height = 720
grid_size = 30
grid_size = grid_size
n_grids_horizontal = (width-2*grid_size)//grid_size
n_grids_vertical = (height-2*grid_size)//grid_size

# print(n_grids_vertical,n_grids_horizontal)

root = Tk()
root.title("Conway's Game of Life")
frame = Frame(root, width=width, height=height)
frame.pack()
canvas = Canvas(frame, width=width, height=height)
canvas.pack()

def create_grid():
    """This function creates the board on which the game will take place"""
    x = grid_size
    y = grid_size
    global grids # Variable to store the Cell objects
    global rectangles # Variable to store rectangles
    rectangles = []
    grids = []
    for i in range(n_grids_vertical):
        grids.append([])
        rectangles.append([])
        for j in range(n_grids_horizontal):
            rect = canvas.create_rectangle(x, y, x+grid_size, y+grid_size, fill="white")
            rectangles[i].append(rect)
            grids[i].append(Cell(x, y, i, j))
            x += grid_size
        x = grid_size
        y += grid_size



def change_colour_on_click(event):
    iy = int(event.x // grid_size) - 1
    ix = int(event.y // grid_size) - 1

    if ix < 0 or iy < 0 or ix >= n_grids_horizontal or iy >= n_grids_vertical:
        # print("out of bound")
        return

    if grids[ix][iy].isAlive:
        canvas.itemconfig(rectangles[ix][iy], fill="white")
    else:
        canvas.itemconfig(rectangles[ix][iy], fill="green")

    grids[ix][iy].switchStatus()



"""*******my**********"""
def n_alive_neighbors(cell):
    num_alive = 0
    x, y = cell.pos_matrix
    for i in (x-1, x, x+1):
        for j in (y-1, y, y+1):
            if i == x and j == y:
                continue
            if i == -1 or j == -1:
                continue
            try:
                if grids[i][j].isAlive:
                    num_alive += 1
            except IndexError:
                pass
    return num_alive

def change_status_of_the_grids():
    for row in grids:
        for grid in row:
            n_neighbours = n_alive_neighbors(grid)

            if grid.isAlive:
                if n_neighbours<2 or n_neighbours>3:
                    grid.nextStatus = False
                else:
                    grid.nextStatus = True
            else:
                if n_neighbours == 3:
                    grid.nextStatus = True
                else:
                    grid.nextStatus = False

def color_the_grids():
    for row in grids:
        for grid in row:
            x, y = grid.pos_matrix
            if grid.nextStatus:
                canvas.itemconfig(rectangles[x][y], fill="green")
            else:
                canvas.itemconfig(rectangles[x][y], fill="white")

            grid.isAlive = grid.nextStatus

def start_the_geme():
    change_status_of_the_grids()
    color_the_grids()
    global begin_id
    begin_id = root.after(1000, start_the_geme)

def clear_the_game():
    for row in grids:
        for grid in row:
            grid.isAlive = False
            grid.nextStatus = False
            x, y = grid.pos_matrix
            canvas.itemconfig(rectangles[x][y], fill="white")

def stop_the_game():
    root.after_cancel(begin_id)





create_grid()
start = Button(root, text="Start!", command=start_the_geme)
start.pack(side = LEFT)
stop = Button(root, text="Stop!", command = stop_the_game)
stop.pack(side = RIGHT)
clear = Button(root, text="Clear!", command = clear_the_game)
clear.pack(side = RIGHT)
canvas.bind("<Button-1>", change_colour_on_click)
root.mainloop()
