import sqlite3


class DBHelper():

	@staticmethod
	def getCursor():
		try:
			return DBHelper.cur
		except AttributeError:
			DBHelper.con = sqlite3.connect('website/website/db/website.db')
			DBHelper.cur = DBHelper.con.cursor()
			return DBHelper.cur

	@staticmethod
	def getNotExistFileNames(limit=1000):
		res = DBHelper.getCursor().execute("select file_name from survey_data where file_exists=0 limit=%i" % limit)
		return res.fetchall()

	@staticmethod
	def getNotRDFedFileName(limit=1000):
		res = DBHelper.getCursor().execute("select file_name from survey_data where file_exists=1 and rdf=0 limit=%i" % limit)
		return res.fetchall()

	@staticmethod
	def dataAddEntry(file_name, url, exist, type='PERSON'):
		try:
			print 'statement: ', """insert into survey_data(file_name, file_url, file_exists, type)
					values ('%s', '%s', %i, '%s')""" % (file_name, url, int(exist), type)

			DBHelper.getCursor().execute(
				"""insert into survey_data(file_name, file_url, file_exists, type)
					values ('%s', '%s', %i, '%s')""" % (file_name, url, int(exist), type))
			DBHelper.con.commit()
		except sqlite3.IntegrityError:
			if exist:
				DBHelper.getCursor().execute("update survey_data set file_exists=%i" % int(exist))
				DBHelper.con.commit()
			else:
				raise sqlite3.IntegrityError

	@staticmethod
	def dataSetRDF(file_name):
		DBHelper.getCursor().execute("update survey_data set rdf=1 where file_name=%s" % file_name)

	@staticmethod
	def isDataRDFed(file_name):
		res = DBHelper.getCursor().execute("select count(*) from survey_data where file_name='%s' and rdf=0"
			% file_name)
		count = res.fetchone()[0]
		if count != 0:
			return True
		else:
			return False

	@staticmethod
	def dataInDB(file_name):
		res = DBHelper.getCursor().execute("select count(*) from survey_data where file_name = '%s'" % file_name)
		count = res.fetchone()[0]
		if count != 0:
			return True
		else:
			return False

	@staticmethod
	def commitAndClose():
		try:
			DBHelper.cur.close()
			DBHelper.con.commit()
			DBHelper.con.close()

			del DBHelper.cur
			del DBHelper.con
		except AttributeError:
			pass