import requests
from lxml.html import fromstring
import json


def main(url):
	response = requests.get(url, allow_redirects=True)
	tree = fromstring(response.text)
	results = {}
	for meta in tree.cssselect('meta'):
		if "name" in meta.keys():
			results[meta.get("name")] = meta.get("content")
		elif "property" in meta.keys():
			results[meta.get("property")] = meta.get("content")
	print json.dumps(results, indent=4, sort_keys=True)


if __name__ == '__main__':
	import sys
	main(sys.argv[1])
