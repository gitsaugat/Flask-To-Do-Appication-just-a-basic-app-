from flask import Flask 
from flask import render_template
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
from flask import request 
from flask import redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
class Todo(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	work = db.Column(db.String(200) , nullable = False)
	date = db.Column(db.DateTime , default = datetime.utcnow)

	def __repr__(slef):
		return 'Work - %r' %str(self.id)



@app.route('/' , methods = ['GET' , 'POST'])
@app.route('/home' ,  methods = ['GET' , 'POST'])
def home():
	todo = Todo.query.all()
	if request.method == 'POST':
		newwork = request.form['work']
		new = Todo(work = newwork)
		db.session.add(new)
		db.session.commit()
		
		return redirect('/')

	return render_template('home.html' , title = 'Home' , works = todo)
@app.route('/work/delete/<int:id>')
def delete(id):
	work = Todo.query.get_or_404(id)
	db.session.delete(work)
	db.session.commit()
	return redirect('/')
@app.route('/work/update/<int:id>' , methods = ['GET' , 'POST'])
def update(id):
	work = Todo.query.get_or_404(id)
	if request.method == 'POST':
		work.work = request.form['work']
		db.session.commit()
		return redirect('/')

	return render_template('edit.html' , title = 'Edit %r' %str(id) , work = work)

if __name__ == '__main__':
	app.run(debug = True)
