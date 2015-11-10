from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'Secret'

mysql = MySQLConnector('full_friendsdb')
friends = mysql.fetch("SELECT * FROM friends")
def find_friend(id):
	for friend in friends:
		if friend['id'] == int(id):
			return friend
	return False

@app.route('/', methods=['GET'])
def index():
	friends = mysql.fetch("SELECT * FROM friends")
	return render_template('index.html', friends=friends)

@app.route('/friends', methods=['POST'])
def create():
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['occupation'])
	print query
	mysql.run_mysql_query(query)
	return redirect('/')


@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
	print id
	friend = find_friend(id)
	if friend:
		return render_template('edit.html', friend=friend, id = id)
	return redirect('/friends/<id>')
	

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	query = "UPDATE `full_friendsdb`.`friends` SET `first_name`='{}', `last_name`='{}', `occupation` = '{}' WHERE `id`='{}'".format(request.form['first_name'], request.form['last_name'], request.form['occupation'], id)
	mysql.run_mysql_query(query)
	return redirect('/')

	
@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
	print "KATE"
	friend = find_friend(id)
	if friend:
		query = "DELETE FROM friends WHERE id = '{}'".format(id)
		mysql.run_mysql_query(query)
	return redirect('/')

app.run(debug=True)


