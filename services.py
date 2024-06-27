from db import Database
from exceptions import BadRequestException
from models import User
from utils import make_password, match_password


class AuthService:

    def __init__(self):
        self.database = Database()
        super().__init__()

    def register_user(self, user: User):
        if self.database.check_username_unique(user.username):
            user.password = make_password(password=user.password)
            self.database.insert_user(**user.__dict__)
        else:
            raise BadRequestException(f"{user.username} username already registered")

    def login_user(self, username, password):
        data = self.database.get_user_by_username(username)
        user = User(username=data[1], password=data[2], email=data[3], phone=data[4])
        user.id = data[0]
        if match_password(password=password, hashed_password=user.password):
            return user
        else:
            raise BadRequestException("Password is not correct")


class TodoService:
    def __init__(self, user):
        self.user = user
        self.database = Database()

    def create_todo(self, title):
        self.database.insert_todo(title=title, status="todo", owner_id=self.user.id)

    def update_todo(self, todo_id, value):
        db_user_id = self.database.check_exists_todo_user(todo_id)
        if self.user.id == db_user_id[0]:
            self.database.update_todo(todo_id=todo_id, value=value)
        else:
            print("You can update only your todos!!!")

    def my_todos(self):
        data = self.database.my_todos(self.user.id)
        return data

    def delete_todo(self, todo_id):
        db_user_id = self.database.check_exists_todo_user(todo_id)
        if self.user.id == db_user_id[0]:
            self.database.delete_todo(todo_id=todo_id)
        else:
            print("You can delete only your todos!!!")

    def edit_todo_title(self, todo_id, title):
        db_user_id = self.database.check_exists_todo_user(todo_id)
        if self.user.id == db_user_id[0]:
            self.database.edit_todo_title(todo_id=todo_id, title=title)
        else:
            print("You can edit only your todos!!!")
