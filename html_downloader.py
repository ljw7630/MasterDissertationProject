import urllib
from google import search
import string
import html_parser

class HTMLDownloader:

	# Download the html and store to a location specified by file_name
	def download(self, url, file_name):
		wp = urllib.urlopen(url)

		wp_stream = wp.read()

		wp_file = open(file_name,'w')

		wp_file.write(wp_stream);

		wp.close()
		wp_file.close()


class PublicProfileDownloader:
	_linkedin_ireland_url = 'http://ie.linkedin.com/in/'

	# Just like in Google, type: "keyword site:http://ie.linkedin.com/in/"
	# and download the cotent from return ulrs
	def googleSearch(self, keywords, site = _linkedin_ireland_url, num = 20):
		urls = []
		urls[:] = search(keywords + ' ' + 'site:' + site, stop = num)

		urls[:] = (str(value) for value in urls if str(value).startswith(_linkedin_ireland_url) == True)
		return urls

	# Search and Download
	def download(self, keywords, site = _linkedin_ireland_url, num = 20, path = './user_raw/', postfix = '.htm'):
		urls = self.googleSearch(keywords)
		html_downloader = HTMLDownloader()
		for url in urls:
			file_name = url.rsplit('/', 1)[1]
			html_downloader.download(url, path+file_name+postfix)

# Download skills from research gate
class SkillDownloader:
	_research_gate_topic_url = 'https://www.researchgate.net/topics/'
	_folder_path = './resources/'

	def download(self, site = _research_gate_topic_url, store_path = _folder_path, postfix='.htm'):
		html_downloader = HTMLDownloader()
		for c in string.uppercase:
			url = site + c + '/'
			path = store_path + 'skill/' + c + postfix
			html_downloader.download(url, path)
			parser = html_parser.SkillParser(path)
			pages = parser.getNumberOfPages()
			for i in range(2, pages+1):
				url = site + c + '/?page=' + str(i)
				path = store_path + 'skill/' + c + '_' + str(i) + postfix
				html_downloader.download(url, path)



# def main(argv):
# 	profile_downloader = PublicProfileDownloader()
# 	for i in range(1, len(argv)):
# 		profile_downloader.download(argv[i], num = 3)

# if __name__ == "__main__":
# 	main(sys.argv)

if __name__ == "__main__":
	skd = SkillDownloader()
	skd.download() 