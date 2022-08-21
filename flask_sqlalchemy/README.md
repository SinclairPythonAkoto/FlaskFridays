# Flask SQLAlchemy ORM #

We will cover the different ways we can use database relationship models with **one-to-many**, **one-to-one** and **many-to-many** relationships.

For an example, we will pretend we are using a HR system ehivh are usig the following models:
- `Employee`
- `Department`
- `Project`

### One-To-Many ###
 In the example, a **one-to-many** relationship should exist between the `Employee` and the `Departement`. This relationship will indicate that *an employee belongs to only one department. However, a department can contain multiple employees*.

 **basic commands**
 
 - create an department object
 - db add & commit
 - create a emplaoyee object
 - db add & commit
 - department_object.staff
 - department_object.staff.first_name

 eg.
 ```
 sales = Department(name='Sales Team', location='London')
 db.session.add(sales)
 db.session.commit()
 sin = Employee(first_name='Sinclair', last_name='Akoto', department=sales)
 db.session.add(sin)
 db.session.commit()

 sales                  # <Department Sales Team>
 sales.name             # 'Sales Team'
 sin.department         # <Department Sales Team>
 sin.department.name    # 'Sales Team'
 ```

 We can create more employees for the `Sales Team` and other departments.
 ```
 jane = Epmplyee(first_name='Jane', last_name='Doe', department=sales)
 db.session.add(jane)
 db.session.commit()

 john = Employee(first_name='John', last_name='Doe', department=sales)
 db.session.add(john)
 db.session.commit()
 ```