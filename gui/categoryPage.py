import tkinter as tk
from .widgets import themedFrame
from .detailsPage import DetailsPage
from .table import Table

class CategoryPage(themedFrame):
	def __init__(self,
				 app: tk.Tk,
				 container: tk.Frame,
				 name,
				 packages: list = [],
				 ):
		themedFrame.__init__(self, container)
		# assert len(category_packages) != 0,"No packages!"
		self.app = app
		self.name = name
		self.packages = packages
		self.handler = self.app.handler

		self.table = Table(self, on_selection_event = self.open_details)
		self.table.place(relheight = 1, relwidth = 1)
		self.build_table(self.packages)
		
	def on_listbox_selection(self, event):
		selection=self.package_listbox.curselection()
		picked = self.package_listbox.get(selection[0])
		for package in self.packages:
			if package["name"] == picked:
				self.open_details(package)

	def build_table(self, packages):
		if not packages:
			return

		table_data = {
			"Package": [],
			"Title": [],
			"Author": [],
			"Version": [],
			"Updated": []
		}
		for package in packages:
			if not package:
				continue
			table_data["Package"].append(package["name"].strip())
			table_data["Title"].append(package["title"].strip())
			table_data["Author"].append(package["author"].strip())
			table_data["Version"].append(package["version"].strip())
			table_data["Updated"].append(package["updated"].strip())

		self.table.build(table_data)

	def open_details(self, pkg):
		package = self.handler.get_package_by_name(pkg)
		page = DetailsPage(self.app, self.handler, package)