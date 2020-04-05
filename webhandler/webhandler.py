import os, sys, shutil
from .etags import accessETaggedFile

#web handling
import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

#Variable to map previously downloaded jsons to minimize repeated downloads
filedict = {}

if not os.path.isdir("cache"):
	os.mkdir("cache")

#opens a url in a new tab
def opentab(url):
	import webbrowser
	webbrowser.open_new_tab(url)

#Download a file at a url, returns file path
def download(fileURL):
	try:
		downloadedfile, headers = urllib.request.urlretrieve(fileURL)
		print(headers)
		filename = headers["Content-Disposition"].split("filename=",1)[1]
		downloadlocation = os.path.join("downloads",filename)
		shutil.move(downloadedfile, downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return filename
	except Exception as e: 
		print(e)
		return None

def getJson(jsonname, apiurl):
	try:
		jsonfile = os.path.join("cache", jsonname + ".json")
		jfile = accessETaggedFile(apiurl,jsonfile)
		return jfile
	except Exception as e:
		print(e)
		print("failed to download json file for {}".format(jsonname))
		return None

def getCachedJson(jsonname):
	return os.path.join("cache", jsonname + ".json")

def download_object(remote_name):
    try:
        r = urllib.request.urlopen(remote_name)
        if r.getcode() == 200:
            return r.read()
    except urllib.error.HTTPError:
        print("Error getting app update data (github quota exceeded?)")
    except Exception as e:
        print(e)