import socket
import re

HOST = 'localhost'
PORT = 12345


class SocketHandler:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST, PORT))
		self.fid = self.s.makefile()

	def send_index_command(self):
		self.s.sendall('index\n')

	def send_query_command(self):
		self.s.sendall('query\n')

	def send_query(self, query_string):
		pass


class CourseSocketHandler(SocketHandler):

	def send_index_command(self):
		SocketHandler.send_index_command(self)
		self.s.sendall('CourseSearchEngine\n')

	def send_query_command(self):
		SocketHandler.send_query_command(self)
		self.s.sendall('CourseSearchEngine\n')

	def send_query(self, query_string):
		query_string += '\n'
		self.s.sendall(query_string)

		data = self.fid.readline().strip()

		return data

	def close(self):
		self.s.close()


class DegreeSocketHandler(SocketHandler):

	def send_index_command(self):
		SocketHandler.send_index_command(self)
		self.s.sendall('DegreeSearchEngine\n')

	def send_query_command(self):
		SocketHandler.send_query_command(self)
		self.s.sendall('DegreeSearchEngine\n')

	def send_query(self, query_string, change=True):
		if change:
			query_string = self.clean_query_string(query_string)
		query_string += '\n'

		self.s.sendall(query_string)

		data = self.fid.readline()
		data = data.strip().split(',')
		return data[0], data[1]

	def clean_query_string(self, query_string):
		old_query_string = query_string
		p = re.compile(r'(.*?)(\(.*\))', re.M)
		query_string = p.sub(r'\1', query_string)
		query_string = query_string.strip()
		query_string = query_string.replace('.', '')
		if not query_string:
			return old_query_string
		return query_string

	def close(self):
		self.s.close()


class LanguageSocketHandler(SocketHandler):

	def send_index_command(self):
		SocketHandler.send_index_command(self)
		self.s.sendall('LanguageSearchEngine\n')

	def send_query_command(self):
		SocketHandler.send_query_command(self)
		self.s.sendall('LanguageSearchEngine\n')

	def send_query(self, query_string, change=True):
		if change:
			query_string = self.clean_query_string(query_string)
		query_string += '\n'
		print query_string
		self.s.sendall(query_string)

		data = self.fid.readline().strip()
		return data

	def clean_query_string(self, query_string):
		p = re.compile(r'([a-zA-Z]+)[\s,\-_](.*)', re.M)
		query_string = p.sub(r'\1', query_string)
		query_string = query_string.strip()

		return query_string

	def close(self):
		self.s.close()


class UniversityLocationSocketHandler(SocketHandler):

	def send_index_command(self):
		SocketHandler.send_index_command(self)
		self.s.sendall('UniversityLocationSearchEngine\n')

	def send_query_command(self):
		SocketHandler.send_query_command(self)
		self.s.sendall('UniversityLocationSearchEngine\n')

	def send_query(self, query_string, change=True):
		if change:
			query_string = self.clean_query_string(query_string)
		query_string += '\n'
		self.s.sendall(query_string)

		data = self.fid.readline().strip()
		if data == 'None':
			return None
		else:
			return data

	def close(self):
		self.s.close()

	def clean_query_string(self, query_string):
		query_string = query_string.replace(',', '')
		return query_string


class UniversitySocketHandler(SocketHandler):

	def send_index_command(self):
		SocketHandler.send_index_command(self)
		self.s.sendall('UniversitySearchEngine\n')

	def send_query_command(self):
		SocketHandler.send_query_command(self)
		self.s.sendall('UniversitySearchEngine\n')

	def send_query(self, query_string):
		print query_string
		query_string += '\n'
		self.s.sendall(query_string)

		data = self.fid.readline().strip()
		return data

	def close(self):
		self.s.close()

	def clean_query_string(self, query_string):
		p = re.compile(r'(.*?)(\(.*\))', re.M)
		query_string = p.sub(r'\1', query_string)
		query_string = query_string.strip()
		return query_string
