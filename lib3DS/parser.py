#A basic python object for parsing a libget json into lists per category
#Copyright LyfeOnEdge 2019, 2020
#Licensed under GPL3
import json
class Parser(object):
	def __init__(self, out):
		"""Python object to hold appstore repo"""
		self.out = out
		self.init()

	def init(self):
		self.all = []
		self.advanced = []
		self.emus = []
		self.games = []
		self.loaders = []
		self.themes = []
		self.tools = []
		self.misc = []
		self.legacy = []

		self.map = {
			"advanced" : self.advanced,
			"concept" : self.misc,
			"emu" : self.emus,
			"game" : self.games,
			"loader" : self.loaders,
			"theme" : self.themes,
			"tool" : self.tools,
			"_misc" : self.misc,
			"media" : self.misc,
			"misc" : self.misc,
			"legacy" : self.legacy,
		}

	def clear(self):
		"""Clears all lists"""
		self.init()
		
	def load_file(self, repo_json):
		""""Loads libget json file as a large list of dicts"""
		if not repo_json:
			return
		self.clear()
		try:
			with open(repo_json, encoding="utf-8") as repojson:
				self.all = json.load(repojson)["packages"]
			self.sort()
		except Exception as e:
			self.out(f"Exception loading repo json {e}")
		num_entries = len(self.all)
		self.out(f"Loaded {num_entries} packages")

	def load_json(self, repo_json):
		""""Loads libget json object as a large list of dicts"""
		if not repo_json:
			return
		self.clear()
		self.all = repo_json["packages"]
		self.sort()
		num_entries = len(self.all)
		self.out(f"Loaded {num_entries} packages")

	def get_package_by_name(self, package_name: str):
		"""Returns a package dict given a package name,
		returns none if nothing is found."""
		for package in self.all:
			if package["name"] == package_name:
				return package

	def get_package_by_title(self, package_title: str):
		"""WARNING, LIBGET REPOS CAN CONCEIVABLY CONTAIN
		MULTIPLE PACKAGES WITH THE SAME TITLE. This will
		return the first instance of a package with the
		given title. Probably a non-issue, but if you
		are for some reason using this lib to obtain
		homebrew programatically, you should probably use
		self.get_package_by_name() """

		for package in self.all:
			if package["title"] == package_title:
				return package 

	def sort(self):
		"""sorts list into smaller chunks by category"""
		if self.all:
			for entry in self.all:
				try:
					self.map[entry["category"]].append(entry)
				except Exception as e:
					pkg = entry["name"]
					self.out(f"Error sorting {pkg} - {e}")