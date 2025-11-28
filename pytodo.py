import os
import sys
import datetime
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QPushButton, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QLineEdit, QDialogButtonBox, QMessageBox
from qt_material import apply_stylesheet

# Task Class
class Task:
    def __init__(self, name, due_date, description):
        self.name = name
        self.due_date = due_date
        self.completed = False
        self.description = description

    def change_name(self, new_name):
        self.name = new_name

    def change_due_date(self, new_date):
        self.due_date = new_date

    def change_description(self, new_description):
        self.description = new_description

    def complete(self):
        self.completed = True

tasks = []

# Save Tasks function
def save_tasks():
    path_to_save = os.path.join(os.path.expanduser("~"), "tasks.pkl")
    with open(path_to_save, "wb") as file:
        pickle.dump(tasks, file, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Tasks have been successfully saved to: {path_to_save}")

# Load tasks function
def load_tasks():
    global tasks
    path_to_load = os.path.join(os.path.expanduser("~"), "tasks.pkl")
    try:
        with open(path_to_load, "rb") as file:
            tasks = pickle.load(file)
        print("Tasks have been successfully loaded from tasks.pkl")
    except:
        print("ERROR: No saved file to load (missing tasks.pkl file?)")

# List all tasks function
def view_tasks():
    for i in tasks:
        print(f'{tasks.index(i) + 1}. {i.name}')
        print(f'Due Date: {i.due_date}')
        print(f'Completed: {i.completed}')
        print(f'Description: {i.description}')
        print()

## WINDOWS

class FenetreSecondaire(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fenêtre secondaire")
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ceci est une fenêtre secondaire"))
        self.setLayout(layout)

class AddTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add task")
        self.setGeometry(200, 200, 400, 250)
        
        layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Task Name")
        layout.addWidget(QLabel("Task Name:"))
        layout.addWidget(self.name_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Due-Date")
        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.date_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description")
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.result = None

    def get_task_data(self):
        if self.exec_() == QDialog.Accepted:
            return {
                'name': self.name_input.text(),
                'due_date': self.date_input.text(),
                'description': self.desc_input.text()
            }
        return None

class TaskDetailsWindow(QDialog):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Title: {task.name}"))
        layout.addWidget(QLabel(f"Due Date: {task.due_date}"))
        layout.addWidget(QLabel(f"Description: {task.description}"))
        layout.addWidget(QLabel(f"Completed: {'Yes' if task.completed else 'No'}"))

        self.setLayout(layout)

class FenetrePrincipale(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 500, 500)

        layout = QVBoxLayout()

        # Tasks list
        self.t_list = QListWidget()
        self.refresh_tasks_list()
        self.t_list.itemDoubleClicked.connect(self.open_task_details)
        layout.addWidget(QLabel("Tasks list:"))
        layout.addWidget(self.t_list)

        # Separator
        layout.addSpacing(20)

        # "Mark as Completed" button
        self.mark_completed_button = QPushButton('✔ Mark "Completed"')
        self.mark_completed_button.clicked.connect(self.mark_completed)
        self.mark_completed_button.setStyleSheet("""
            QpushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px
                padding: 8px
                fontweight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        self.mark_completed_button.setFlat(True)
        layout.addWidget(self.mark_completed_button)

        # "Remove task" button
        self.remove_button = QPushButton("🗑️ Remove Selected Task")
        self.remove_button.clicked.connect(self.remove_selected_task)
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #dc3545;
                border: 2px solid #dc3545;
                border-radius: 15px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc3545;
                color: white;
            }
        """)
        self.remove_button.setFlat(True)
        layout.addWidget(self.remove_button)

        layout.addSpacing(20)

        # Buttons
        self.button2 = QPushButton("Add Task")
        self.button2.clicked.connect(self.open_add_task_window)

        self.button3 = QPushButton("Save")
        self.button3.clicked.connect(self.do_save_tasks)

        self.button4 = QPushButton("Quit")
        self.button4.clicked.connect(self.quit)

        buttons_list = [self.button2, self.button3, self.button4]

        for i in buttons_list:
            layout.addWidget(i)

        self.setLayout(layout)
        self.tasks_list = tasks

    # Functions
    def refresh_tasks_list(self):
        self.t_list.clear()
        for i in tasks:
            item = QListWidgetItem(f"{i.name} - Due: {i.due_date}")
            if i.completed:
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
            self.t_list.addItem(item)

    def open_list_tasks_window(self):
        self.list_tasks_window = ListTasksWindow(self)
        self.list_tasks_window.show()

    def open_task_details(self, item):
        row = self.t_list.row(item)
        task = tasks[row]
        dlg = TaskDetailsWindow(task, self)
        dlg.exec_()

    def remove_selected_task(self):
        current_row = self.t_list.currentRow()
        if current_row >=0:
            del tasks[current_row]
            self.refresh_tasks_list()
        else:
            QMessageBox.warning(self, "No selected task", "Please first select a task to remove.")

    def mark_completed(self):
        current_row = self.t_list.currentRow()
        if current_row >=0:
            if not tasks[current_row].completed:
                tasks[current_row].completed = True
            elif tasks[current_row].completed:
                tasks[current_row].completed = False

            self.refresh_tasks_list()
        else:
            QMessageBox.warning(self, "No selected task", "Please select a task first.")
            

    def open_add_task_window(self):
        dialog = AddTaskWindow(self)
        task_data = dialog.get_task_data()
        if task_data:
            new_task = Task(task_data['name'], task_data['due_date'], task_data['description'])
            tasks.append(new_task)
            self.refresh_tasks_list()

    def do_save_tasks(self):
        try:
            save_tasks()
        except:
            print("Error, couldn't save.")

    def quit(self):
        self.close()

load_tasks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec_())
