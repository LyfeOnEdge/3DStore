import json
import tkinter as tk
import style
from .widgets import themedFrame, themedLabel, Button, ScrolledThemedText, LabeledPathEntry, CreateToolTip, labeledThemedEntry

from settings_tool import settings

advanced_settings = ["boot9_path", "movable_path", "repo_url"]

class ScrollableFrame(themedFrame):
	def __init__(self, master, **kwargs):
		themedFrame.__init__(self, master, **kwargs)

		# create a canvas object and a vertical scrollbar for scrolling it
		self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, troughcolor = style.primary_color, bg = style.secondary_color)
		self.vscrollbar.pack(side='right', fill="y",  expand="false")
		self.canvas = tk.Canvas(self,
								bg=style.primary_color, bd=0,
								height=350,
								highlightthickness=0,
								yscrollcommand=self.vscrollbar.set)
		self.canvas.pack(side="left", fill="both", expand="true")
		self.vscrollbar.config(command=self.canvas.yview)

		# reset the view
		self.canvas.xview_moveto(0)
		self.canvas.yview_moveto(0)

		# create a frame inside the canvas which will be scrolled with it
		self.interior = themedFrame(self.canvas, **kwargs)
		self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

		self.bind('<Configure>', self.set_scrollregion)


	def set_scrollregion(self, event=None):
		""" Set the scroll region on the canvas"""
		self.canvas.configure(scrollregion=self.canvas.bbox('all'))


class SettingsPage(themedFrame):
	def __init__(self, app: tk.Tk, container: tk.Frame):
		themedFrame.__init__(self, container)
		self.app = app
		self.name = "SETTINGS"
		self.checkbutton_map = {}

		advanced_settings_frame = themedFrame(self)
		advanced_settings_frame.place(relwidth = 0.5, relheight = 1, height = - (20 + style.STANDARD_OFFSET))

		self.sed_box = LabeledPathEntry(advanced_settings_frame, "Path to movable.sed file -", filetypes = [('sed file', '*.sed')])
		self.sed_box.place(relwidth = 1, height = 20)
		CreateToolTip(self.sed_box.xtainer, "Select movable.sed file, this can be dumped from a 3ds")
		self.sed_box.set(settings.get_setting("movable_path"))

		self.boot9_box = LabeledPathEntry(advanced_settings_frame, "Path to boot9 file -", filetypes = [('boot9 file', '*.bin')])
		self.boot9_box.place(relwidth = 1, height = 20, y = 30)
		CreateToolTip(self.boot9_box.xtainer, "Select the path to boot9.bin, this can be dumped from a 3ds")
		self.boot9_box.set(settings.get_setting("boot9_path"))

		self.repo_box = labeledThemedEntry(advanced_settings_frame, "Repo URL to use -")
		self.repo_box.place(relwidth = 1, height = 20, y = 60)
		self.repo_box.set(settings.get_setting("repo_url"))


		checkbox_pane = ScrollableFrame(self)
		checkbox_pane.place(relx = 0.5, relwidth = 0.5, relheight = 1, height = - (20 + style.STANDARD_OFFSET))

		save_button = Button(self, text = "SAVE", callback = self.save)
		save_button.place(rely = 1, y = - 20, relwidth = 1, x = style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET)

		i = 0
		settings_dict = settings.get_settings()
		for s in settings_dict:
			if s in advanced_settings:
				continue
			var = tk.IntVar()
			var.set(settings_dict[s])
			b = tk.Checkbutton(checkbox_pane.interior, 
				text=s, 
				variable = var, 
				onvalue = True, 
				offvalue = False,
				background = style.primary_color,
				foreground = style.secondary_text_color,
				borderwidth = 0,
				highlightthickness = 0,
				)
			b.var = var
			b.grid(row=i, column=0, sticky = "w")
			self.checkbutton_map[s] = b
			i += 1

	def save(self):
		s = {}
		for b in self.checkbutton_map:
			s[b] = self.checkbutton_map[b].var.get()

		s["boot9_path"] = self.boot9_box.get()
		s["movable_path"] = self.sed_box.get()
		s["repo_url"] = self.repo_box.get()

		settings.save_settings(s)