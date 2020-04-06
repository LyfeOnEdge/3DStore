# Some basic scripts for installing 3ds homebrew
# (INCREDIBLY) Loosely based on vgmoose's libget here: https://github.com/vgmoose/libget
# Licensed under GPL3
# By LyfeOnEdge

import os, sys, json
from io import BytesIO
from zipfile import ZipFile
import urllib.request 

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

DOWNLOADSFOLDER = "downloads"
CACHEFOLDER = "cache"
ICON  = "icon.png"
SCREEN = "screen.png"
SCREENBUFFER = {}
ICONBUFFER = {}


# Name of package info file
PACKAGE_INFO = "info.json"
# Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"

LIBGET = "libget"
TINYDB = "tinydb"

class Store(object):
	def __init__(self, out, repo_url):
		self.base_install_path = None
		self.out = out

		self.repo_url = repo_url
		store_url = "{}{}".format(repo_url, "{}")
		self.image_base_url = store_url.format("packages/{}/{}")
		self.package_url = "{}zips/{}.zip".format(repo_url, "{}")

	def set_path(self, path: str, silent = False):
		self.base_install_path = path
		if self.base_install_path:
			if not silent:
				self.out(f"Set SD Root path to {path}")
		else:
			if not silent:
				self.out("Invalid path set")

	def check_path(self):
		return self.base_install_path

	def download(self, url, file, silent = False):
		try:
			urllib.request.urlretrieve(url,file)
			return file
		except Exception as e:
			if not silent:
				print("failed to download file - {} from url - {}, reason: {}".format(file, url, e)) 
			return None

	def download_object(self, remote_name):
		try:
			r = urllib.request.urlopen(remote_name)
			if r.getcode() == 200:
				return r.read()
		except Exception as e:
			self.out(e)

	#Gets (downloads or grabs from cache) an image of a given type (icon or screenshot) for a given package
	def getImage(self, package, image_type, force = False):
		"""Gets an image, given a package name and image type"""
		path = os.path.join(os.path.join(sys.path[0], CACHEFOLDER), package["name"].replace(":",""))
		if not os.path.isdir(path):
			os.mkdir(path)

		image_file = os.path.join(path, image_type)

		if os.path.isfile(image_file) and not force:
			return(image_file)
		else:
			if package["type"] == LIBGET:
				return self.download(self.image_base_url.format(package["name"], image_type), image_file, silent = False)
			elif package["type"] == TINYDB:
				id = package["id"]
				vid = package["vid"]
				return self.download(self.repo_url + f"qr/{id}/{vid}/QR.png", image_file, silent = False)

	def getPackageIcon(self, package, force = False):
		"""Gets the icon for a given package"""
		if package["name"] in ICONBUFFER.keys():
			return ICONBUFFER[package["name"]]
		icon = self.getImage(package, ICON, force = force)
		ICONBUFFER.update({package["name"] : icon})
		return icon

	def getScreenImage(self, package, force = False):
		"""Gets the screenshot for a given package"""
		if package["name"] in SCREENBUFFER.keys():
			return SCREENBUFFER[package["name"]]
		screen = self.getImage(package, SCREEN, force = force)
		SCREENBUFFER.update({package["name"] : screen})
		return screen

	def getPackage(self, package):
		"""Downloads the current zip of a package"""
		try:
			packageURL = self.package_url.format(package)
			return self.download_object(packageURL)
		except Exception as e:
			print("Error getting package zip for {} - {}".format(package, e))

	def install_package(self, package: dict):
		"""Installs a libget package"""
		if not package:
			self.out("[INSTALLER]: No package entry passed")
			self.out("[INSTALLER]: Not continuing with install")
			return

		try:
			package_name = package["name"]
		except:
			self.out("[INSTALLER]: Error - package name not found in package data")
			self.out("[INSTALLER]: Not continuing with install")
			return

		version = package.get("version")
		self.out(f"[INSTALLER]: Installing {package_name} - {version}" if version else (f"Installing {package_name}"))
		if not version: version = "0"

		self.out(f"[INSTALLER]: Beginning install for package {package_name}")

		if package["type"] == LIBGET:
			package_zip = self.getPackage(package_name)
			if not package_zip:
				self.out(f"[INSTALLER]: Failed to download zip for package {package_name}")
				return
			package_object = BytesIO(package_zip)
			with ZipFile(package_object) as zipObj:
				# Extract everything but the manifest and the info file
				extract_manifest = []
				for filename in zipObj.namelist():
					if filename == PACKAGE_MANIFEST or filename == PACKAGE_INFO:
						pass
					else:
						zipObj.extract(filename, path=self.base_install_path)
						extract_manifest.append(filename)

			self.out("[INSTALLER]: Extracted: {}".format(json.dumps(extract_manifest, indent=4)))
			if not "binary" in package.keys():
				self.out("[INSTALLER]: No binary.")
				return ""
			return os.path.join(self.base_install_path, package["binary"])

		elif package["type"] == TINYDB:
			cia_path = f"/cias/{package_name}.cia"
			cia = self.download(package["download_url"], os.path.join(self.base_install_path + cia_path))
			if not cia:
				self.out(f"[INSTALLER]: Failed to download cia for {package_name}")
			else:
				self.out(f"[INSTALLER]: Downloaded cia for {package_name}")
			return cia

		else:
			raise

		


