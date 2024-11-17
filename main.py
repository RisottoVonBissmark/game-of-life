import time
import pygame

from pygame.locals import *

pygame.init()

class Cell():

    def __init__(self, pos: tuple|list, is_alive: bool, type = 0) -> None:
        
        self.pos = pos
        next_cells = 0
        self.is_alive = is_alive
        self.type = type

    def find_next_cells(self, map: list):

        self.next_cells = [0,0]
        for dir in [[1,0], [-1,0], [0,1], [0,-1], [1,1], [1,-1], [-1,1], [-1,-1]]:

            pos = [self.pos[0]+dir[0], self.pos[1]+dir[1]]
            
            if pos[0] < 0 or pos[0] > len(map)-1 or pos[1] < 0 or pos[1] > len(map[1])-1:
                continue
            
            cell = map[pos[1]][pos[0]]

            if cell.is_alive:
                self.next_cells[cell.type] += 1
    
    def update_state(self):

        if self.is_alive and self.next_cells[self.type] in [2,3]:
            self.is_alive = True
        elif not self.is_alive and self.next_cells[0] == 3:
            self.is_alive = True
            self.type = 0
        elif not self.is_alive and self.next_cells[1] == 3:
            self.is_alive = True
            self.type = 1
        else:
            self.is_alive = False

        if self.next_cells[0]+self.next_cells[1] > 3:
            self.is_alive = False

def grid(surface, pos: list, row: int, column: int, size: int) -> None:

    start_pos = pos[:]
    end_pos = [pos[0]+column*size, pos[1]]

    for i in range(column):
        
        start_pos[1] += size
        end_pos[1] += size
        pygame.draw.line(
            surface,
            "#000000",
            start_pos, 
            end_pos
        )

    start_pos = pos[:]
    end_pos = [pos[0], pos[1]+row*size]
    
    for j in range(row):

        start_pos[0] += size
        end_pos[0] += size
        pygame.draw.line(
            surface,
            "#000000",
            start_pos, 
            end_pos
        )

def main():
    
    scale = 16
    size = 70

    window = pygame.display.set_mode([scale*size, scale*size])

    map = [[Cell([j,i], False) for j in range(size)] for i in range(size)]

    cell_sprite = pygame.Surface([scale,scale])

    pause = True

    #game settings

    show_grid = True
    speed = 1  
    it = 0
    end = False
    while not end:

        for event in pygame.event.get():
            if event.type == QUIT:
                end = True
                

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    type = 1
                if event.button == 3:
                    type = 0

                pos = [event.pos[1] // scale, event.pos[0] // scale]
                cell = map[pos[0]][pos[1]]
                cell.is_alive = not cell.is_alive
                cell.type = type
                
                time.sleep(0.1)

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause = not pause
                    time.sleep(0.1)
                
                if event.key == K_g:
                    show_grid = not show_grid
                    time.sleep(0.1)
                
                if event.key == K_LEFT:
                    speed += 1
                    time.sleep(0.1)

                if event.key == K_RIGHT:
                    speed -= 1
                    if speed < 1:
                        speed = 1

                    time.sleep(0.1)

        for i in range(len(map)):
            for j in range(len(map[i])):
                cell = map[i][j]

                if not pause: 
                    cell.find_next_cells(map)

        window.fill('#FFFFFF')

        if show_grid:
            grid(window, [0,0], size, size, scale)

        for i in range(len(map)):
            for j in range(len(map[i])):
                cell = map[i][j]

                if not pause: 
                    cell.update_state()

                if cell.is_alive :
                    if cell.type == 1:
                        cell_sprite.fill('#AA0000')
                    if cell.type == 0:
                        cell_sprite.fill('#00AA00')

                    window.blit(cell_sprite, [cell.pos[0]*scale, cell.pos[1]*scale])

        
        pygame.display.update()
        
        if not pause:   
            print(it)
            it += 1
            time.sleep(1/speed)
    
    pygame.quit()

main()