import urllib2
from datetime import datetime

class FlashAirFile(object):
	READ_ONLY  = 0b1
	HIDDEN     = 0b10
	SYSTEM     = 0b100
	VOLUME     = 0b1000
	DIRECTORY  = 0b10000
	ARCHIVE    = 0b100000
	def __init__(self, in_address, in_dir, in_filename, in_size, in_attributes, in_date, in_time):
		self.address = in_address
		self.dir = in_dir
		self.filename = in_filename
		self.size = int(in_size)
		self.attributes = int(in_attributes)
		
		date_int = int(in_date)#Worry about better conversion of these later
		year = ((date_int >> 9) & 0b1111111) + 1980
		month = ((date_int >> 5) & 0b1111)
		day = (date_int & 0b11111)
		
		time_int = int(in_time)#Worry about conversion later.
		hour = ((time_int >> 11) & 0b11111)
		minute = ((time_int >> 5) & 0b111111)
		second = ((time_int & 0b11111))*2
		
		try:
			self.date = datetime(year, month, day, hour, minute, second, 0)
		except:
			self.date = None#No time specified

	def full_name(self):
		return self.dir + "/" + self.filename
	
	def get_thumbnail_url(self):
		return self.address + "/thumbnail.cgi?" + self.dir + "/" + self.filename
	
	def get_url(self):
		return self.address + self.dir + "/" + self.filename

	def get_list(self):
		if not self.is_dir():
			raise Exception("This is not a directory.")
		listing = urllib2.urlopen(self.address + "/command.cgi?op=100&DIR=" + self.full_name())
                firstline = listing.readline().strip()
                if not firstline == "WLANSD_FILELIST":
			raise Exception("There was a problem listing the FlashAir directory.")
		for line in listing:
                        inputs = [self.address] + line.strip().split(',')
                        yield FlashAirFile(*inputs)
			
	def is_dir(self):
		return self.attributes & FlashAirFile.DIRECTORY

	def search_dir(self):
		if not self.is_dir():
			raise Exception("This is not a directory.")

		file_iterator = self.get_list()
		for one_file in file_iterator:
			if one_file.is_dir():
				sub_iter = one_file.get_list()
				for i in sub_iter:
					yield i
			else:
				yield one_file
