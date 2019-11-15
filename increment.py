import webapp2
import passwords
import MySQLdb

passwords = passwords.Passwords()

conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST,
			user = passwords.SQL_USER,
			passwd = passwords.SQL_PASSWD,
			db = passwords.SQL_DB)

cursor = conn.cursor()

class IncrementPage(webapp2.RequestHandler):
	def post(self):
		user = self.request.get("user")
		
		self.response.headers['Content-Type'] = 'text/html'

		cursor.execute('UPDATE Users SET I = I + 1 WHERE '
				'User = \"' + user + '\";') 
		conn.commit()
		self.redirect("/")

app = webapp2.WSGIApplication([
	('/increment', IncrementPage),
], debug=True)
