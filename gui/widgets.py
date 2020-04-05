import platform
import tkinter as tk
import style
import tkinter.filedialog as tkfiledialog


def theme(widget, kw):
	if not (kw.get("background") or kw.get("bg")):
		widget.configure(bg = style.primary_color)
	if not kw.get("borderwidth"):
		widget.configure(borderwidth = 0)
	if not kw.get("highlightthickness"):
		widget.configure(highlightthickness = 0)

class themedFrame(tk.Frame):
	def __init__(self, frame, **kw):
		tk.Frame.__init__(self, frame, **kw)
		theme(self, kw)
		
class themedListbox(tk.Listbox):
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		tk.Listbox.configure(self, bg = style.primary_color)
		tk.Listbox.configure(self, fg = style.primary_text_color)
		theme(self, kw)
		if not kw.get("borderwidth"):
			self.configure(borderwidth = 2)

class themedText(tk.Text):
	def __init__(self, *args, **kw):
		tk.Text.__init__(self, *args, **kw)
		theme(self, kw)

	def clear(self):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.configure(state="disabled")

	def set(self, string):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.insert("1.0", string)
		self.configure(state="disabled")

	def set_entry(self, string):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.insert("1.0", string)

	def get(self):
		return self.get("1.0","end")

class themedLabel(tk.Label):
	def __init__(self, master, **kw):
		tk.Label.__init__(self, master, **kw)
		theme(self, kw) 
		if not kw.get("fg") or kw.get("foreground"):
			self.configure(fg = style.ENTRY_FOREGROUND)

	def set(self, set_str):
		self.configure(text = set_str)

class Button(tk.Label):
	"""Cross-platform button"""
	def __init__(self,frame,callback,**kw):
		self.callback = callback
		self.background = style.BUTTON_COLOR
		self.selected = False
		tk.Label.__init__(self, frame, **kw)
		self.configure(anchor="center")
		self.configure(background=self.background)
		self.configure(highlightthickness=1)
		if not "font" in kw.keys():
			self.configure(font = style.BUTTON_FONT)
		self.configure(highlightbackground = "#999999")
		self.bind('<Button-1>', self.on_click)

	# Use callback when our makeshift "button" clicked
	def on_click(self, event=None):
		self.configure(background="#dddddd")
		if not self.selected:
			self.after(100, self.on_click_color_change)
		if self.callback:
			self.callback()

	# Function to set the button's image
	def setimage(self, image):
		self.configure(image=image)

	# Function to set the button's text
	def settext(self, text):
		self.configure(text=text)

	def deselect(self):
		self.selected = False
		self.configure(background=self.background)

	def on_click_color_change(self):
		if not self.selected:
			self.configure(background=self.background)

class themedEntry(tk.Entry):
	def __init__(self, *args, **kw):
		tk.Entry.__init__(self, *args, **kw)
		theme(self, kw)

class labeledThemedEntry(themedEntry):
	"""Gives the PathEntry class a label"""
	def __init__(self, frame, text, *args, **kw):
		self.container = themedFrame(frame)
		label = tk.Label(self.container, text = text, background = style.primary_color, foreground = style.primary_text_color, font = style.path_entry_font)
		label.place(width = label.winfo_reqwidth(), relheight = 1)
		themedEntry.__init__(self, self.container, *args, **kw)		
		themedEntry.place(self, relwidth = 1, relheight = 1, width = - (label.winfo_reqwidth() + 5), x = label.winfo_reqwidth() + 5)
		self.text_var = tk.StringVar()
		self.configure(textvariable = self.text_var)
		self.configure(background = style.secondary_color)
		self.configure(foreground = style.ENTRY_FOREGROUND)
		self.configure(borderwidth = 0)
		self.configure(highlightthickness = 2)
		self.configure(highlightbackground = style.BUTTON_COLOR)

	def place(self, **kw):
		self.container.place(**kw)

	def set(self, string):
		self.text_var.set(string)

	def get_var(self):
		return self.text_var

	def get(self):
		return self.text_var.get()

class PathEntry(tk.Entry):
	"""Tkinter entry widget with a button to set the file path using tkinter's file dialog"""
	def __init__(self, frame, dir = False, filetypes = None, *args, **kw):
		self.dir = dir
		self.filetypes = filetypes
		container = themedFrame(frame)
		self.button = Button(container, self.set_path, text = "...", font = style.smallboldtext)
		self.button.place(relheight = 1, relx = 1, x = - style.BUTTONSIZE, width = style.BUTTONSIZE)
		tk.Entry.__init__(self, container, *args, **kw)
		self.text_var = tk.StringVar()
		self.configure(textvariable = self.text_var)
		self.configure(background = style.secondary_color)
		self.configure(foreground = style.ENTRY_FOREGROUND)
		self.configure(borderwidth = 0)
		self.configure(highlightthickness = 2)
		self.configure(highlightbackground = style.BUTTON_COLOR)
		super().place(relwidth = 1, relheight = 1, width = - style.BUTTONSIZE)
		self.container = container

	def clear(self):
		self.text_var.set("")

	def set(self, string):
		self.text_var.set(string)

	def get_var(self):
		return self.text_var

	def get(self):
		return self.text_var.get()

	def place(self, **kw):
		self.container.place(**kw)

	def set_path(self):
		if not self.dir:
			self.set(tkfiledialog.askopenfilename(filetypes = self.filetypes))
		else:
			self.set(tkfiledialog.askdirectory())

class LabeledPathEntry(PathEntry):
	"""Gives the PathEntry class a label"""
	def __init__(self, frame, text, *args, **kw):
		self.xtainer = themedFrame(frame)
		label = tk.Label(self.xtainer, text = text, background = style.primary_color, foreground = style.primary_text_color, font = style.path_entry_font)
		label.place(width = label.winfo_reqwidth(), relheight = 1)
		PathEntry.__init__(self, self.xtainer, *args, **kw)		
		PathEntry.place(self, relwidth = 1, relheight = 1, width = - (label.winfo_reqwidth() + 5), x = label.winfo_reqwidth() + 5)

	def place(self, **kw):
		self.xtainer.place(**kw)


class AutoScroll(object):
	def __init__(self, master):
		try:
			vsb = tk.Scrollbar(master, orient='vertical', command=self.yview, troughcolor = style.primary_color, bg = style.secondary_color)
		except:
			pass
		hsb = tk.Scrollbar(master, orient='horizontal', command=self.xview, troughcolor = style.primary_color, bg = style.secondary_color)

		try:
			self.configure(yscrollcommand=self._autoscroll(vsb))
		except:
			pass
		self.configure(xscrollcommand=self._autoscroll(hsb))

		self.grid(column=0, row=0, sticky='nsew')
		try:
			vsb.grid(column=1, row=0, sticky='ns')
		except:
			pass
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
			| tk.Place.__dict__.keys()

		for m in methods:
			if m[0] != '_' and m not in ('config', 'configure'):
				setattr(self, m, getattr(master, m))


	@staticmethod
	def _autoscroll(sbar):
		'''Hide and show scrollbar as needed.'''
		def wrapped(first, last):
			first, last = float(first), float(last)
			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def __str__(self):
		return str(self.master)


def _create_container(func):
	'''Creates a tk Frame with a given master, and use this new frame to
	place the scrollbars and the widget.'''
	def wrapped(cls, master, **kw):
		container = themedFrame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind(
			'<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)
	return wrapped


def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-MouseWheel>',
					   lambda e: _on_shiftmouse(e, child))
	else:
		child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
		child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		widget.unbind_all('<MouseWheel>')
		widget.unbind_all('<Shift-MouseWheel>')
	else:
		widget.unbind_all('<Button-4>')
		widget.unbind_all('<Button-5>')
		widget.unbind_all('<Shift-Button-4>')
		widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
	if platform.system() == 'Windows':
		widget.yview_scroll(-1 * int(event.delta / 120), 'units')
	elif platform.system() == 'Darwin':
		widget.yview_scroll(-1 * int(event.delta), 'units')
	else:
		if event.num == 4:
			widget.yview_scroll(-1, 'units')
		elif event.num == 5:
			widget.yview_scroll(1, 'units')


class ScrolledText(AutoScroll, tk.Text):
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

class ScrolledThemedText(AutoScroll, themedText):
	@_create_container
	def __init__(self, master, **kw):
		themedText.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, tk.Listbox):
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw,)
        AutoScroll.__init__(self, master)

class ScrolledThemedListbox(ScrolledListBox):
	def __init__(self, master, **kw):
		ScrolledListBox.__init__(self, master, **kw)
		theme(self, kw)

# from https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
class CreateToolTip(object):
	'''
	create a tooltip for a given widget
	'''
	def __init__(self, widget, text='widget info'):
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.close)

	def enter(self, event=None):
		x = y = 0
		x, y, cx, cy = self.widget.bbox("insert")
		x += self.widget.winfo_rootx()
		y += self.widget.winfo_rooty() + 20
		# creates a toplevel window
		self.tw = tk.Toplevel(self.widget)
		# Leaves only the label and removes the app window
		self.tw.wm_overrideredirect(True)
		self.tw.wm_geometry("+%d+%d" % (x, y))
		label = tk.Label(self.tw, text=self.text, justify='left',
					   background='gray', foreground = style.primary_text_color,
					   relief='solid', borderwidth=2,
					   font=("times", "12", "normal"),
					   wraplength = self.widget.winfo_width())
		label.pack(ipadx=1)

	def close(self, event=None):
		if self.tw:
			self.tw.destroy()


class textPage(themedFrame):
	def __init__(self, container, name, text):
		themedFrame.__init__(self, container)
		self.inner_frame = themedFrame(self)
		self.inner_frame.place(relwidth = 1, relheight = 1, x = + style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET, y = + style.STANDARD_OFFSET, height = - 2 * style.STANDARD_OFFSET)
		self.name = name
		textbox = ScrolledThemedText(self.inner_frame, wrap = "word", foreground = style.secondary_text_color)
		textbox.place(relwidth = 1, relheight = 1)
		textbox.insert("end", text)
		textbox.configure(state="disable")
