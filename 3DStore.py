# A python app for installing 3DS Homebrew to an SD card using ihaveamac's custominstall
# Copyright (C) 2020 Andrew Spangler

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, json, platform, subprocess, threading
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import importlib.util
import webhandler, style
from lib3DS import lib3DSStore
import gui.widgets as widgets
from gui.categoryPage import CategoryPage
from gui.settingsPage import SettingsPage
from gui.installerPage import InstallerPage
from settings_tool import settings

settings.set_file("settings.json")

if not os.path.isfile("settings.json"):
	s = {
		"Launch fullscreen": False,
		"Details windows on top": False,
		"Details windows full screen": False,
		"Install cia if avialable": False,
		# "Delete cia after install": True,
		"boot9_path": "",
		"movable_path": "",
		"repo_url": "https://3ds.apps.fortheusers.org/",
	}
	settings.save_settings(s)

REPO_URL = settings.get_setting("repo_url")
REPO_JSON = REPO_URL + "repo.json"

class threader_object:
	def  __init__(self):
		self.running_threads = []
	"""an object to be declared outside of tk root so 
	things can be called asyncronously (you cannot start
	a new thread from within a tkinter callback so you
	must call it from an object that exists outside)"""
	def do_async(self, func, arglist = []):
		t = threading.Thread(target = func, args = arglist)
		t.start()
		self.running_threads.append(t)

	def join(self):
		for t in self.running_threads:
			t.join()
		self.running_threads = []


class gui(tk.Tk):
	def __init__(self, threader):
		tk.Tk.__init__(self)
		
		self.title("3DStore")
		self.minsize(600, 400)
		self.threader = threader
		self.installer = None
		self.fullScreenState = False
		self.zoomedScreenState = False
		self.topmostScreenState = False

		if settings.get_setting("Launch Fullscreen"):
			if platform.system() == 'Windows':
				try:
					self.statepages("fullscreen")
				except Exception as e:
					print("Error setting window launch type for Windows, this is a bug please report it:\n     {}".format(e))
			else:
				self.attributes("-fullscreen", True)

		self.f = widgets.themedFrame(self)
		self.f.place(relwidth = 1, relheight = 1)

		setup_frame = widgets.themedFrame(self.f)
		setup_frame.place(relwidth = 1, height = 20, rely = 0.60, y = -20, x = + style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET)
		
		self.sd_box = widgets.LabeledPathEntry(setup_frame, "Path to SD root -", dir = True)
		self.sd_box.place(relwidth = 1, height = 20)
		widgets.CreateToolTip(self.sd_box.xtainer, "Select the root of the sd card you wish to install the cias to.")

		console_frame = widgets.themedFrame(self.f)
		console_frame.place(relwidth = 1, relheight = 0.40, rely = 0.60, y = + style.STANDARD_OFFSET, height = - style.STANDARD_OFFSET)

		console_label = tk.Label(console_frame, text = "Console:", background = "black", foreground = "white", font = style.boldmonospace, borderwidth = 0, highlightthickness = 0)
		console_label.place(relwidth = 1, height = 20)
		self.console = widgets.ScrolledText(console_frame, background = "black", foreground = "white", highlightthickness = 0)
		self.console.place(relwidth = 1, relheight = 1, y = 20, height = - 20)

		repo_types = ["/repo.json", "/api/apps"]
		for t in repo_types:
			repo_json = REPO_URL.strip("/") + t
			repo_file = webhandler.getJson("3DS", repo_json)
			if repo_file:
				break
		if not repo_file:
			raise ValueError("Failed to download repository json.")

		self.handler = lib3DSStore(self.output_to_console, REPO_URL, repo_file)

		list_frame = widgets.themedFrame(self.f)
		list_frame.place(x = 0, y = 0, relwidth = 1, relheight = 0.60, height = - (style.STANDARD_OFFSET + 20))

		category_label = tk.Label(list_frame, text = "Categories", background = style.primary_color, foreground = style.primary_text_color, font = style.boldmonospace, anchor = "w")
		category_label.place(x = 0, y = 0, width = style.sidecolumnwidth, height = 20)

		self.category_listbox = widgets.ScrolledThemedListbox(list_frame, foreground = style.primary_text_color, borderwidth = 0, highlightthickness = 0, exportselection=0)
		self.category_listbox.configure(activestyle = "none")
		self.category_listbox.place(relx = 0, y = 20, relheight = 1, height = - 20, width = style.sidecolumnwidth)
		self.category_listbox.bind('<<ListboxSelect>>',self.select_frame)
		
		# the container is where stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be tkraise()'d above the others
		self.container = widgets.themedFrame(list_frame)
		self.container.place(x = style.sidecolumnwidth, width = - style.sidecolumnwidth, relwidth = 1, relheight = 1)

		frames = []

		category_pages = {
			"All" : self.handler.all,
			"Tools" : self.handler.tools,
			"Emulators" : self.handler.emus,
			"Games" : self.handler.games,
			"Advanced" : self.handler.advanced,
			"Misc." : self.handler.misc,
		}

		for frame in category_pages:
			if category_pages[frame]:
				f = CategoryPage(self, self.container, frame, category_pages[frame])
				frames.append(f)

		settings_frame = SettingsPage(self, self.container)
		installer_frame = InstallerPage(self, self.container)

		with open("gui/help.md") as h: helptext = h.read()
		help_frame = widgets.textPage(self.container, "HELP", helptext)

		frames.extend([installer_frame, help_frame, settings_frame])

		self.frames = {}
		for f in frames:
			f.place(relwidth = 1, relheight = 1)
			self.frames[f.name] = f
			self.category_listbox.insert('end', f.name)

		self.category_listbox.select_set(0)

		self.frames["All"].tkraise()

		self.bind("<F9>", self.toggle_topmost_screen)
		self.bind("<F10>", self.toggle_zoomed_screen)
		self.bind("<F11>", self.toggle_full_screen)

	def select_frame(self, event = None):
		try:
			selection=self.category_listbox.curselection()
			picked = self.category_listbox.get(selection[0])
			self.frames[picked].tkraise()
		except IndexError:
			pass

	def load_pages(self, pagelist):
		for F in pagelist:
			page_name = F.name
			self.frames[page_name] = F

			#place the frame to fill the whole window, stack them all in the same place
			F.place(relwidth = 1, relheight = 1)
			self.pagelist.append(F)

		self.category_listbox.delete(0, 'end')
		for page_name in self.frames.keys():
			self.category_listbox.insert("end", " {}".format(page_name))


	def install(self, package: dict, percent_handler): #percent_handle is function to pass to progress bar etc 
		"""Install libget-style 3ds package, install cia specified in "binary" value directly to the sd card."""

		# Todo: make sure only one instance of the same package can be being installed at a time
			
		sd_path = self.sd_box.get()
		if not sd_path:
			self.output_to_console("[USER MESSAGE]: - SD path not set, can't continue.")
			return "SD path not set, can't continue."

		self.handler.set_path(sd_path)

		#Store object handles printing errors to gui console and console.
		#Return a status if and only if the handler installs sucessfully and
		#the binary value in the passed package dict ends with '.cia'
		status = self.handler.install_package(package)
		name = package["name"]
		title = package["title"]
		if status: #If there was a cia in installed package
			if settings.get_setting("Install cia if avialable"):
				if not status.endswith(".cia"):
					return
				
				self.output_to_console("[PACKAGE INSTALLER]: Cia detected, installing cia.")

				sed_path = settings.get_setting("movable_path")
				if not sed_path:
					self.output_to_console("[USER MESSAGE]: - movable.sed path not set, can't continue, set it in the settings menu.")
					return "movable.sed path not set, can't continue."

				boot9_path = settings.get_setting("boot9_path")
				if not boot9_path:
					self.output_to_console("[USER MESSAGE]: - boot9.bin path not set, can't continue, set it in the settings menu.")
					return "boot9.bin path not set, can't continue."

			return self.install_files([status])

			# Todo: Figure out how to clean up cias since the installer starts its own 
			# thread and (grumble grumble bitch-whine-moan) this means I can't wait
			# for it to be done by my normal means to clean up the cia after.

	def install_files(self, files: list): #percent_handle is function to pass to progress bar etc 
		"""Install libget-style 3ds package, install cia specified in "binary" value directly to the sd card."""

		# Todo: make sure only one instance of the same package can be being installed at a time
			
		sd_path = self.sd_box.get()
		if not sd_path:
			self.output_to_console("[USER MESSAGE]: - SD path not set, can't continue.")
			return "SD path not set, can't continue."

		sed_path = settings.get_setting("movable_path")
		if not sed_path:
			self.output_to_console("[USER MESSAGE]: - movable.sed path not set, can't continue, set it in the settings menu.")
			return "movable.sed path not set, can't continue."

		boot9_path = settings.get_setting("boot9_path")
		if not boot9_path:
			self.output_to_console("[USER MESSAGE]: - boot9.bin path not set, can't continue, set it in the settings menu.")
			return "boot9.bin path not set, can't continue."

		if not self.installer:
			installscriptpath = os.path.join(os.path.dirname(__file__),"custominstall/custominstall.py")
			try:
				spec = importlib.util.spec_from_file_location("installer", installscriptpath)
				m = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(m)
				self.installer = m.CustomInstall
			except Exception as e:
				self.output_to_console(f"[PACKAGE INSTALLER]: ERROR - Failed to init installer object - {e}")
				return 

		installer = self.installer(boot9_path, sed_path, files, sd_path, False)

		def log_handle(msg, end='\n'):
			self.output_to_console(f"[PACKAGE INSTALLER]: {title} - {msg}")
		
		def percent_handle(total_percent, total_read, size):
			installer.log(f' {total_percent:>5.1f}%  {total_read:>.1f} MiB / {size:.1f} MiB\r', end='')

		installer.event.on_log_msg += log_handle
		installer.event.update_percentage += percent_handle

		installer.start()

	def output_to_console(self, outstring):
		print(outstring)
		self.console.insert('end', str(outstring) + "\n")
		self.console.see('end')

	def toggle_topmost_screen(self, event):
		self.topmostScreenState = not self.topmostScreenState
		self.attributes("-topmost", self.topmostScreenState)
		
	def toggle_zoomed_screen(self, event):
		self.zoomedScreenState = not self.zoomedScreenState
		self.attributes("-zoomed", self.zoomedScreenState)

	def toggle_full_screen(self, event):
		self.fullScreenState = not self.fullScreenState
		self.attributes("-fullscreen", self.fullScreenState)

if __name__ == "__main__":
	app = gui(threader_object())
	app.mainloop()