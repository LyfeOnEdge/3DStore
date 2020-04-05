import os, json
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import style
from .widgets import themedFrame, themedLabel, Button, themedListbox, LabeledPathEntry, CreateToolTip, labeledThemedEntry

class InstallerPage(themedFrame):
	def __init__(self, app: tk.Tk, container: tk.Frame):
		themedFrame.__init__(self, container)
		self.app = app
		self.name = "INSTALLER"

		self.container = themedFrame(self)
		self.container.place(relwidth = 1, relheight = 1, x = style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET, y = style.STANDARD_OFFSET, height = - 2 * style.STANDARD_OFFSET,)

		self.cia_container = themedFrame(self.container)
		self.cia_container.place(relwidth = 1, relheight = 1, height = -30)


		cia_label = themedLabel(self.cia_container, text = "cia paths - ")
		cia_label.place(relwidth = 1, height = 20)
		self.cia_box = themedListbox(self.cia_container, highlightthickness = 0)
		self.cia_box.place(relwidth = 1, relheight = 1, height = - 60, y = 30)
		CreateToolTip(cia_label, "Select the cias you wish to install to the sd card. The `add folder` button will add all cias in the selected folder, but will not check subdirs. The `remove cia` button will remove the currently selected file from the listbox.")

		add_cia_button = Button(self.cia_container, self.add_cia, text = "ADD CIA", font = style.monospace)
		add_cia_button.place(relx = 0, relwidth = 0.333, height = 20, rely = 1, y = - 20, width = - 6)
		
		add_cia_folder_button = Button(self.cia_container, self.add_cia_folder, text = "ADD FOLDER", font = style.monospace)
		add_cia_folder_button.place(relx = 0.333, relwidth = 0.333, height = 20, rely = 1, y = - 20, x = + 3, width = - 6)
		
		remove_cia_button = Button(self.cia_container, self.remove_cia, text = "REMOVE CIA", font = style.monospace)
		remove_cia_button.place(relx = 0.666, relwidth = 0.333, height = 20, rely = 1, y = - 20, x = + 6, width = - 6)

		install_button = Button(self.container, self.install, text = "INSTALL CIAS", font = style.monospace)
		install_button.place(rely = 1, y = - 20, height = 20, relwidth = 1)

	def add_cia(self):
		cia_to_add = tkfiledialog.askopenfilename(filetypes = [('cia file', '*.cia')])
		if cia_to_add:
			self.cia_box.insert('end', cia_to_add)

	def add_cia_folder(self):
		cia_dir_to_add = tkfiledialog.askdirectory()
		if cia_dir_to_add:
			cias_to_add = [f for f in os.listdir(cia_dir_to_add) if (os.path.isfile(os.path.join(cia_dir_to_add, f)) and f.endswith(".cia"))]
			if cias_to_add:
				for cia_to_add in cias_to_add:
					self.cia_box.insert('end', cia_to_add)

	def remove_cia(self):
		index = self.cia_box.curselection()
		if index:
			self.cia_box.delete(index)
			if self.cia_box.size():
				self.cia_box.select_clear(0, 'end')
				if self.cia_box.size() > 1:
					try:
						self.cia_box.select_set(index)
					except:
						pass
				else:
					self.cia_box.select_set(0)

	def install(self):
		cias = []
		for i in range(0, self.cia_box.size()):
			cias.append(self.cia_box.get(i).strip())
		self.app.install_files(cias)