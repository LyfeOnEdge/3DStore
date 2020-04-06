#A basic python object for parsing a libget json into lists per category
#Copyright LyfeOnEdge 2019, 2020
#Licensed under GPL3
import json



LIBGET = "libget"

TINYDB = "tinydb"
TINYDB_CATEGORY_MAP = {
	1 : "All",
	3 : "Save Tools",
	4 : "Games"
}


class Parser(object):
	def __init__(self, out):
		"""Python object to hold appstore repo"""
		self.out = out
		self.mode = None
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
			"Games" : self.games,
			"game" : self.games,
			"loader" : self.loaders,
			"theme" : self.themes,
			"Save Tools" : self.tools,
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
		""""Loads json file as a large list of dicts"""
		if not repo_json:
			return

		# try:
		with open(repo_json, encoding="utf-8") as repojson:
			j = json.load(repojson)
			if "packages" in j:
				self.mode = LIBGET
				self.clear()
				self.all = j["packages"]
			else:
				self.mode = TINYDB
				self.clear()
				self.all = j

		self.sort()
		# except Exception as e:
		# 	self.out(f"Exception loading repo json {e}")
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
		if self.mode == LIBGET:
			if self.all:
				for entry in self.all:
					try:
						entry["type"] = LIBGET
						self.map[entry["category"]].append(entry)
					except Exception as e:
						pkg = entry["name"]
						self.out(f"Error sorting {pkg} - {e}")
		elif self.mode == TINYDB:
			if self.all:
				al = self.all.copy()
				self.all = []
				for entry in al:
					p = {}
					p["name"] = entry["name"]
					p["title"] = entry["name"]
					p["author"] = entry["author"]
					p["description"] = entry["headline"]
					p["details"] = entry["headline"]
					p["category"] = TINYDB_CATEGORY_MAP.get(max(entry["categories"]))
					p["type"] = TINYDB

					for c in reversed(entry["cia"]):
						cia = c
						break
					p["download_url"] = cia["download_url"]
					p["version"] = cia["version"]
					p["updated"] = cia["mtime"]
					p["titleid"] = cia["titleid"]
					p["license"] = "n/a"
					p["id"] = entry["id"]
					p["vid"] = cia["id"]

					try:
						if not p["category"] == "All":
							self.map[p["category"]].append(p)
					except Exception as e:
						p = entry["name"]
						self.out(f"Error sorting {p} - {e}")

					self.all.append(p)