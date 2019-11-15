import webapp2
import passwords
import MySQLdb
import random

passwords = passwords.Passwords()

conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST,
			user = passwords.SQL_USER,
			passwd = passwords.SQL_PASSWD,
			db = passwords.SQL_DB)

cursor = conn.cursor()

def user_form(session_id):
	html = '<form action="new_user" method="POST">'
	html += '<p>User:'
	html +=	'<br><input type="text" name="user">'
	html += '</p>'
	html += '<input type="hidden" name="id" value=\"' + session_id + '\">'  
	html += '<input type="submit">'
	html += '</p></form>'
	return html

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('<html>')

		cursor.execute('SELECT * FROM Sessions;')
		results = cursor.fetchall()
		cookie = self.request.cookies.get("cookie_name")

		if(cookie == None):
			session_id = "%015x" % random.getrandbits(60)
			self.response.set_cookie("cookie_name", session_id, max_age=1800)
			cursor.execute('INSERT into Sessions (SessionID) VALUES (' + "\'" + session_id + "\');") 
			conn.commit()		
			cookie = session_id

		cursor.execute('SELECT user FROM Sessions WHERE SessionID=\"' + cookie + '\";')
		results = cursor.fetchall()
		
		user = results[0][0]

		if(user == None):
			self.response.write(user_form(cookie))

		else:
			self.response.write(user)
			cursor.execute('SELECT I FROM Users WHERE user=\"' + user + '\";')
			i = cursor.fetchall()[0][0]
			self.response.write("<p>Increment: " + str(i) + "</p>")
		
			self.response.write('<form action="/increment" method="post" id="inc">'
						'<input type="hidden" name="user" value=\"' + user + '\">' 
						'</form>'
						'<button type="submit" form="inc" value="Submit">Submit</button>')

		self.response.write('</html>')
		
app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
