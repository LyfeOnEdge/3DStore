from .parser import Parser
from .store import Store

class lib3DSStore(Store, Parser):
	def __init__(self, out, repo_url, repo_file):
		Store.__init__(self, out, repo_url)
		Parser.__init__(self, out)
		Parser.load_file(self, repo_file)
