import sqlite3

class BackupFile(object):
	def __init__(self):
		self.thumb_hash = None
		self.full_hash = None
		self.name = None


#This may all seem complicated, but SQLITE3 doesn't have 128 bit integer types.
#I want to use the md5 hash, because it is standard, but I want to use SQLITE3.
#why not use a text column, you ask? Beause it is far far faster to compare integers, and they are easier/faster to index.


def _split_hash(hash_value):
	if isinstance(hash_value, str):
		hash_value = int('0x'+hash_value,16)
	upper = (hash_value & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000000000000000000000000000L ) >> 64
	lower = (hash_value & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFL )
	
	return upper, lower

def _combine_hash(upper, lower):
	return upper << 64 | lower

class ORM(object):
	def __init__(self, URL):
		self.connection = sqlite3.connect(URL)
		c = self.connection.cursor()
		
		c.execute("create table if not exists backupfiles ( thumb_hash_high integer, thumb_hash_low integer, full_hash_high integer, full_hash_low integer, name varchar unique, unique (thumb_hash_high, thumb_hash_low), unique (full_hash_high, full_hash_low) )")
		
		self.connection.commit()

	
	def exists(self, test_file):
		c = self.connection.cursor()
		thumb_up, thumb_low = _split_hash(test_file.thumb_hash)
		full_up, full_low = _split_hash(test_file.full_hash)
		
		c.execute("select count(*) from backupfiles where (thumb_hash_high = ? and thumb_hash_low = ?) or (full_hash_high = ? and full_hash_low = ?)",
			(thumb_up, thumb_low, full_up, full_low))
		result = c.fetchone()
		if result is not None and len(result) > 0 and int(result[0]) > 0:
			return True
		else:
			return False

	def store(self, test_file):
		c = self.connection.cursor()
		
                thumb_up, thumb_low = _split_hash(test_file.thumb_hash)
                full_up, full_low = _split_hash(test_file.full_hash)
		c.execute("insert into backupfiles values ( ?, ?, ?, ?, ?)",
			(thumb_up, thumb_low, full_up, full_low, test_file.name))
		self.connection.commit()
			
