import datetime
from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_login import login_required, logout_user, LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database, get_relationship_names
from database.models import UserRoleEnum, User, Task, Project, Subtask, Notif, NotifTypeEnum, NotifStatusEnum, Category, PriorityEnum, TaskCompletionEnum
import database.models as models
import os
from helpers import enum_to_readable
from sqlalchemy import inspect


reset_database = True


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "this-is-a-secret-key"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
db.init_app(app)
if reset_database:
    with app.test_request_context():
        init_database()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    return models.User.query.filter_by(username=user).first()


@app.route('/')
@login_required
def route():
    return redirect('/home_page')


task_order_date = False


# HOME PAGE
@app.route('/home_page', methods=['POST', 'GET'])
@login_required
def dashboard():
    global task_order_date
    return render_template("home_page.html.jinja2", users=User.query.all(), tasks=Task.query.all(),
                           taskOrderDate=task_order_date)


# HOME PAGE
@app.route('/update_dash_board', methods=['POST'])
@login_required
def update_dash_board():
    global task_order_date
    # Obtenir les données envoyées depuis la requête AJAX
    input_search_bar = request.form['input_search_bar']
    input_select_project = request.form['input_select_project']
    input_select_status = request.form['input_select_status']
    input_select_priority = request.form['input_select_priority']
    input_select_date_order = request.form['input_select_date_order']

    # Trier les tâches en fonction de la valeur sélectionnée dans le menu déroulant DateSelect
    if input_select_date_order == 'AscendingDate':
        task_order_date = False
    elif input_select_date_order == 'DescendingDate':
        task_order_date = True

    # Mettre à jour les tâches filtrées
    update_filtered_tasks(input_search_bar, input_select_project, input_select_status, input_select_priority,
                          input_select_date_order)

    db.session.commit()

    return jsonify({'success': 'we correctly receive data'}), 200


def update_filtered_tasks(input_search_bar, input_select_project, input_select_status, input_select_priority,
                          input_select_date_order):
    all_tasks = Task.query.all()

    # Parcourir toutes les tâches et mettre à jour l'attribut displayable
    for task in all_tasks:

        # Mettre à jour displayable si les critères de filtrage sont satisfaits
        if (input_search_bar.lower() in task.name.lower() or input_search_bar == '') and \
                (input_select_project == 'Filtre par projet' or str(input_select_project) == str(task.project_id)) and \
                (input_select_status == 'Filtre par statut' or input_select_status == task.completionStatus.value) and \
                (input_select_priority == 'Filtre par priorité' or input_select_priority == task.label.value):
            task.displayable = True
        else:
            task.displayable = False


# HOME PAGE
# Route for retrieving projects
@app.route('/projects', methods=['GET'])
@login_required
def get_projects():
    projects = Project.query.all()
    project_data = []
    for project in projects:
        members_id = [user.id for user in project.users]
        members = []
        for member_id in members_id:
            members.append(User.query.get(member_id).username)
        project_data.append({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'color': project.color,
            'endDate': project.endDate,
            'startDate': project.startDate,
            'members': members
        })
    return jsonify(project_data)


def retrieve_data():
    name = request.form['name']
    description = request.form['description']
    color = request.form['color']
    start_date = datetime.date.today()
    end_date = datetime.date(2024, 12, 30)

    if request.form['startDate']:
        start_date_str = request.form['startDate']
        start_year, start_month, start_day = map(int, start_date_str.split('-'))
        start_date = datetime.date(start_year, start_month,
                                   start_day)  # Transforme les dates de javascript en date utilisable par Python
    if request.form['endDate']:
        end_date_str = request.form['endDate']
        end_year, end_month, end_day = map(int, end_date_str.split('-'))
        end_date = datetime.date(end_year, end_month, end_day)

    project_members = request.form.getlist('members[]')  # Récupère une liste des membres du projet

    return name, description, color, start_date, end_date, project_members


# HOME PAGE
@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    name, description, color, start_date, end_date, members = retrieve_data()
    existing_project = Project.query.filter_by(name=name).first()
    if existing_project:
        return jsonify({'error': 'A project with the same name already exists'}), 400

    # Création d'un projet et ajout à la base de données
    project = Project(description=description, name=name, color=color, startDate=start_date, endDate=end_date)
    db.session.add(project)
    # Ajout des membres au projet
    if members:
        for member_name in members:
            member = User.query.filter_by(username=member_name).first()
            if member:
                project.users.append(member)
    else:
        project.users.append(current_user)

    db.session.commit()

    project_created = Project.query.order_by(Project.id.desc()).first()
    for member in project_created.users:
        notif = Notif(project_id=project_created.id,
                      type=NotifTypeEnum.ASSIGNED,
                      datetime=datetime.datetime.now(),
                      status=NotifStatusEnum.NOTREAD,
                      user=member.id)
        db.session.add(notif)
    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 200


# HOME PAGE
@app.route('/delete_project', methods=['POST'])
@login_required
def delete_project():
    id_project = request.form['id']
    project = Project.query.filter_by(id=id_project).first()
    if project:
        db.session.delete(project)
        db.session.commit()  # Confirmer la suppression
        return jsonify({'message': 'Project deleted successfully'}), 200
    else:
        return jsonify({'error': 'Project not found'}), 404


# HOME PAGE
@app.route('/save_project', methods=['POST'])
@login_required
def save_project():
    print("\n==== SAVING PROJECT ====\n")
    name, description, color, start_date, end_date, members = retrieve_data()

    # Rechercher le projet existant dans la base de données
    existing_project = Project.query.filter_by(name=name).first()
    if existing_project:
        # Mettre à jour les champs du projet avec les nouvelles valeurs
        existing_project.description = description
        existing_project.color = color
        existing_project.startDate = start_date
        existing_project.endDate = end_date
        print("    Current Project : " + str(existing_project))
        print("        Description : " + description)
        print("        Color : " + str(color))
        print("        Start Date : " + str(start_date))
        print("        End Date : " + str(end_date))
        print("        Members : " + str(members))

        # Supprimer les membres actuels du projet
        for member in existing_project.users:
            if member.username not in members:
                existing_project.users.remove(member)
                notif = Notif(project_id=existing_project.id,
                              type=NotifTypeEnum.UNASSIGNED,
                              datetime=datetime.datetime.now(),
                              status=NotifStatusEnum.NOTREAD,
                              user=member.id)
                db.session.add(notif)
            else:
                notif = Notif(project_id=existing_project.id,
                              type=NotifTypeEnum.MODIFIED,
                              datetime=datetime.datetime.now(),
                              status=NotifStatusEnum.NOTREAD,
                              user=member.id)
                db.session.add(notif)
        print("\n    Deleted previous members from project")

        # Ajouter les nouveaux membres au projet
        print("    Adding new members :")
        for member_name in members:
            member = User.query.filter_by(username=member_name).first()
            if member and member not in existing_project.users:
                existing_project.users.append(member)
                print("        Added user " + member.username)
                notif = Notif(project_id=existing_project.id,
                              type=NotifTypeEnum.ASSIGNED,
                              datetime=datetime.datetime.now(),
                              status=NotifStatusEnum.NOTREAD,
                              user=member.id)
                db.session.add(notif)

        # Sauvegarder les modifications dans la base de données
        db.session.commit()

        return jsonify({'message': 'Project updated successfully'}), 200
    else:
        return jsonify({'error': 'Project not found'}), 404


# PROJECT PAGES
@login_required
@app.route('/projects/standard_view/<int:project_id>', methods=['GET', 'POST'])
def standard_project_page(project_id):
    project = Project.query.get(project_id)
    users = project.users  # Récupérer les utilisateurs associés à ce projet
    print(project.id)
    return render_template("project_standard_view.html.jinja2", project=project, users=users)


# PROJECT PAGES
# Route for creating categories
@app.route('/create_category', methods=['POST'])
@login_required
def create_category():
    name = request.form['category_name']
    project_id = request.form['project_id']
    # Ici on crée la categorie
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({'error': 'A category with the same name already exists'}), 400

    category = Category(name=name, project_id=project_id)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully'}), 200


@login_required
@app.route('/create_task', methods=['POST'])
def create_task():
    name = request.form.get('name')
    description = request.form.get('description')
    due_date = datetime.date(2024, 12, 30)
    if request.form['dueDate']:
        due_date_str = request.form['dueDate']
        due_year, due_month, due_day = map(int, due_date_str.split('-'))
        due_date = datetime.date(due_year, due_month,
                                 due_day)
    label = request.form.get('priority')
    status = request.form.get('status')
    users = request.form.getlist('users[]')
    category_id = request.form.get('categoryId')
    label_enum = get_priority_enum_from_value(label)
    status_enum = get_completion_enum_from_value(status)

    task = Task(name=name, description=description, dueDate=due_date, label=label_enum, completionStatus=status_enum, category_id=category_id)

    current_category = Category.query.get(category_id)
    current_category.tasks.append(task)
    db.session.add(task)
    db.session.commit()
    for username in users:
        user = User.query.filter_by(username=username).first()
        task.users.append(user)
    db.session.commit()
    return jsonify({'success': True})


@login_required
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_data = []
    for task in tasks:
        task_users = [user.username for user in task.users]
        task_details = {
            'id': task.id,
            'name': task.name,
            'category_id': task.category_id,
            'label': task.label.value,
            'description': task.description,
            'dueDate': task.dueDate.strftime('%Y-%m-%d') if task.dueDate else None,
            'displayable': task.displayable,
            'completionStatus': task.completionStatus.value,
            'users': task_users
        }
        task_data.append(task_details)
    return jsonify(task_data), 200


# PROJECT PAGE
@login_required
@app.route('/modify_task', methods=['POST'])
def modify_task():
    id = request.form.get('idTask')
    name = request.form.get('name')
    description = request.form.get('description')
    due_date = datetime.date(2024, 12, 30)
    if request.form['dueDate']:
        due_date_str = request.form['dueDate']
        due_year, due_month, due_day = map(int, due_date_str.split('-'))
        due_date = datetime.date(due_year, due_month,
                                 due_day)
    priority = request.form.get('priority')
    status = request.form.get('status')
    usernames = request.form.getlist('users[]')

    task = Task.query.get(id)
    task.name = name
    task.description = description
    task.dueDate = due_date
    task.priority = get_priority_enum_from_value(priority)
    task.status = get_completion_enum_from_value(status)

    users = []
    for username in usernames:
        user = User.query.filter_by(username=username).first()
        users.append(user)
    task.users = users
    db.session.commit()
    return jsonify({'success': True})


# PROJECT PAGE

@app.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    print("Nous voulons delete")
    id_task = request.form['id']
    task = Task.query.filter_by(id=id_task).first()
    if task:
        db.session.delete(task)
        db.session.commit()  # Confirmer la suppression
        return jsonify({'message': 'Project deleted successfully'}), 200
    else:
        return jsonify({'error': 'Project not found'}), 404


@login_required
@app.route('/current_user', methods=['GET'])
def get_current_user():
    user_projects = current_user.get_project()
    projects_data = [{"id": project.id, "name": project.name} for project in user_projects]
    if current_user.is_authenticated:
        user_details = {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role.value,
            "projects": projects_data
        }
        return jsonify(user_details)
    else:
        return jsonify({"error": "No users are currently logged in"}), 401


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("==== LOGIN PAGE ====\n")
    users = User.query.all()
    print("    Users in the database :")
    for user in users:
        print("         ID: {:<3}  | Username: {:<15}  | Password: {:<100}".format(user.id, user.username,
                                                                                   user.password_hash))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = models.User.query.filter_by(username=username).first()
        print("Username : ", username)
        print("Remember : ", remember)
        print(check_password_hash(user.password_hash, password))
        print(generate_password_hash(password))
        print(user.password_hash)
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return render_template('login.html.jinja2')
        login_user(user, remember=remember)
        return redirect('/home_page')
    else:
        return render_template('login.html.jinja2')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        user = models.User.query.filter_by(username=username).first()
        if user:
            flash('User already exists')
        elif not username or not password or not role:
            flash('Please fill in all the fields')
        else:
            user = User(username=username,
                        password_hash=generate_password_hash(password, method='sha256'),
                        role=role)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    user_roles_enums = [role.name for role in UserRoleEnum]
    user_roles = [enum_to_readable(role.name) for role in UserRoleEnum]
    return render_template('register.html.jinja2',
                           user_roles_enums=user_roles_enums,
                           user_roles=user_roles,
                           zip=zip)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/notifs', methods=['GET'])
@login_required
def get_notifs():
    notifs = Notif.query.all()
    notif_data = []
    for notif in notifs:
        member = User.query.get(notif.user).username
        project = Project.query.get(notif.project_id)
        datetime_str = notif.datetime.strftime("%Y-%m-%d %H:%M:%S").split(" ")
        date = "/".join(datetime_str[0].split("-")[::-1][:2])
        time = datetime_str[1][:5]
        notif_data.append({
            'id': notif.id,
            'project_id': project.id,
            'project_name': project.name,
            'color': project.color,
            'type': notif.type.value,
            'date': date,
            'time': time,
            'status': notif.status.value,
            'user': member
        })
        if notif.task_id:
            task = Task.query.get(notif.task_id)
            notif_data[0]['task'] = task.name
    return jsonify(notif_data)


@app.route('/delete_notif', methods=['POST'])
@login_required
def delete_notif():
    id_notif = request.form['id_notif']
    notif = Notif.query.get(id_notif)
    if notif:
        db.session.delete(notif)
        db.session.commit()  # Confirmer la suppression
        return jsonify({'message': 'Notif deleted successfully'}), 200
    else:
        return jsonify({'error': 'Notif not found'}), 404


@app.route('/set_notif', methods=['POST'])
@login_required
def change_status_notif():
    id_notif = request.form['id_notif']
    notif = Notif.query.get(id_notif)
    if notif:
        if notif.status.value:
            notif.status = NotifStatusEnum.NOTREAD
        else:
            notif.status = NotifStatusEnum.READ
        db.session.commit()  # Confirmer
        return jsonify({'message': 'Notif status changed successfully'}), 200
    else:
        return jsonify({'error': 'Notif not found'}), 404


@app.route('/database')
def show_database():
    print("\n==== SHOWING THE DATABASE ====\n")
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    tables = [table for table in tables if not is_junction_table(table)]
    columns_dict = {}
    for table in tables:
        columns = inspector.get_columns(table)
        columns_dict[table] = [column['name'] for column in columns]
    data = {}
    print("    Structure :")
    print("        Tables : ", tables)
    print("        Columns : ")
    for table, columns in columns_dict.items():
        print("            " + table + " : " + str(columns))
    print("\n    Data :")
    for table in tables:
        print("        " + table.capitalize() + " :")
        model_class = globals()[table.capitalize()]
        data[table] = model_class.query.all()
        print("            Instances :" + str(data[table]))

        relationships = get_relationship_names(model_class)
        if not relationships:
            continue
        print("            Relationships with classes :", get_relationship_names(model_class))

        for instance in data[table]:
            print("            Instance :", instance)
            for relationship in relationships:
                print("                Linked with instances of class " + relationship, end="")
                linked_objects = getattr(instance, relationship)
                if hasattr(linked_objects, "__iter__"):
                    linked_ids = [linked_object.id for linked_object in linked_objects]
                else:
                    linked_ids = [linked_objects.id]
                print(" with ids : " + str(linked_ids))

    return render_template('database.html.jinja2', columns=columns_dict, data=data, getattr=getattr)


def is_junction_table(table_name):
    inspector = inspect(db.engine)
    foreign_keys = inspector.get_foreign_keys(table_name)
    columns = inspector.get_columns(table_name)
    return len(foreign_keys) == 2 and len(columns) == 2


def get_priority_enum_from_value(string):
    for priority in PriorityEnum:
        if priority.value == string:
            return priority


def get_completion_enum_from_value(string):
    for completion in TaskCompletionEnum:
        if completion.value == string:
            return completion

if __name__ == '__main__':
    app.run()
