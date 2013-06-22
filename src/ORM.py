import sqlite3

class BackupFile(object):
	def __init__(self):
		self.thumb_hash = None
		self.full_hash = None
		self.name = None


class ORM(object):
	def __init__(self, URL):
		self.connection = sqlite3.connect(URL)
		c = self.connection.cursor()
		
		c.execute("create table if not exists backupfiles ( thumb_hash unique, full_hash unique, name varchar unique)")
		
		self.connection.commit()

	
	def exists(self, test_file):
		c = self.connection.cursor()
		
		c.execute("select count(*) from backupfiles where thumb_hash = ? or full_hash = ?", (test_file.thumb_hash, test_file.full_hash) )
		result = c.fetchone()
		if result is not None and len(result) > 0 and int(result[0]) > 0:
			return True
		else:
			return False

	def store(self, test_file):
		c = self.connection.cursor()
		
		c.execute("insert into backupfiles values ( ?, ?, ?)", (test_file.thumb_hash, test_file.full_hash, test_file.name) )
		self.connection.commit()
		
