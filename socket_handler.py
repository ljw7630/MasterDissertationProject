import socket
import re

HOST = 'localhost'
PORT = 12345


class DegreeSocketHandler:

	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST, PORT))
		self.fid = self.s.makefile()

	def send_index_command(self):
		self.s.sendall('index\n')

	def send_query_command(self):
		self.s.sendall('query\n')

	def send_query(self, query_string, change=True):
		if change:
			query_string = self.clean_query_string(query_string)
		query_string += '\n'
		print 'query_string', repr(query_string)

		self.s.sendall(query_string)

		# data = self.s.recv(1024)
		data = self.fid.readline()
		print 'data', repr(data)
		data = data.strip().split(',')
		return data[0], data[1]

	def clean_query_string(self, query_string):
		p = re.compile(r'(.*?)(\(.*\))', re.M)
		query_string = p.sub(r'\1', query_string)
		query_string = query_string.strip()
		query_string = query_string.replace('.', '')
		return query_string

	def close(self):
		self.s.close()