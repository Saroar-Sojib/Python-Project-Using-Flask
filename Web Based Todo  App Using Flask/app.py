from datetime import datetime
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class Test(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False )
    dsc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route("/", methods=['GET','POST'])

def hello_world():
    if request.method=="POST":
        title=request.form['title']
        dsc=request.form['dsc']
        test=Test(title=title, dsc=dsc)
        db.session.add(test)
        db.session.commit()
   
    allTodo=Test.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        dsc=request.form['dsc']
        todo = Test.query.filter_by(sno=sno).first()
        todo.title=title
        todo.dsc=dsc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')   
    todo = Test.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    

@app.route("/delate/<int:sno>")
def delate(sno):
    todo = Test.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    


if __name__ =="__main__":
    app.run(debug=True)