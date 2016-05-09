# -*- coding: utf-8 -*-
import wx
import wx.lib.platebtn as plt
import area

HEIGHT = 10
WIDTH = 20
CELL = 20	# cell drawing size

class Board(wx.Panel):

	def __init__(self, parent, **kw):
		# catch game board before initializing widget
		self.area = kw.pop('area',None)

		super(Board, self).__init__(parent,size=(WIDTH*CELL,HEIGHT*CELL))

		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnPaint(self, e):
		dc = wx.PaintDC(self)
		x,y = self.GetSize()

		# draw cells
		for i in range(HEIGHT):
			for j in range(WIDTH):
				dc.SetBrush(wx.Brush(area.colors[self.area[i,j]]))
				dc.SetPen(wx.Pen("black",style=wx.TRANSPARENT))
				dc.DrawRectangle(j*x/WIDTH,i*y/HEIGHT,x/WIDTH,y/HEIGHT)

class Control(wx.Panel):

	def __init__(self, parent, **kw):

		super(Control, self).__init__(parent,size=(HEIGHT*CELL/len(area.colors),0))

		self.parent = parent
		vbox = wx.BoxSizer(wx.VERTICAL)

		self.ids = {}
		for i in area.colors:
			btn = wx.Panel(self)
			btn.SetBackgroundColour(i)
			btn.Bind(wx.EVT_LEFT_UP,self.OnClick)
			btn.Bind(wx.EVT_ENTER_WINDOW,self.OnEnter)
			btn.Bind(wx.EVT_LEAVE_WINDOW,self.OnLeave)

			self.ids[btn.GetId()] = i
			vbox.Add(btn, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.Bind(wx.EVT_LEFT_UP,self.OnClick)

	def OnClick(self,e):
		print e.GetId()
		print self.parent
		# e.GetEventObject().parent.area.set_color(0,0,area.colors.index[self.ids[e.GetId()]])
		# print parent.area
		# print "press", self.ids[e.GetId()],e.GetId()
		e.Skip()

	def OnEnter(self,e):
		o = e.GetEventObject()
		r,g,b = o.GetBackgroundColour().Get()
		o.SetBackgroundColour((r,g,b,200))
		o.Refresh()

	def OnLeave(self,e):
		o = e.GetEventObject()
		o.SetBackgroundColour(self.ids[o.GetId()])
		o.Refresh()

class Frame(wx.Frame):

	def __init__(self, *args, **kw):

		# catch game board before initializing widget
		self.area = kw.pop('area',None)

		super(Frame, self).__init__(*args, **kw)

		self.InitUI()

	def InitUI(self):

		# main panel
		panel = wx.Panel(self)

		# controls and game board
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		ctl1 = Control(panel)
		ctl2 = Control(panel)
		area = Board(panel,area=self.area)

		# arrange everything
		hbox.Add(ctl1, 0, wx.EXPAND)
		hbox.Add(area, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, CELL)
		hbox.Add(ctl2, 0, wx.EXPAND)
		panel.SetSizer(hbox)

		# fit window to content
		panel.Fit()
		self.Fit()

		self.SetTitle('Area')
		self.Centre()
		self.Show(True)

def main():
	a = area.Board(WIDTH,HEIGHT)
	print a
	app = wx.App()
	Frame(None,area=a)
	app.MainLoop()


if __name__ == '__main__':
	main()