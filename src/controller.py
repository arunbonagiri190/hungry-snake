from tkinter import *
import random
import gui_components
import pathFinder


class Controller():
    
    def __init__(self):
        self.window = None
        self.pathFinder = pathFinder.PathFinder(self.window)
        self.flag = False

        self.path = ['d','d','d','d','d','d','d','d','d','d',
                     's','s','s','s','s','s','s','s','s','s',
                     'a','a','a','a','a','a','a','a','a','a',
                     'w','w','w','w','w','w','w','w','w','w']
        
        self.path_index = 0
        

    def trail(self):

        if self.flag:
                self.window.update(self.path[self.path_index])
                
                if self.path_index+1 >= len(self.path):
                    self.clearPath()
                    self.flag = False
                else:
                    self.path_index +=1

                self.window.canvas.after(50, self.trail)
    
    def clearPath(self):
        self.path_index = 0
        self.path = []
    
    def on_key_press(self, e):
        
        if e.char == 'p':

            if self.flag == False: # means snake alredy moving using path
                self.clearPath()
                self.path = self.pathFinder.find()
                #print('path: ', self.path, 'len: ', len(self.path))

                if len(self.path)>0:
                    self.flag = True
                    self.trail()
                else:
                    print('safe path not exits')

        elif e.char == 'o':
            self.flag = False
            
        else:
            self.window.update(e.char)
    
    def set_window(self, window):
        self.window = window
        self.pathFinder.window = window