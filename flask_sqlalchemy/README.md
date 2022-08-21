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
 - employee_name.department
 - employee_name.department.name

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

 ### One-To-One ###
A **one-to-one** relationship should exist between the `Employee` and `Department`. This relationship will indicate that an employee can be the head of a department (only one at a time).

The steps are similar to creating *One-To-Many* relationships, execpt that we add an additional parameter called `uselist` when creating a ForeignKey & relationship between the models.

We need to make sure that there is only one employee being the head of a department at one time.  So `uselist` is used to make sure that the relationship between the two will **not** be with more than one `employee`.  We set `uselist` to `False` to prevent the relationship pointing to a list.


### Many-To-Many ###
A **many-to-many** relationship should exist between the `Employee` and the `Project`. This relationship will indicate that an employee can work on multiple projects while a project can have multiple employees working on it at the same time.

We will craete an *association table* that will have the **ForeignKeys** of the models that we want to connect together.  ***(Notice how we create a db table not model).***  Then we only need to add the relationship to just one of the models (ie `Project` or `Employee`).

We will create a `relationship()` called `members` in the `Project` model. This relationship is made with the `Employee` model - we will use an *association table* to create it. Therefore, we will to need set the `secondary` parameter equal to the table `project_members`. Finally, we will create a `backref` in this relationship so that we can access this project from the `Employee` table. We will name this backref `projects`. This means that `employee.projects` will give us all the projects that this employee is working on.