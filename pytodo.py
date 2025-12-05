import os
import sys
from datetime import datetime
import pickle
from operator import attrgetter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QLineEdit, QDialogButtonBox, QMessageBox, QTextEdit
from qt_material import apply_stylesheet

# "Task" Class
class Task:
    def __init__(self, name, due_date_str, description):
        self.name = name
        self.completed = False
        self.description = description

        if not due_date_str or not due_date_str.strip():
            raise ValueError("You must set a due date!")

        try:
            self.due_date = datetime.strptime(due_date_str, "%m-%d-%Y").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format! Use MM-DD-YYYY")

    def __str__(self):
        return f"{self.name} - Due: {self.due_date.strftime('%m-%d-%Y')}"

    def change_name(self, new_name):
        self.name = new_name

    def change_due_date(self, new_date):
        self.due_date = new_date

    def change_description(self, new_description):
        self.description = new_description

    def complete(self):
        self.completed = True

tasks = []

## Functions

# Save Tasks function
def save_tasks():
    path_to_save = os.path.join(os.path.expanduser("~"), "tasks.pkl")
    with open(path_to_save, "wb") as file:
        pickle.dump(tasks, file, protocol=pickle.HIGHEST_PROTOCOL)

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

## Windows

class AddTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add task")
        self.setGeometry(200, 200, 400, 250)
        
        layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Task Name or Title (ex: 'Buy a book')")
        layout.addWidget(QLabel("Task Name:"))
        layout.addWidget(self.name_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Ex: 01-31-2026")
        layout.addWidget(QLabel("Due Date (MM-DD-YYYY):"))
        self.date_input.textChanged.connect(self.validate_date)
        layout.addWidget(self.date_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description details")
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.result = None

    def validate_date(self):
        date_text = self.date_input.text()

        if not date_text:
            self.date_input.setStyleSheet("")
            return
            
        try:
            datetime.strptime(date_text, "%m-%d-%Y")
            self.date_input.setStyleSheet("QLineEdit { border: 2px solid green; }")
        except ValueError:
            self.date_input.setStyleSheet("QLineEdit { border: 2px solid red; }")

    def validate_and_accept(self):
        date_text = self.date_input.text().strip()
        
        if not date_text:
            QMessageBox.warning(self, "Error: due date is mandatory!")
            self.date_input.setFocus()
            return

        try:
            datetime.strptime(date_text, "%m-%d-%Y")
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Invalid Date format!\nUse MM-DD-YYYY")
            self.date_input.selectAll()
            self.date_input.setFocus()

    def get_task_data(self):
        if self.exec_() == QDialog.Accepted:
            return {
                'name': self.name_input.text().strip(),
                'due_date': self.date_input.text().strip(),
                'description': self.desc_input.text().strip()
            }
        return None

class TaskDetailsWindow(QDialog):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle(f"Details: {task.name}")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<b>{task.name}</b>"))
        status = "✅ Completed" if task.completed else "⏳ In Progress"
        layout.addWidget(QLabel(f"Status: {status}"))
        layout.addWidget(QLabel(f"Due by: {task.due_date.strftime('%m-%d-%Y')}"))

        layout.addWidget(QLabel(f"Description:"))
        desc = QTextEdit()
        desc.setPlainText(task.description or "No description")
        desc.setReadOnly(True)
        layout.addWidget(desc)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

class FenetrePrincipale(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(200, 200, 500, 800)

        layout = QVBoxLayout()

        # Tasks list

        self.tasks_title = QLabel("TASK LIST")
        self.tasks_title.setAlignment(Qt.AlignCenter)
        self.tasks_title.setStyleSheet("""
        QLabel {
        color: #ecf0f1;
        font-family: 'Segoe UI';
        font-size: 22px; 
        letter-spacing: 0.5px;
        padding: 14px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2c3e50, stop:1 #34495e);
        border: 2px solid #3498db;
        border-radius: 10px;
        margin: 6px 0 12px 0;
        width: 100%;
        }
        """)

        self.t_list = QListWidget()
        self.refresh_tasks_list()

        self.t_list.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 8px;
                font-family: 'Consolas';
                font-size 13px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #1a252f;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.t_list.setWordWrap(False)

        self.t_list.itemDoubleClicked.connect(self.open_task_details)
        layout.addWidget(self.tasks_title)
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

        # "Add Task" button
        self.add_task_button = QPushButton('➕ Add Task')
        self.add_task_button.clicked.connect(self.open_add_task_window)
        self.add_task_button.setStyleSheet("""
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

        # "Save" button
        self.save_button = QPushButton('💾 Save Tasks')
        self.save_button.clicked.connect(self.do_save_tasks)
        self.save_button.setStyleSheet("""
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

        # Buttons List to add/activate
        buttons_list = [self.add_task_button, self.mark_completed_button, self.save_button, self.remove_button]
        for i in buttons_list:
            i.setFlat(True)
            layout.addWidget(i)

        layout.addSpacing(20)

        # Quit Button
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit)
        layout.addWidget(self.quit_button)

        # Set Tasks list and layout
        self.setLayout(layout)
        self.tasks_list = tasks

    # Main Menu Functions
    def refresh_tasks_list(self):
        self.t_list.clear()

        pending_tasks = sorted([t for t in tasks if not t.completed], key=attrgetter('due_date'))
        completed_tasks = sorted([t for t in tasks if t.completed], key=attrgetter('due_date'))

        max_name_length = 35

        for i in pending_tasks:
            days_left = (i.due_date - datetime.now().date()).days

            if days_left <= 1:
                icon = "🔴"
                urgency = "URGENT"
            elif days_left <= 3:
                icon = "🟡"
                urgency = "Soon"
            else:
                icon = "🟢"
                urgency = "OK"

            name_short = (i.name + " " * max_name_length)[:max_name_length]
            text = f"{icon} {name_short} {i.due_date.strftime('%m-%d-%Y')} ({urgency})"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, i)
            self.t_list.addItem(item)

        separator = QListWidgetItem("───────────────────────── COMPLETED ─────────────────────────")
        separator.setData(Qt.UserRole, None)
        font = separator.font()
        font.setItalic(True)
        separator.setFont(font)
        self.t_list.addItem(separator)

        for i in completed_tasks:
            name_short = (i.name + " " * max_name_length)[:max_name_length]
            text = f"✅ {name_short}  {i.due_date.strftime('%Y-%m-%d')}"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, i)
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
            self.t_list.addItem(item)

    def open_list_tasks_window(self):
        self.list_tasks_window = ListTasksWindow(self)
        self.list_tasks_window.show()

    def open_task_details(self, item):
        if item:
            task = item.data(Qt.UserRole)
            dlg = TaskDetailsWindow(task, self)
            dlg.exec_()

    def remove_selected_task(self):
        current_row = self.t_list.currentRow()
        if current_row >=0:
            item = self.t_list.item(current_row)
            task = item.data(Qt.UserRole)
            tasks.remove(task)
            self.refresh_tasks_list()
        else:
            QMessageBox.warning(self, "No selected task", "Please first select a task to remove.")

    def mark_completed(self):
        current_row = self.t_list.currentRow()
        if current_row >=0:
            item = self.t_list.item(current_row)
            task = item.data(Qt.UserRole)
            if not task.completed:
                task.completed = True
            elif task.completed:
                task.completed = False
            self.refresh_tasks_list()
        else:
            QMessageBox.warning(self, "No selected task", "Please select a task first.")

    def open_add_task_window(self):
        dialog = AddTaskWindow(self)
        task_data = dialog.get_task_data()

        if task_data:
            try:
                new_task = Task(task_data['name'], task_data['due_date'], task_data['description'])
                tasks.append(new_task)
                self.refresh_tasks_list()
            except ValueError as e:
                QMessageBox.critical(self, "Task Error", f"Task creation error: {e}")

    def do_save_tasks(self):
        if self.confirm_save("tasks.pkl"):
            save_tasks()
            print("✅ Tasks Successfully Saved!")
        else:
            print("❌ Save Canceled")

    def confirm_save(self, filename="tasks.pkl"):
        dialog = QDialog(self)
        dialog.setWindowTitle("💾 Confirmation")
        dialog.setFixedSize(400,250)
        dialog.setModal(True)

        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 12px;
            }
            QLabel {
                font-size: 16px;
                font-weight: 500;
                padding: 20px;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
            QPushButton#cancel {
                background-color: #95a5a6;
            }
            QPushButton#cancel:hover {
                background-color: #7f8c8d;
            }
        """)

        icon_label = QLabel("💾")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; margin-bottom: 1px;")

        message = QLabel(f"Confirm save: {filename}")
        message.setAlignment(Qt.AlignCenter)

        yes_button = QPushButton("✅ Yes, SAVE")
        yes_button.setObjectName("yes")
        no_button = QPushButton("❌ CANCEL")
        no_button.setObjectName("cancel")

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(yes_button)
        buttons_layout.addWidget(no_button)
        buttons_layout.addStretch()

        layout = QVBoxLayout(dialog)
        layout.addWidget(icon_label, 0, Qt.AlignCenter)
        layout.addWidget(message)
        layout.addLayout(buttons_layout)
        layout.setSpacing(10)

        result = {"accepted": False}

        def on_yes():
            result["accepted"] = True
            dialog.accept()

        def on_no():
            result["accepted"] = False
            dialog.reject()

        yes_button.clicked.connect(on_yes)
        no_button.clicked.connect(on_no)

        dialog.exec_()
        return result["accepted"]

    def quit(self):
        self.close()

##  Load Tasks 1st time, then launch main window

load_tasks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec_())

