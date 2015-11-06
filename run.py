#  Ericson's PyTetris
#
#  run.py
#  
#  Copyright 2015 Ericson Willians (Rederick Deathwill) <EricsonWRP@ERICSONWRP-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
  
import os
import pyglet
import json
import random

LINE_SEGMENT_THICKNESS = 16
ORIGIN = 0
PIECE_TOKEN = '0'
GAME_FONT = "Times New Roman"

class Serializable:

	def __init__(self):
		self.file = None
		
	def serialize(self, path, mode):    
		try:
			self.file = open(path, mode)
		except:
			raise FileNotFoundError()
		if self.file:
			return self.file

class App(Serializable, pyglet.window.Window):

	def __init__(self):
		Serializable.__init__(self)
		if os.path.isfile("config.txt"):
			self.data = self.load("config.txt")
		else:
			self.data = {
					"SCREEN_WIDTH": 768,
					"SCREEN_HEIGHT": 768,
					"FULLSCREEN": False,
					"LOCKED_MOUSE": False}
		self.write("config.txt")
		pyglet.window.Window.__init__(self, self.data["SCREEN_WIDTH"], 
											self.data["SCREEN_HEIGHT"], 
											fullscreen=self.data["FULLSCREEN"])
		if self.data["LOCKED_MOUSE"]:
			self.set_exclusive_mouse()

	def write(self, path):
		self.serialize(path, "w").write(json.dumps(self.data))
		
	def load(self, path):
		json_data = open(path, "r")
		self.data = json.load(json_data)
		json_data.close()
		return self.data

if __name__ == '__main__':
	app = App()
	
	def draw_game_area():
		pyglet.graphics.draw(24, pyglet.gl.GL_TRIANGLES, 
			("v2f", (ORIGIN, ORIGIN, ORIGIN, app.height, LINE_SEGMENT_THICKNESS, ORIGIN,
					 ORIGIN, app.height, LINE_SEGMENT_THICKNESS, app.height, LINE_SEGMENT_THICKNESS, ORIGIN,
					 ORIGIN, ORIGIN, ORIGIN, LINE_SEGMENT_THICKNESS, app.width / 2, ORIGIN,
					 ORIGIN, LINE_SEGMENT_THICKNESS, app.width / 2, LINE_SEGMENT_THICKNESS, app.width / 2, ORIGIN,
					 app.width / 2 - LINE_SEGMENT_THICKNESS, app.height, app.width / 2, app.height, app.width / 2, ORIGIN,
					 app.width / 2 - LINE_SEGMENT_THICKNESS, app.height, app.width / 2, ORIGIN, app.width / 2 - LINE_SEGMENT_THICKNESS, ORIGIN,
					 ORIGIN, app.height, app.width / 2, app.height, app.width / 2, app.height - LINE_SEGMENT_THICKNESS,
					 ORIGIN, app.height, ORIGIN, app.height - LINE_SEGMENT_THICKNESS, app.width / 2, app.height - LINE_SEGMENT_THICKNESS
					 ))
		)

	def draw_texts():
		pyglet.text.Label(
			"Ericson's PyTetris - 2015",
			font_name = GAME_FONT,
			font_size=LINE_SEGMENT_THICKNESS,
			color = (255, 255, 255, 255),
			x = app.width - 184, y = app.height - LINE_SEGMENT_THICKNESS,
			anchor_x = "center", anchor_y = "center"
		).draw()
		
	def fetch_elemental_piece(_x, _y):
		return (pyglet.text.Label(
			PIECE_TOKEN*2,
			font_name=GAME_FONT,
			font_size=LINE_SEGMENT_THICKNESS,
			color=(255, 0, 0, 255),
			x=_x+LINE_SEGMENT_THICKNESS*2, y=_y+app.height-LINE_SEGMENT_THICKNESS*2-n,
			anchor_x = "center", anchor_y = "center"
		) for n in range(0, LINE_SEGMENT_THICKNESS*2, LINE_SEGMENT_THICKNESS))

	def fetch_master_piece(name, x, y):
		if name == 'I':
			return (fetch_elemental_piece(x+LINE_SEGMENT_THICKNESS*n/1.5, y) for n in range(0, 8, 2))

	@app.event
	def on_draw():
		app.clear()
		#[label.draw() for label in labels]
		draw_game_area()
		draw_texts()
		for master_piece in fetch_master_piece('I', 4, 0):
			for elemental_piece in master_piece:
				elemental_piece.draw()
	
	pyglet.app.run()
