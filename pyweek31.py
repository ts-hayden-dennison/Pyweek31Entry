
#system stuff
import multiprocessing
import os
import random



#pygame
import pygame



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
	def enter(self, result)
		return

class GameState(State):
	def __init__(self, *args, **kwargs):
		State.__init__(self, *args, **kwargs)
		return
	
	def update(self, dt, surface):
		return




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



class GameStack(StateStack):
	def __init__(self, *args, **kwargs):
		StateStack.__init__(self, *args, **kwargs)
		return
	
	#update newest game state with the time passed since last frame and 
	#pygame surface on which to draw
	def update(self, dt, surface):
		if len(self.states) > 0:
			self.states[-1].update(dt, surface)
			if self.states[-1].finished:
				self.pop()
		return



def main():
	pygame.init()
	screen = pygame.display.set_mode(