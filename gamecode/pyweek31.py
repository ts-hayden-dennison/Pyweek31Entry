
#system stuff
import multiprocessing as mp
import os
import random
from copy import deepcopy
from math import floor
import json




#pygame
import pygame
from pygame.locals import *

configpath = os.path.join(os.path.join(os.getcwd(), 'gamecode'), 'config.json')


#data from config file
with open(configpath, 'r') as f:
	config = json.load(f)

#dict for images
cache = {}


#state machine stuff
class State():
	def __init__(self, *args, **kwargs):
		self.finished = False
	
	#called when the state stack adds a state on top of this one
	#or we are removed
	def leave():
		return
	
	#called when the state stack removes us from the stack
	def exit():
		self.leave()
		return
	
	#update ourselves
	def update(self):
		return
	
	# when we are returned to from a state higher in the stack
	def enter(self, result):
		return

class GameState(State):
	def __init__(self, *args, **kwargs):
		State.__init__(self, *args, **kwargs)
		return
	
	def update(self, dt, surface):
		return

class TitleMenuState(GameState):
	pass


class StateStack():
	def __init__(self, *args, **kwargs):
		self.states = []
	
	#add state to stack
	def add(self, state):
		if len(self.states) > 0:
			self.states[-1].leave()
		self.states.append(state)
		return
	
	#remove highest state from the stack
	def pop(self):
		if len(self.states) > 1:
			result = self.states[-1].exit()
			self.states.pop()
			self.states[-1].enter(result)
		elif len(self.states) == 1:
			self.states[-1].exit()
			self.states.pop()
		return
	
	#update latest state in the stack
	def update(self):
		if len(self.states) > 0:
			self.states[-1].update()
			if self.states[-1].finished:
				self.pop()
		return
	
	def __len__(self):
		return len(self.states)



class GameStack(StateStack):
	def __init__(self, surface, *args, **kwargs):
		StateStack.__init__(self, *args, **kwargs)
		self.surface = surface
		return
	
	#update newest game state with the time passed since last frame and 
	#pygame surface on which to draw
	def update(self, dt, surface, events):
		if surface != self.surface:
			self.surface = surface
		if len(self.states) > 0:
			self.states[-1].update(dt, surface)
			if self.states[-1].finished:
				self.pop()
		return


def loader(requestQ, resultQ):
	print('hi')
	return

def main(requestQ, resultQ):
	pygame.init()
	width, height = config['width'], config['height']
	if not config['fullscreen']:
		screen = pygame.display.set_mode(
									 size=(width, height),
									 flags=(pygame.SHOWN | pygame.SCALED),
									 vsync=1,
									 display=0)
	else:
		screen = pygame.display.set_mode(
									 size=(width, height),
									 flags=(pygame.SHOWN | pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE),
									 vsync=1,
									 display=0)
	
	clock = pygame.time.Clock()
	
	
	stateShell = GameStack(screen)
	title = TitleMenuState(stateShell)
	stateShell.add(title)
	running = True
	dt = 0
	while (len(stateShell) > 0) and (running == True):
		
		#enforce fps
		clock.tick_busy_loop(config['FPS'])
		dt = clock.get_time()
		fps = int(clock.get_fps())
		
		# get events
		events = pygame.event.get()
		
		
		#process events
		for e in events:
			if e.type == pygame.QUIT:
				return
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					return
		
		stateShell.update(dt, screen, events)
		pygame.display.set_caption('{} | FPS: {}'.format(config['caption'], fps))
		
		pygame.display.flip()
	
	return

