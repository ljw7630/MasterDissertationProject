import sqlite3


class DBHelper():

	@staticmethod
	def getCursor():
		DBHelper.con = sqlite3.connect('website/website/db/website.db')
		DBHelper.cur = DBHelper.con.cursor()
		return DBHelper.cur

	@staticmethod
	def dataAddEntry(file_name, url, exist):
		try:
			DBHelper.getCursor().execute("insert into survey_data(file_name, file_url, file_exists) values ('%s', '%s', %i)"
				% (file_name, url, int(exist)))
			DBHelper.con.commit()
		except sqlite3.IntegrityError:
			if exist:
				DBHelper.getCursor().execute("update survey-data set file_exists = %i" % int(exist))
				DBHelper.con.commit()
			else:
				raise sqlite3.IntegrityError

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
			DBHelper.con.commit()
			DBHelper.con.close()
		except AttributeError:
			pass