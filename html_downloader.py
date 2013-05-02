import urllib
from google import search
import sys

linkedin_ireland_url = 'http://ie.linkedin.com/in/'

# Download the html and store to a location specified by file_name
def downloadHtml(url, file_name):

	wp = urllib.urlopen(url)

	wp_stream = wp.read()

	wp_file = open(file_name,'w')

	wp_file.write(wp_stream);

	wp.close()
	wp_file.close()

# Just like in Google, type: "keyword site:http://ie.linkedin.com/in/"
# and download the cotent from return ulrs
def googleSearch(keywords, site = linkedin_ireland_url, num = 20):
	urls = []
	urls[:] = search(keywords + ' ' + 'site:' + site, stop = num)

	urls[:] = (str(value) for value in urls if str(value).startswith(linkedin_ireland_url) == True)
	return urls

# Search and Download
def downloader(keywords, site = linkedin_ireland_url, num = 20, path = './user_raw/', postfix = '.htm'):
	urls = googleSearch(keywords)

	for url in urls:
		file_name = url.rsplit('/', 1)[1]
		downloadHtml(url, path+file_name+postfix)

def main(argv):	
	for i in range(1, len(argv)):
		downloader(argv[i], num = 3)

if __name__ == "__main__":
    main(sys.argv)