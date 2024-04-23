from tkinter import messagebox
from .Wrapper import database_wrapper, modify_database_wrapper


# creating tables
@modify_database_wrapper
def create_database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
    (id INTEGER PRIMARY KEY, title TEXT, state INTEGER, task_type INTEGER, id_mark INTEGER, archived BOOLEAN)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS marks
    (id INTEGER PRIMARY KEY, mark TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS classicals (id INTEGER PRIMARY KEY, id_task INTEGER, 
    description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS checklists
    (id INTEGER PRIMARY KEY, id_task INTEGER, is_checked BOOLEAN, description TEXT)''')


# tasks table
@modify_database_wrapper
def create_classical_task(cursor, title, state, task_type, mark, description):
    id_mark = get_mark_id_from_name(mark)
    if id_mark is None:
        id_mark = ['']
    cursor.execute("INSERT INTO tasks (title, state, task_type, id_mark, archived) VALUES(?, ?, ?, ?, "
                   "False)",
                   (title, state, task_type, id_mark[0],))

    # Filling the classicals table
    cursor.execute("SELECT id FROM tasks ORDER BY id DESC LIMIT 1")
    id_task = cursor.fetchone()
    cursor.execute("INSERT INTO classicals (id_task, description) VALUES(?, ?)", (id_task[0], description,))


@modify_database_wrapper
def create_checklist_task(cursor, title, state, task_type, mark, micro_tasks_dict):
    id_mark = get_mark_id_from_name(mark)
    if id_mark is None:
        id_mark = ['']
    cursor.execute("INSERT INTO tasks (title, state, task_type, id_mark, archived) VALUES(?, ?, ?, ?, "
                   "False)",
                   (title, state, task_type, id_mark[0],))

    # Filling the checklists table
    cursor.execute("SELECT id FROM tasks ORDER BY id DESC LIMIT 1")
    id_task = cursor.fetchone()
    for i in range(0, len(micro_tasks_dict)):
        cursor.execute("INSERT INTO checklists (id_task, is_checked, description) VALUES(?, ?, ?)",
                       (id_task[0], micro_tasks_dict[i][0], micro_tasks_dict[i][1]))


@modify_database_wrapper
def modify_classical_task(cursor, id_task, title, state, task_type, mark, description):
    id_mark = get_mark_id_from_name(mark)
    if id_mark is None:
        id_mark = ['']
    cursor.execute("UPDATE tasks SET title = ?, state = ?, task_type = ?, id_mark = ? WHERE id = ?",
                   (title, state, task_type, id_mark[0], id_task,))
    cursor.execute("UPDATE classicals SET description = ? WHERE id_task = ?", (description, id_task,))
    cursor.execute("DELETE FROM checklists WHERE id_task = ?", (id_task,))


@modify_database_wrapper
def modify_checklist_task(cursor, id_task, title, state, task_type, mark, micro_tasks_dict):
    id_mark = get_mark_id_from_name(mark)
    if id_mark is None:
        id_mark = ['']
    cursor.execute("UPDATE tasks SET title = ?, state = ?, task_type = ?, id_mark = ? WHERE id = ?",
                   (title, state, task_type, id_mark[0], id_task,))
    cursor.execute("SELECT COUNT(*) FROM checklists WHERE id_task = ?", (id_task,))
    counter = cursor.fetchone()
    for i in range(0, counter[0]):
        cursor.execute("UPDATE checklists SET is_checked = ?, description = ? WHERE id_task = ?",
                       (micro_tasks_dict(i)(0), micro_tasks_dict(i)(1), id_task,))
    cursor.execute("DELETE FROM classicals WHERE id_task = ?", (id_task,))
    cursor.execute("SELECT id FROM checklists WHERE id_task = ?", (id_task,))
    ids = cursor.fetchall()

    for element in ids:
        checkpoint = False
        for i in range(0, micro_tasks_dict.length()):
            if element == micro_tasks_dict(i):
                checkpoint = True
        if not checkpoint:
            cursor.execute("DELETE FROM checklists WHERE id = ?", (element,))


@database_wrapper
def get_all_checklists_of_task(cursor, id_task):
    cursor.execute("SELECT * FROM checklists WHERE id_task = ?", (id_task,))
    checklists = cursor.fetchall()
    return checklists


@modify_database_wrapper
def delete_task_from_id(cursor, id_task):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id_task,))
    cursor.execute("DELETE FROM classicals WHERE id_task = ?", (id_task,))
    cursor.execute("DELETE FROM checklists WHERE id_task = ?", (id_task,))


@database_wrapper
def get_all_tasks(cursor, states, mark):
    if mark == "nothing":
        req = "SELECT * FROM tasks WHERE archived = False AND ("
    else:
        req = "SELECT * FROM tasks JOIN marks ON id_mark = marks.id WHERE marks.mark LIKE '" + mark + '%' + "' AND ("
    counter = 1
    for id_state in states:
        req = req + "state = " + str(id_state)
        if counter < len(states):
            req = req + " OR "
        else:
            req = req + ") AND archived = False ORDER BY state"
        counter += 1
    cursor.execute(req)
    tasks = cursor.fetchall()
    return tasks


@database_wrapper
def get_global_task_details_from_id(cursor, id_task):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id_task,))
    task = cursor.fetchone()
    return task


@database_wrapper
def get_classical_task_details_from_id(cursor, id_task):
    cursor.execute("SELECT * FROM classicals WHERE id_task = ?", (id_task,))
    task = cursor.fetchone()
    return task


@database_wrapper
def get_checklist_task_details_from_id(cursor, id_task):
    cursor.execute("SELECT is_checked, description FROM checklists WHERE id_task = ?", (id_task,))
    task = cursor.fetchall()
    print(task)
    return task


@database_wrapper
def get_number_from_state(cursor, state, mark=None):
    if mark is None:
        cursor.execute("SELECT COUNT(*) AS number FROM tasks WHERE state =? AND archived = False", (state,))
    else:
        cursor.execute("SELECT COUNT(*) AS number FROM tasks JOIN marks ON marks.id = tasks.id_mark WHERE state =? "
                       "AND marks.mark =? AND archived = False", (state, mark,))
    number = cursor.fetchone()
    return number


@database_wrapper
def get_checklist_task_from_id_task(cursor, id_task):
    cursor.execute("SELECT * FROM checklists WHERE id_task = ?", (id_task,))
    checklist_tasks = cursor.fetchall()
    return checklist_tasks


# marks table
@modify_database_wrapper
def add_mark(cursor, mark):
    if cursor.execute("SELECT mark FROM marks WHERE mark = ?", (mark,)).fetchone() is not None:
        messagebox.showinfo("Attention", "Cette étiquette existe déjà.")
    else:
        cursor.execute("INSERT INTO marks (mark) VALUES(?)", (mark,))


@modify_database_wrapper
def delete_mark_from_id(cursor, id_mark):
    cursor.execute("DELETE FROM marks WHERE id = ?", (id_mark,))


@database_wrapper
def get_mark_id_from_name(cursor, mark):
    cursor.execute(
        "SELECT marks.id FROM marks WHERE marks.mark = ?", (mark,))
    id_task = cursor.fetchone()
    return id_task


@database_wrapper
def get_mark_from_id(cursor, id_mark):
    cursor.execute("SELECT mark FROM marks WHERE marks.id = ?", (id_mark,))
    mark = cursor.fetchone()
    return mark


@database_wrapper
def get_all_marks(cursor):
    cursor.execute("SELECT * FROM marks")
    marks = cursor.fetchall()
    return marks


@modify_database_wrapper
def archive_task(cursor, id_task):
    cursor.execute("UPDATE tasks SET archived = True WHERE id = ?", (id_task,))


@modify_database_wrapper
def unarchive_task(cursor, id_task):
    cursor.execute("UPDATE tasks SET archived = False WHERE id = ?", (id_task,))


@database_wrapper
def get_all_archived_tasks(cursor):
    cursor.execute("SELECT * FROM tasks WHERE archived = True")
    tasks = cursor.fetchall()
    return tasks


@database_wrapper
def download_database(cursor):
    with open('../data/saves/Sauvegarde BDD.txt', 'w') as file:
        cursor.execute('SELECT * FROM tasks')
        data = cursor.fetchall()
        file.write('TASKS' + '\n')
        for row in data:
            if ','.join(map(str, row)) != '\n':
                file.write(','.join(map(str, row)) + '\n')
        cursor.execute('SELECT * FROM marks')
        data = cursor.fetchall()
        file.write('\nMARKS' + '\n')
        for row in data:
            file.write(','.join(map(str, row)) + '\n')

        cursor.execute('SELECT * FROM checklists')
        data = cursor.fetchall()
        file.write('\nCHECKLISTS' + '\n')
        for row in data:
            file.write(','.join(map(str, row)) + '\n')
