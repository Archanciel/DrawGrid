# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg

from tkinter import *
from tkinter import messagebox

from configurationmanager import ConfigurationManager
from gridview import GridView
import os


EVENT_BUTTON_ONE = 1
WHITE = (255, 255, 255)

class GridViewController:
    def __init__(self):
        '''
        Initializes game window, etc.
        '''
        self.configMgr = ConfigurationManager('gridView.ini')

        # setting Pygame window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = self.configMgr.windowLocation

        pg.init()
        self.screen = pg.display.set_mode((self.configMgr.gridWidth, self.configMgr.gridHeight))
        pg.display.set_caption(self.configMgr.windowTitle)
        self.clock = pg.time.Clock()
        self.running = True

        self.gridView = GridView(surface=self.screen, configManager=self.configMgr)
        self.buttonDownPressed = False
        self.dragging = False
        self.mouse_x_beg = 0
        self.mouse_y_beg = 0
        self.mouse_x_end = 0
        self.mouse_y_end = 0

    def new(self):
        '''
        Starts a new game.
        '''
        pass

    def run(self):
        '''
        Is the game loop.
        '''
        self.playing = True
        fps = self.configMgr.fps

        while self.playing:
            self.clock.tick(fps)
            self.handleEvents()
            self.update()
            self.draw()

    def handleEvents(self):
        '''
        Acquires and handles events.
        '''
        moveIncrementPx = self.configMgr.gridMoveIncrement

        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
                    Tk().wm_withdraw()  # to hide the main window
                    if messagebox.askquestion(None,'Do you want to save grid data ?') == 'yes':
                        self.gridView.saveGridData()

            # handling mouse grid move
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == EVENT_BUTTON_ONE:
                    self.buttonDownPressed = True
                    self.mouse_x_beg, self.mouse_y_beg = event.pos
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == EVENT_BUTTON_ONE:
                    self.buttonDownPressed = False
                    if self.dragging:
                        self.dragging = False
                    else:
                        if (self.mouse_x_beg, self.mouse_y_beg) == event.pos:
                            # here, we just clicked on a cell to activate or deactivate it
                            self.gridView.toggleCell(event.pos)
            elif event.type == pg.MOUSEMOTION:
                if self.buttonDownPressed:
                    self.dragging = True
                    self.mouse_x_end, self.mouse_y_end = event.pos
                    xOffset = self.mouse_x_beg - self.mouse_x_end
                    yOffset = self.mouse_y_beg - self.mouse_y_end

                    self.gridView.move(xOffset, yOffset)

                    self.mouse_x_beg = self.mouse_x_end
                    self.mouse_y_beg = self.mouse_y_end

            # technique used to allow moving grid only 1 unit at a time
            # elif event.type == pg.KEYDOWN:
            #     if event.key == pg.K_RIGHT:
            #         self.grid.moveRight(1)
            #     elif event.key == pg.K_LEFT:
            #         self.grid.moveLeft(1)

        # technique used to enable move grid more than 1 unit at a time
        keys = pg.key.get_pressed()

        if pg.key.get_mods() & pg.KMOD_SHIFT: #SHIFT key pressed
            if keys[pg.K_UP]:
                self.gridView.zoomIn()
            elif keys[pg.K_DOWN]: # using elif: since either zoom in or out, not both together, makes sense
                self.gridView.zoomOut()
        elif pg.key.get_mods() & pg.KMOD_CTRL:  # CTRL key pressed
            if keys[pg.K_UP]:
                self.gridView.moveViewToTop()
            if keys[pg.K_DOWN]:
                self.gridView.moveViewToBottom()
            if keys[pg.K_LEFT]:
                self.gridView.moveViewToLeftHome()
            if keys[pg.K_RIGHT]:
                self.gridView.moveViewToRightEnd()
        else:
            if keys[pg.K_DOWN]:
                self.gridView.moveViewDown(moveIncrementPx)
            if keys[pg.K_UP]:
                self.gridView.moveViewUp(moveIncrementPx)
            if keys[pg.K_RIGHT]:
                self.gridView.moveViewRight(moveIncrementPx)
            if keys[pg.K_LEFT]:
                self.gridView.moveViewLeft(moveIncrementPx)

    def update(self):
        '''
        Updates all game objects.
        '''
        pass

    def draw(self):
        '''
        Redraws all game objects. Thw actual drawing is delegated to the GridView class.
        '''
        if self.gridView.changed:
            # optimization: the grid is only drawned if something changed on it
            self.screen.fill(WHITE)
            self.gridView.draw()

            # *after* drawing everything, flip the display
            pg.display.flip()

    def show_start_screen(self):
        '''
        Shows game splash/start screen.
        '''
        Tk().wm_withdraw()  # to hide the main window
        if messagebox.askquestion(None, 'Do you want to load existing grid data ?') == 'yes':
            # here, we ask the GridView to load the grid data from the file specified in the gridview.ini
            # configuration file (loadatstartpathfilename setting). In case the grid data file is not found,
            # an error msg box informs the user.
            fileNotFoundName = self.gridView.loadGridData()
            if fileNotFoundName:
                messagebox.showerror(None, fileNotFoundName + ' not found. Grid initialized with neutral data !')
                self.gridView.initialiseCellsToValue(0)
        else:
            self.gridView.initialiseCellsToValue(0)

    def show_go_screen(self):
        '''
        Shows game over screen.
        '''
        pass

g = GridViewController()
g.show_start_screen()

while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()