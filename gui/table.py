import platform
import tkinter as tk
from .widgets import themedFrame, _on_mousewheel, themedListbox
import style

class Table(themedFrame):
	def __init__(self, *args, **kw):
		self.on_selection_event = None
		if "on_selection_event" in kw:
			self.on_selection_event = kw.pop("on_selection_event")
		themedFrame.__init__(self, *args, **kw)
		if not (kw.get("bg") or kw.get("background")):
			background = style.primary_color
			self.configure(bg = background)
		else:
			background = kw.get("bg") or kw.get("background")
		self.scrollbar = tk.Scrollbar(self, troughcolor = style.primary_color, bg = style.secondary_color)
		self.scrollbar.config(command=self.on_scroll_bar)
		self.scrollbar.place(relx = 1, relheight = 1, width = 20, x = - 20)
		
		self.listbox_frame = themedFrame(self)
		self.listbox_frame.place(relheight = 1, relwidth = 1, width = - 20)
		self.listboxes = {} #Dict to map listboxes by title

	def clear(self):
		for lb in self.listboxes:
			self.listboxes[lb].destroy()
		self.listboxes = {}

	def build(self, contents: dict):
		self.clear()
		for title in contents:
			self.listboxes[title] = themedListbox(self.listbox_frame, borderwidth = 0, highlightthickness = 0, exportselection=0)
			self.listboxes[title].bind("<<ListboxSelect>>", self.listbox_touch)
			self.listboxes[title].bind("<Double-Button>", self.on_selection)
			for item in contents[title]:
				self.listboxes[title].insert("end", item)

		ratio = 1 / len(self.listboxes)
		i = 0
		for lb in self.listboxes:
			tk.Label(self.listbox_frame, text = lb, background = style.primary_color, foreground = style.primary_text_color).place(relx = i * ratio, relwidth = ratio, height = 20)
			self.listboxes[lb].place(relx = i * ratio, relwidth = ratio, relheight = 1, y = 20, height = - 20)
			self.listboxes[lb].configure(state = "disable")
			i += 1
		for lb in self.listboxes:
			self.listboxes[lb].configure(state = "normal")
			self.listboxes[lb].config(yscrollcommand=self.scrollbar.set)
			break

		if platform.system() == 'Windows' or platform.system() == "Darwin":
			for lb in self.listboxes:
				self.listboxes[lb].bind("<MouseWheel>", self.on_mouse_wheel)
		elif platform.system() == "Linux":
			for lb in self.listboxes:
				self.listboxes[lb].bind("<Button-4>", self.on_mouse_wheel)
				self.listboxes[lb].bind("<Button-5>", self.on_mouse_wheel)

	def on_mouse_wheel(self, event):
		for lb in self.listboxes:
			break
		if platform.system() == 'Windows':
			self.listboxes[lb].yview("scroll", int(-1*(event.delta/120),"units"))
		elif platform.system() == "Linux":
			if event.num == 5:
				self.listboxes[lb].yview("scroll", 1,"units")
			if event.num == 4:
				self.listboxes[lb].yview("scroll", -1,"units")
		elif platform.system() == "Darwin":
			self.listboxes[lb].yview("scroll", event.delta,"units")

		for listbox in self.listboxes:
			self.listboxes[listbox].yview_moveto(self.listboxes[lb].yview()[0])

		return "break"

	def on_scroll_bar(self, move_type, move_units, __ = None):
		if move_type == "moveto":
			for lb in self.listboxes:
				self.listboxes[lb].yview_moveto(move_units)

	def listbox_touch(self, widget):
		pass

	def on_selection(self, event):
		root = self.winfo_toplevel()
		cursor_y = root.winfo_pointery()
		for lb in self.listboxes:
			cursor_y -= self.listboxes[lb].winfo_rooty()
			index = self.listboxes[lb].nearest(cursor_y)
			selection = self.listboxes[lb].get(index)
			break
		if self.on_selection_event:
			self.on_selection_event(selection)