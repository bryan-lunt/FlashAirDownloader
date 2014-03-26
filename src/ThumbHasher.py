from __future__ import print_function

from FlashAir import *

class ThumbHasher(object):
	def __init__(self, flash_air_address, target_directories=['/DCIM']):
		self.flash_air_address = flash_air_address
		self.target_dirs = [FlashAirFile(*([self.flash_air_address] + i.rsplit('/',1) + [ 0, 16, 0 ,0])) for i in target_directories]
	
	def search(self):
		for td in self.target_dirs:
			for i in td.search_dir():
				yield i

if __name__ == "__main__":
	myHasher = ThumbHasher("http://192.168.0.104")
	for i in myHasher.search():
		print(i.get_url(), i.get_thumbnail_url())	
