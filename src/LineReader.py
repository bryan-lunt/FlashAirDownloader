import io

class LineReader(object):
	def __init__(self, filename):
		self.stream = io.open(filename)
	
	def __iter__(self):
		while True:
			oneline = self.stream.readline()
			if oneline not in [None, ""]:
				#throttle up
				yield oneline
			else:
				pass#throttle down.
			#wait according to throttle

