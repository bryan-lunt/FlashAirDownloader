import shutil
import os
import subprocess as sp
from urllib2 import urlparse
from LineReader import LineReader
from ORM import ORM, BackupFile

class BackupDaemon(object):
	def __init__(self, command_file, database_file, base_dir, tmp_dir):
		self.reader = LineReader(command_file)
		self.ORM = ORM(database_file)
		self.base_dir = base_dir
		self.tmp_dir = tmp_dir
	
	def run(self):
		for oneline in self.reader:
			thumb_hash, URL, priority = oneline.split() + [0]
			prority = int(priority)
			
			one_file = BackupFile()
			one_file.thumb_hash = thumb_hash
			one_file.name = os.path.basename(urlparse.urlsplit(URL).path)
			EXT = URL[-3:].upper()#FLASHAIR seems to only allow three-letter extensions

			if self.ORM.exists(one_file):
				print "file already exists!"
				continue #Nothing has been downloaded yet.
			
			#The thumb_hash must have been unique.

			tmp_filename = os.path.join(self.tmp_dir, thumb_hash + "." + EXT)

			retval = sp.call("curl '%s' > '%s'" % (URL, tmp_filename), shell=True)
			if retval != 0:
				continue #there was a problem. maybe try again later.
			
			
			md5sum = None
			try:
				#TODO: md5 of only the first few MB of large files. (Or the last few, to guard against truncated files.)
				#
				md5out = sp.check_output("md5sum %s" % tmp_filename, shell=True)
				md5sum, other = md5out.split()[:2]
				md5sum = md5sum.strip()
			except:
				pass
			
			one_file.full_hash = md5sum
			
			if self.ORM.exists(one_file):
				try:
					os.remove(tmp_filename)
				except:
					#maybe its alreayd gone?
					pass
				continue
			
			#Does not exist in the database
			#TODO: Set the creation date of the file (read that on input?)
			#TODO: Folders based on creation date
			#TODO: 
			
			new_name = os.path.join(self.base_dir, one_file.name)
			shutil.move(tmp_filename, new_name)
			
			self.ORM.store(one_file)
