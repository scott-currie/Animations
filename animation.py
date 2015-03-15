import cfg
from imageloader import ImageLoader as IL 
import os

class Animation(object):
	''' Class consists of a list: self.frames that is a list of all the
	frames in each individual animation. Each game update, the next_frame()
	method increments currFrame by 1 and returns the next image in self.frames.
	If character animation changes, play method is called on the appropriate
	animation, currFrames is set to -1, and next_frame() cues up the first
	frame. This method results in lists of frames with potentially many
	duplicated frames, but benefits from the simplicity of having each animation
	keep track of its own position as it runs instead of timing it externally.
	next_frame() also sets finished = True when it runs out from frames, so
	game loop should be aware when an animation is ending so it can replay
	or choose another animation.
	'''
	
	def __init__(self, spriteSheet, startCell, endCell, duration=1.0):
		#Need to provide a spritesheet and the starting and ending cells 
		#to build the sequence of frames. Duration is essentially the
		#number of seconds the animation should take. A 1.0 second ani at
		#30fps means that all the frames in an animation should be spread
		#out over 30 frames.

		#self.frames is the list of frames making up an individual
		#animation. The number of times each unique frame in sequence
		#is repeated should represent the proportion of time each frame
		#should be displayed. The frame list is either expanded by
		#duplicating frames or compressed by removing frames.

		self.frames = spriteSheet.get_cells(startCell, endCell)
		
		#expansion is frame factor, or number of times to duplicate
		#each frame in the expanded frames list
		expansion = (duration * cfg.FPS) / len(self.frames)
		expandedFrames = []
		for frame in self.frames:
			for i in range(0, int(expansion)):
				expandedFrames.append(frame)
		self.frames = expandedFrames
		self.currFrame = -1
		self.finished = False

	def play(self):
		#Start currFrame at -1. That way, we can use the next_frame method to 
		#advance to frames[0] without having to handle whether or not we're starting 
		#a new animation, since we always advance frame each cycle and
		#don't want to skip frames[0].
		self.currFrame = -1
		self.finished = False

	def next_frame(self):		
		self.currFrame += 1
		if self.currFrame >= len(self.frames) - 1:
			self.finished = True
		return self.frames[self.currFrame]
