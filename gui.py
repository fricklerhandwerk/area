# -*- coding: utf-8 -*-
from __future__ import division
import wx
import game
from wx.lib.pubsub import pub

CELL = 15	# cell drawing size

class View(wx.Panel):
	def __init__(self, parent, area):
		self.area = area

		super(View, self).__init__(parent,size=(self.area.width*CELL,self.area.height*CELL))
		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def OnPaint(self, e):
		dc = wx.PaintDC(self)
		x,y = self.GetSize()
		# draw cells
		for i in range(self.area.height):
			for j in range(self.area.width):
				dc.SetBrush(wx.Brush(self.area.colors[self.area[i,j]]))
				dc.SetPen(wx.Pen("black",style=wx.TRANSPARENT))
				dc.DrawRectangle(	j*x/self.area.width,\
				                 	i*y/self.area.height,\
				                 	x/self.area.width,\
				                 	y/self.area.height)

class Score(wx.Panel):
	def __init__(self, parent, player, colors):

		self.colors = colors
		self.player = player
		super(Score, self).__init__(parent)

		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnPaint(self, e):
		dc = wx.PaintDC(self)
		x,y = self.GetSize()
		# draw score bar
		s = self.player.score_relative
		dc.SetBrush(wx.Brush(self.colors[self.player.color]))
		dc.SetPen(wx.Pen("black",1))
		dc.DrawRectangle(0,0,min(s*x,x),y)

class Control(wx.Panel):
	def __init__(self, parent, game, player):

		self.game = game
		self.player = player
		super(Control, self).__init__(parent)

		self.InitButtons()
		self.NextTurn()

	def InitButtons(self):
		"""
		set up buttons with labels
		"""
		vbox = wx.BoxSizer(wx.VERTICAL)
		# remember button IDs and map them to colors
		self.ids = {}
		for i in self.game.colors:
			btn = wx.Panel(self)
			self.ids[btn.GetId()] = i

			# put centered labels
			# WARNING: labels hard coded to hard coded key map
			label = wx.StaticText(btn,0,label=str((i+1+5*self.player)%10))
			sizer = wx.GridSizer(1,1)
			sizer.Add(label,0,wx.ALIGN_CENTER)
			btn.SetSizer(sizer)

			vbox.Add(btn, 1, wx.EXPAND)
		self.SetSizer(vbox)

	def NextTurn(self):
		"""
		set buttons for a player's turn
		"""
		for i in self.ids:
			btn = wx.FindWindowById(i)
			if self.ids[i] in self.game.colors_available(self.player):
				# show label
				for c in btn.GetChildren():
					c.Show()
				btn.Bind(wx.EVT_LEFT_UP,self.OnClick)
				btn.Bind(wx.EVT_ENTER_WINDOW,self.OnEnter)
				btn.Bind(wx.EVT_LEAVE_WINDOW,self.OnLeave)
				btn.SetBackgroundColour(self.game.area.colors[self.ids[i]])
			else:
				# hide label
				for c in btn.GetChildren():
					c.Hide()
				btn.Unbind(wx.EVT_LEFT_UP)
				btn.Unbind(wx.EVT_ENTER_WINDOW)
				btn.Unbind(wx.EVT_LEAVE_WINDOW)
				btn.SetBackgroundColour(None)

	def OnClick(self,e):
		# change player's color to chosen value
		self.game.command(self.player,self.ids[e.GetId()])

	def OnEnter(self,e):
		# darken color
		o = e.GetEventObject()
		r,g,b = o.GetBackgroundColour().Get()
		o.SetBackgroundColour((r,g,b,200))
		o.Refresh()

	def OnLeave(self,e):
		# set color back
		o = e.GetEventObject()
		o.SetBackgroundColour(self.game.area.colors[self.ids[o.GetId()]])
		o.Refresh()

class Window(wx.Frame):
	def __init__(self):
		super(Window, self).__init__(None)

		# display settings
		width = 42
		height = 30
		colors = ["red","green","blue","yellow","magenta"]

		# size constraints for nice square buttons
		assert height/len(colors) * len(colors) == height
		assert width/(height/len(colors)) * height/len(colors) == width

		self.game = game.Game(height,width,colors)

		panel = wx.Panel(self)

		# controls and game board
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.ctl1 = Control(panel,self.game,player=0)
		self.ctl2 = Control(panel,self.game,player=1)
		self.score1 = Score(panel,self.game.players[0],colors)
		self.score2 = Score(panel,self.game.players[1],colors)
		self.view = View(panel,self.game.area)

		# arrange everything
		hbox.Add(self.ctl1,  	1, wx.EXPAND)
		hbox.Add(self.view,  	width/(height/len(colors)), wx.EXPAND)
		hbox.Add(self.ctl2,  	1, wx.EXPAND)
		vbox.Add(hbox,       	height, wx.EXPAND)
		vbox.Add(self.score1,	1, wx.EXPAND)
		# collapse border separating score bars
		vbox.Add(self.score2,	1, wx.EXPAND | wx.TOP,-1)

		panel.SetSizer(vbox)

		# fit window to content
		panel.Fit()
		self.Fit()

		self.Bind(wx.EVT_CHAR_HOOK,self.OnPress)
		pub.subscribe(self.NextTurn,"next turn")
		pub.subscribe(self.Winner,"winner")

		self.SetTitle('Area')
		self.Centre()
		self.Show()

	def NextTurn(self):
		self.ctl1.NextTurn()
		self.ctl2.NextTurn()
		self.Refresh()

	def Winner(self,winner):
		self.game.turn = 2
		self.NextTurn()

	def OnPress(self,e):
		# TODO: make this less hard coded
		k = e.GetUniChar()
		if chr(k) in ['1','2','3','4','5']:
			k = int(chr(k))-1
			if self.game.command(0,k):
				self.Refresh()
		elif chr(k) in ['6','7','8','9','0']:
			k = int(chr(k))
			if k != 0:
				k -= 6
			else:
				k = 4

			if self.game.command(1,k):
				self.Refresh()
		elif k == wx.WXK_ESCAPE:
			# quite game
			self.Close()
		elif k == wx.WXK_DELETE:
			# reset game
			pub.unsubAll()
			self.Close()
			Window()
		else:
			pass

def main():
	app = wx.App()
	Window()
	app.MainLoop()


if __name__ == '__main__':
	main()