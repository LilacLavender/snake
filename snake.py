from tkinter import *
import random
import pygame
from pygame.locals import *
from sys import exit


inputs = []
root = Tk()
root.title("Set Configurations")
height_label = Label(root, font=("Courier New", 10), text="Window Height:".rjust(20))
height_entry = Entry(root)
width_label = Label(root, font=("Courier New", 10), text="Window Width:".rjust(20))
width_entry = Entry(root)
gridsize_label = Label(root, font=("Courier New", 10), text="Grid Size:".rjust(20))
gridsize_entry = Entry(root)
speed_label = Label(
    root, font=("Courier New", 10), text="Speed(milliseconds):".rjust(20)
)
speed_entry = Entry(root)


def submit():
    global inputs
    entries = [height_entry, width_entry, gridsize_entry, speed_entry]
    inps = [
        height_entry.get(),
        width_entry.get(),
        gridsize_entry.get(),
        speed_entry.get(),
    ]
    for inp in inps:
        if not inp.isdigit():
            for entry in entries:
                entry.delete(0, "end")
            return
        else:
            inps[inps.index(inp)] = int(inp)
    if not (inps[0] % inps[2] == 0 and inps[1] % inps[2] == 0):
        for entry in entries:
            entry.delete(0, "end")
        return
    inputs = inps
    return


def default():
    global inputs
    inputs = [500, 500, 20, 10]


submit_button = Button(
    root, command=submit, text="Submit".center(38), font=("Courier New", 10)
)
default_button = Button(
    root,
    command=default,
    text="Use Default Values".center(38),
    font=("Courier New", 10),
)

height_label.grid(column=0, row=0)
height_entry.grid(column=1, row=0)
width_label.grid(column=0, row=1)
width_entry.grid(column=1, row=1)
gridsize_label.grid(column=0, row=2)
gridsize_entry.grid(column=1, row=2)
speed_label.grid(column=0, row=3)
speed_entry.grid(column=1, row=3)
submit_button.grid(column=0, columnspan=2, row=4)
default_button.grid(column=0, columnspan=2, row=5)


def check():
    global inputs
    if len(inputs) != 0:
        root.destroy()
    else:
        root.after(500, check)


check()
root.protocol("WM_DELETE_WINDOW", exit)
root.mainloop()


configs = inputs


pygame.init()

DISPLAYWIDTH, DISPLAYHEIGHT, GRIDSIZE, SPEED = configs

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTGREEN = (144, 238, 144)

windowSurface = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT), 0, 32)
clock = pygame.time.Clock()
score = 0
snake = {
    "rect": pygame.Rect(
        (DISPLAYWIDTH / 2) - ((DISPLAYWIDTH / 2) % GRIDSIZE),
        (DISPLAYHEIGHT / 2) - ((DISPLAYHEIGHT / 2) % GRIDSIZE),
        GRIDSIZE,
        GRIDSIZE,
    ),
    "color": WHITE,
}
apple = {
    "rect": pygame.Rect(
        random.randint(0, (DISPLAYWIDTH - GRIDSIZE) / GRIDSIZE) * GRIDSIZE,
        random.randint(0, (DISPLAYHEIGHT - GRIDSIZE) / GRIDSIZE) * GRIDSIZE,
        GRIDSIZE,
        GRIDSIZE,
    ),
    "color": RED,
}


def update(scoreLOCAL):
    if (
        snake["rect"].top == apple["rect"].top
        and snake["rect"].left == apple["rect"].left
    ):
        scoreLOCAL += 1
        apple["rect"] = pygame.Rect(
            random.randint(0, (DISPLAYWIDTH - GRIDSIZE) / GRIDSIZE) * GRIDSIZE,
            random.randint(0, (DISPLAYHEIGHT - GRIDSIZE) / GRIDSIZE) * GRIDSIZE,
            GRIDSIZE,
            GRIDSIZE,
        )
        pygame.display.set_caption(str(scoreLOCAL))
        print(apple["rect"])
    if dir == "up":
        snake["rect"].top -= GRIDSIZE
    if dir == "left":
        snake["rect"].left -= GRIDSIZE
    if dir == "down":
        snake["rect"].top += GRIDSIZE
    if dir == "right":
        snake["rect"].left += GRIDSIZE
    pygame.draw.rect(windowSurface, snake["color"], snake["rect"])
    pygame.draw.rect(windowSurface, apple["color"], apple["rect"])
    pygame.display.update()
    clock.tick(SPEED)
    return scoreLOCAL


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                dir = "left"
            if event.key == K_RIGHT or event.key == K_d:
                dir = "right"
            if event.key == K_DOWN or event.key == K_s:
                dir = "down"
            if event.key == K_UP or event.key == K_w:
                dir = "up"
    windowSurface.fill(GREEN)
    if not (
        snake["rect"].left > DISPLAYWIDTH
        or snake["rect"].left < 0
        or snake["rect"].top > DISPLAYHEIGHT
        or snake["rect"].top < 0
    ):
        score = update(score)
    else:
        pygame.display.set_caption("GAME OVER")
