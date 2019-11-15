import webapp2
import passwords
import MySQLdb

passwords = passwords.Passwords()

conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST,
			user = passwords.SQL_USER,
			passwd = passwords.SQL_PASSWD,
			db = passwords.SQL_DB)

cursor = conn.cursor()

class NewUserPage(webapp2.RequestHandler):
	def post(self):
		user = self.request.get("user")
		id = self.request.get("id")
		
		self.response.headers['Content-Type'] = 'text/html'

		cursor.execute('UPDATE Sessions SET User = \"' + user + '\" WHERE '
				'SessionID = \"' + id + '\";') 
		conn.commit()

		cursor.execute('SELECT User FROM Users WHERE User=\"' + user + '\";')
		user_check = cursor.fetchall()

		if(len(user_check) == 0):
			cursor.execute('INSERT INTO Users (User, I) VALUES ( \"' + user + '\", 0);')
			conn.commit()	
	
		self.redirect("/")

app = webapp2.WSGIApplication([
	('/new_user', NewUserPage),
], debug=True)
