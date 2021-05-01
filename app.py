from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"mydatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(50),nullable=False)
    expensename = db.Column(db.String(50),nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    category = db.Column(db.String(50),nullable=False)


@app.route('/')
def add():
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/update/<int:id>')
def update(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('update.html',expense=expense)

@app.route('/edit',methods=['POST'])
def edit():
    id = request.form["id"]
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']

    expense = Expense.query.filter_by(id=id).first() 
    expense.date = date
    expense.expensename = expensename
    expense.amount = amount
    expense.category = category

    db.session.commit()
    return redirect('/expenses')

@app.route('/addexpense',methods=['POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']

    expense = Expense(date=date,expensename=expensename,amount=amount,category=category)
    db.session.add(expense)
    db.session.commit()

    return redirect('/expenses')

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()

    return render_template('expenses.html',expenses=expenses)

@app.route('/breakdown')
def breakdown():
    expenses = Expense.query.all()

    total = 0
    household = 0
    food = 0
    entertainment = 0
    business = 0
    other = 0
    for expense in expenses:
        total += expense.amount
        if expense.category == 'household':
            household += expense.amount
        elif expense.category == 'food':
            food += expense.amount
        elif expense.category == 'entertainment':
            entertainment += expense.amount
        elif expense.category == 'business':
            business += expense.amount
        elif expense.category == 'other':
            other += expense.amount

    return render_template('breakdown.html',expenses=expenses,total=total,household=household,food=food,entertainment=entertainment,business=business,other=other)


if __name__ == "__main__":
    app.run(debug = True)
