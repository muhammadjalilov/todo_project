import psycopg2

import os

from dotenv import load_dotenv

load_dotenv("/home/muhammad/Desktop/programming/git/todo_project/.env")


class Database:
    def __init__(self):
        self.db = psycopg2.connect(
            host="127.0.0.1",
            dbname=os.getenv("database_name"),
            password=os.getenv("postgres_password"),
            user=os.getenv("postgres_user"),
        )
        self.db.autocommit = True

    def create_user_table(self):
        with self.db.cursor() as cursor:
            create_user_sql = """
                create table if not exists users(
                    id serial primary key,
                    username varchar(128) unique not null, 
                    password varchar(128) not null,
                    email varchar(56),
                    phone varchar(56)
                );             
            """
            cursor.execute(create_user_sql)

    def create_todo_table(self):
        with self.db.cursor() as cursor:
            create_user_sql = """
                        create table if not exists todo(
                            id serial primary key,
                            title varchar(128) unique not null, 
                            status varchar(128) not null,
                            owner_id int references users(id),
                            deadline timestamp default now()+interval '1 day'
                        );             
                    """
            cursor.execute(create_user_sql)

    def insert_user(self, username, password, email, phone):
        insert_user_sql = """
        insert into users(username, password, email, phone) values (%s,%s,%s,%s);
        """
        with self.db.cursor() as cursor:
            cursor.execute(insert_user_sql, (username, password, email, phone))

    def insert_todo(self, title, status, owner_id):
        insert_todo_sql = """
                    insert into todo(title, status, owner_id) values (%s,%s,%s); """
        with self.db.cursor() as cursor:
            cursor.execute(insert_todo_sql, (title, status, owner_id))

    def check_username_unique(self, username):
        search_username_unique_sql = """
                select * from users where username=%s; """
        with self.db.cursor() as cursor:
            cursor.execute(search_username_unique_sql, (username,))
            result = cursor.fetchall()
            if result:
                return False
            else:
                return True

    def get_user_by_username(self, username):
        search_username_sql = """
            SELECT * FROM users WHERE username = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(search_username_sql, (username,))
            result = cursor.fetchone()
            return result

    def update_todo(self, todo_id, value):
        update_todo_sql = """
            update todo set status=%s where id=%s
        """
        with self.db.cursor() as cursor:
            cursor.execute(update_todo_sql, (value, todo_id))

    def delete_todo(self, todo_id):
        delete_todo_sql = """
            delete from todo where id=%s
        """
        with self.db.cursor() as cursor:
            cursor.execute(delete_todo_sql, (todo_id,))

    def my_todos(self, user_id):
        my_todo_sql = "select * from todo where owner_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(my_todo_sql, (user_id,))
            data = cursor.fetchall()
            return data

    def edit_todo_title(self, todo_id, title):
        edit_todo_title_sql = """
            update todo set title = %s where id = %s
                """
        with self.db.cursor() as cursor:
            cursor.execute(edit_todo_title_sql, (title, todo_id))

    def check_exists_todo_user(self, todo_id):
        check_exists_todo_user_sql = """
            select owner_id from todo where id =%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(check_exists_todo_user_sql, (todo_id,))
            res = cursor.fetchone()
            return res


if __name__ == '__main__':
    db = Database()
    db.create_user_table()
    db.create_todo_table()
    # db.insert_user("ahmadjon", "testpassword", "ahmadjon@gmail.com", "+998911112233")
    # db.insert_todo("make gpt 4a", "todo", "1")
    # print(db.get_user_by_username("ahmadjon"))
