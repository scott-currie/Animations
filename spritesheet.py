import pygame
from imageloader import ImageLoader as IL 

class SpriteSheet(object):
	def __init__(self, fileName, columns, rows):
		self.rows = rows
		self.cols = columns
		self.sheet = IL.load('resources/graphics', fileName, scale=3.0)
		self.cellWidth = self.sheet.get_rect().width / self.cols
		self.cellHeight = self.sheet.get_rect().height / self.rows

	def get_cell(self, col, row):
		return self.sheet.subsurface((col * self.cellWidth,
						row * self.cellHeight,
						self.cellWidth,
						self.cellHeight))

	def get_cells(self, startCell, endCell):
		""" Return a list of images from left to right and top to bottom.
 		startCell and endCell are tuples representing the column and row pairs
		of the first and last cells in the sequence.
		"""
		frames = []
		for row in range(startCell[1], endCell[1] + 1):
			for col in range(startCell[0], endCell[0] + 1):
				frames.append(self.get_cell(col, row))
		return frames


