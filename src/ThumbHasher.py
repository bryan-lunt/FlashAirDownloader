from __future__ import print_function

from FlashAir import *

class ThumbHasher(object):
	def __init__(self, flash_air_address, target_directories=['/DCIM']):
		self.flash_air_address = flash_air_address
		self.target_dirs = [FlashAirFile(*([self.flash_air_address] + i.rsplit('/',1) + [ 0, 16, 0 ,0])) for i in target_directories]
	
	def search_dir(self,dir_as_f_file):

		file_iterator = dir_as_f_file.get_list()
		for one_file in file_iterator:
			if one_file.is_dir():
				sub_iter = one_file.get_list()
				for i in sub_iter:
					yield i
			else:
				yield one_file
	def search(self):
		for td in self.target_dirs:
			for i in self.search_dir(td):
				yield i

if __name__ == "__main__":
	myHasher = ThumbHasher("http://192.168.0.104")
	for i in myHasher.search():
		print(i.get_url(), i.get_thumbnail_url())	
