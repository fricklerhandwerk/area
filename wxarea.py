# -*- coding: utf-8 -*-
import wx
import area

HEIGHT = 10
WIDTH = 20
CELL = 20	# cell drawing size

class Area(wx.Panel):

	def __init__(self, parent, **kw):
		self.area = kw.pop('area',None)

		super(Area, self).__init__(parent,size=(WIDTH*CELL,HEIGHT*CELL))

		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def OnPaint(self, e):

		dc = wx.PaintDC(self)

		x,y = self.GetSize()

		# draw cells
		for i in range(HEIGHT):
			for j in range(WIDTH):
				dc.SetBrush(wx.Brush(area.colors[self.area.area[i][j]]))
				dc.SetPen(wx.Pen("black",style=wx.TRANSPARENT))
				dc.DrawRectangle(j*x/WIDTH,i*y/HEIGHT,x/WIDTH,y/HEIGHT)

class Control(wx.Panel):

	def __init__(self, parent, **kw):

		super(Control, self).__init__(parent,size=(CELL,0))

		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnPaint(self, e):

		dc = wx.PaintDC(self)

		x,y = self.GetSize()
		print x,y
		# draw cells
		for i in range(len(area.colors)):
			dc.SetBrush(wx.Brush(area.colors[i]))
			dc.SetPen(wx.Pen("black",style=wx.TRANSPARENT))
			dc.DrawRectangle(0,i*y/len(area.colors),CELL,CELL)


class Frame(wx.Frame):

	def __init__(self, *args, **kw):

		self.area = kw.pop('area',None)

		super(Frame, self).__init__(*args, **kw)

		self.InitUI()

	def InitUI(self):

		panel = wx.Panel(self)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		ctl1 = Control(panel)
		ctl2 = Control(panel)
		area = Area(panel,area=self.area)

		hbox.Add(ctl1, 0, wx.EXPAND | wx.ALL, CELL)
		hbox.Add(area, 1, wx.EXPAND)
		hbox.Add(ctl2, 0, wx.EXPAND | wx.ALL, CELL)
		panel.SetSizer(hbox)

		panel.Fit()
		self.Fit()
		self.SetTitle('Focus event')
		self.Centre()
		self.Show(True)


def main():
	a = area.Board(WIDTH,HEIGHT)
	print a.area[0][2]
	print a
	ex = wx.App()
	Frame(None,area=a)
	ex.MainLoop()


if __name__ == '__main__':
	main()