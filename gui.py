# -*- coding: utf-8 -*-
import wx
import game

CELL = 12	# cell drawing size

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

class Control(wx.Panel):
	def __init__(self, parent, game, player):

		self.game = game
		self.player = player
		self.parent = parent
		super(Control, self).__init__(parent,size=(2*CELL,0))

		self.InitButtons()
		self.Bind(wx.EVT_PAINT,self.OnPaint)

	def InitButtons(self):
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.ids = {}
		for i in self.game.colors:
			btn = wx.Panel(self)
			self.ids[btn.GetId()] = i

			# put centered labels
			# WARNING: labels hard coded to hard coded key map
			label = wx.StaticText(btn,-1,label=str((i+1+5*self.player)%10))
			sizer = wx.GridSizer(1,1,1,1)
			sizer.Add(label,0,wx.ALIGN_CENTER)
			btn.SetSizer(sizer)

			vbox.Add(btn, 1, wx.EXPAND)
		self.SetSizer(vbox)

	def OnPaint(self,e):
		# TODO: implement hover effect, otherwise game looks frozen
		# too stupid to not overwrite hover color on dumb refresh
		for i in self.ids:
			btn = wx.FindWindowById(i)

			if self.ids[i] in self.game.colors_available(self.player):
				btn.SetBackgroundColour(self.game.area.colors[self.ids[i]])
				btn.Bind(wx.EVT_LEFT_UP,self.OnClick)
				btn.Bind(wx.EVT_ENTER_WINDOW,self.OnEnter)
				btn.Bind(wx.EVT_LEAVE_WINDOW,self.OnLeave)
			else:
				btn.SetBackgroundColour(None)


	def OnClick(self,e):
		if self.game.command(self.player,self.ids[e.GetId()]):
			for i in self.ids:
				btn = wx.FindWindowById(i)
				btn.Unbind(wx.EVT_LEFT_UP)
				btn.Unbind(wx.EVT_ENTER_WINDOW)
				btn.Unbind(wx.EVT_LEAVE_WINDOW)
			self.parent.Refresh()

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
		# vbox = wx.BoxSizer(wx.VERTICAL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		ctl1 = Control(panel,self.game,player=0)
		ctl2 = Control(panel,self.game,player=1)
		view = View(panel,self.game.area)
		# TODO: implement score counter/bar
		# ctr1 = wx.StaticText(panel,label=str(self.game.players[0].score))
		# ctr2 = wx.StaticText(panel,label=str(self.game.players[1].score))

		# arrange everything
		hbox.Add(ctl1, 1, wx.EXPAND)
		hbox.Add(view, width/(height/len(colors)), wx.EXPAND | wx.LEFT | wx.RIGHT, CELL)
		hbox.Add(ctl2, 1, wx.EXPAND)
		# vbox.Add(hbox,0,wx.EXPAND)
		# vbox.Add(ctr1,0,wx.EXPAND)
		# vbox.Add(ctr2,0,wx.EXPAND)

		panel.SetSizer(hbox)

		# fit window to content
		panel.Fit()
		self.Fit()

		self.Bind(wx.EVT_CHAR_HOOK,self.OnPress)

		self.SetTitle('Area')
		self.Centre()
		self.Show(True)

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
			a = Window()
			self.Close()
		else:
			pass

def main():
	app = wx.App()
	window = Window()
	app.MainLoop()


if __name__ == '__main__':
	main()