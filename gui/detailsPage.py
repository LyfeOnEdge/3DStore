import traceback
import tkinter as tk
from PIL import Image, ImageTk
import style
from .widgets import themedFrame, themedLabel, Button, ScrolledThemedText

class DetailsPage(tk.Toplevel):
	def __init__(self, app, package_handler, package):
		tk.Toplevel.__init__(self)
		name = package["name"]
		self.wm_title(f"Details: {name}")
		self.minsize(500, 300)
		self.image = None

		self.app = app
		self.package_handler = package_handler
		self.package = package

		self.banner_locked = False

		self.progress_frame = themedFrame(self)
		self.progress_frame.place(relwidth = 1, relheight = 1)

		self.progress_label = themedLabel(self.progress_frame)
		self.progress_label.place(relwidth = 1, relheight = 1, height = - (style.BUTTONSIZE + 2 * style.STANDARD_OFFSET))

		self.back_button = Button(self.progress_frame, 
			callback = self.on_back_button, 
			text = "BACK", 
			font=style.mediumboldtext, 
			background=style.secondary_color
			)

		self.body = themedFrame(self, background = style.secondary_color)
		self.body.place(relwidth = 1, relheight = 1, width = -style.detailssidecolumnwidth)

		self.image_frame = themedFrame(self.body, background = style.secondary_color)
		self.image_frame.place(relwidth=1, relheight = style.details_page_image_fraction, x = + style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET)

		self.banner_image = themedLabel(self.image_frame,background = style.secondary_color,anchor="center",wraplength = None)
		self.banner_image.place(relwidth = 1, relheight = 1)

		self.description = ScrolledThemedText(self.body, font = style.smalltext, fg = style.details_page_label_color)
		self.description.place(relwidth = 1, x = style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET,  rely = style.details_page_image_fraction, height = 40)

		self.details = ScrolledThemedText(self.body, font = style.smalltext, fg = style.details_page_label_color)
		self.details.place(relwidth = 1, x = style.STANDARD_OFFSET, width = - 2 * style.STANDARD_OFFSET, rely = style.details_page_image_fraction, y = 40 + style.STANDARD_OFFSET, relheight = 1 - style.details_page_image_fraction, height = - (2 * style.STANDARD_OFFSET + 40))

		#RIGHT COLUMN
		self.column = themedFrame(self, background = style.primary_color)
		self.column.place(relx = 1, rely = 0, width = style.detailssidecolumnwidth, relheight = 1, x = - style.detailssidecolumnwidth)

		self.column_body = themedFrame(self.column, background = style.primary_color)
		self.column_body.place(relwidth=1, relheight=1)

		self.column_title = themedLabel(self.column_body,anchor="w",font=style.mediumboldtext, fg = style.primary_text_color, background = style.primary_color)
		self.column_title.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, rely = 0, relwidth = 1, height = style.details_page_title_height, y =  + style.STANDARD_OFFSET)

		self.column_author = themedLabel(self.column_body,anchor="w",font=style.smalltext, fg = style.primary_text_color, background = style.primary_color)
		self.column_author.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, y = style.details_page_title_height + style.STANDARD_OFFSET, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

		self.column_version = themedLabel(self.column_body,anchor="w",font=style.smalltext, fg = style.primary_text_color, background = style.primary_color)
		self.column_version.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, y = style.details_page_title_height + 0.333 * style.details_item_y_multiplier + style.STANDARD_OFFSET, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

		self.column_license = themedLabel(self.column_body,anchor="w",font=style.smalltext, fg = style.primary_text_color, background = style.primary_color)
		self.column_license.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, y = style.details_page_title_height + 0.666 * style.details_item_y_multiplier + style.STANDARD_OFFSET, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

		self.column_package = themedLabel(self.column_body,anchor="w",font=style.smalltext, fg = style.primary_text_color, background = style.primary_color)
		self.column_package.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, y = style.details_page_title_height + 1.000 * style.details_item_y_multiplier + style.STANDARD_OFFSET, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

		self.column_downloads = themedLabel(self.column_body,anchor="w",font=style.smalltext, fg = style.primary_text_color, background = style.primary_color)
		self.column_downloads.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, y = style.details_page_title_height + 1.333 * style.details_item_y_multiplier + style.STANDARD_OFFSET, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

		self.column_updated = themedLabel(self.column_body,anchor="w",font=style.smalltext, fg = style.primary_text_color, background = style.primary_color)
		self.column_updated.place(x = style.STANDARD_OFFSET, width = - style.STANDARD_OFFSET, y = style.details_page_title_height + 1.666 * style.details_item_y_multiplier + style.STANDARD_OFFSET, relwidth = 1, height = 0.333 * style.details_item_y_multiplier)

		self.column_install_button = Button(self.column_body, 
			callback = self.trigger_install, 
			text = "INSTALL", 
			font=style.mediumboldtext, 
			background=style.secondary_color
			)
		self.column_install_button.place(rely=1,relwidth = 1, x = + style.STANDARD_OFFSET, y = - 2 * (style.BUTTONSIZE + style.STANDARD_OFFSET), width = - 2 * style.STANDARD_OFFSET, height = style.BUTTONSIZE)

		self.column_exit_button = Button(self.column_body, 
			callback = self.exit_window, 
			text = "EXIT (ESC)", 
			font=style.mediumboldtext, 
			background=style.secondary_color
			)
		self.column_exit_button.place(rely=1,relwidth = 1, x = + style.STANDARD_OFFSET, y = - 1 * (style.BUTTONSIZE + style.STANDARD_OFFSET), width = - 2 * style.STANDARD_OFFSET, height = style.BUTTONSIZE)

		# self.progress_bar = progressFrame.ProgressFrame(self)

		# self.yesnoPage = YesNoPage(self)
		self.bind("<Escape>", self.exit_window)

		self.app.threader.do_async(self.update_page, [package])
		self.bind("<Configure>", self.on_configure)

	def update_page(self,package):
		self.package = package
		self.app.threader.do_async(self.update_banner)

		self.column_title.set("Title: {}".format(package["title"]))

		self.column_author.set("Author: {}".format(package["author"]))
		self.column_version.set("Latest Version: {}".format(package["version"]))
		try:
			self.column_license.set("License: {}".format(package["license"]))
		except:
			self.column_license.set("License: N/A")

		self.column_package.set("Package: {}".format(package["name"]))

		ttl_dl = 0
		try:
			ttl_dl += package["web_dls"]
		except:
			pass
		try:
			ttl_dl += package["app_dls"]
		except:
			pass

		self.column_downloads.set("Downloads: {}".format(ttl_dl))
		self.column_updated.set("Updated: {}".format(package["updated"]))
		self.description.set(package["description"].replace("\\n", "\n"))
		self.details.set(package["details"].replace("\\n", "\n"))

	def on_configure(self, event=None):
		self.update_banner()

	def update_banner(self):
		if self.banner_locked: return
		self.banner_locked = True
		if not self.image:
			bannerimage = self.package_handler.getScreenImage(self.package["name"])
			if not bannerimage:
				bannerimage = "gui/notfound.png"

			self.image = Image.open(bannerimage)
		
		self.do_update_banner()
		self.banner_locked = False

	def do_update_banner(self):
		maxheight = self.image_frame.winfo_height()
		maxwidth = self.image_frame.winfo_width()
		
		#Math to make image fit
		if maxwidth > 0 and maxheight > 0:
			wpercent = (maxwidth/float(self.image.size[0]))
			hsize = int((float(self.image.size[1])*float(wpercent)))
			if hsize <= 0: return
			new_image = self.image.resize((maxwidth,hsize), Image.ANTIALIAS)
			if new_image.size[1] > maxheight:
				hpercent = (maxheight/float(self.image.size[1]))
				wsize = int((float(self.image.size[0])*float(hpercent)))
				if wsize <= 0: return
				new_image = self.image.resize((wsize,maxheight), Image.ANTIALIAS)

			new_image = ImageTk.PhotoImage(new_image)

			self.banner_image.configure(image=new_image)
			self.banner_image.image = new_image

	def trigger_install(self):
		self.progress_frame.tkraise()
		try:
			status = self.app.install(self.package, self.progress_label.set)
		except Exception as e:
			status = traceback.format_exc()
		if "path not set" in status:
			self.place_back_button()
		self.progress_label.set(f"Install Status -\n\n{status}")

	def on_back_button(self):
		self.back_button.place_forget()
		self.body.tkraise()
		self.column.tkraise()

	def place_back_button(self):
		self.back_button.place(rely=1,relwidth = 1, x = + 2 * style.STANDARD_OFFSET, y = - 1 * (style.BUTTONSIZE + style.STANDARD_OFFSET), width = - 4 * style.STANDARD_OFFSET, height = style.BUTTONSIZE)

	def exit_window(self, event = None):
		self.destroy()