from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route("/show")
def index():
    employees = Employee.query.all()
    return jsonify([{
        'id': employee.id,
        'name': employee.name,
        'salary': employee.salary,
        'email': employee.email
    } for employee in employees])

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get('name')
    salary = data.get('salary')
    email = data.get('email')
    new_employee = Employee(name=name, salary=salary, email=email)
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'salary': new_employee.salary, 'email': new_employee.email})

@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    employee.name = data.get('name')
    employee.salary = data.get('salary')
    employee.email = data.get('email')
    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'salary': employee.salary, 'email': employee.email})

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

@app.route("/change/<int:id>", methods=["PATCH"])
def change(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()

    if(data.get('name')):
        employee.name = data.get('name')
    if(data.get('salary')):
        employee.salary = data.get('salary')
    if(data.get('email')):
        employee.email = data.get('email')

    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'salary': employee.salary, 'email': employee.email})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
