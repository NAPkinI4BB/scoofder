import sqlite3 as sq
from sqlite3 import Error
from typing import Callable


def connection_dec(func: Callable):
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = sq.connect('users.db')
            cursor = connection.cursor()
            result = func(*args, **kwargs, cursor=cursor)
            connection.commit()
            return result
        except Error as e:
            print(f'DB connection error {e}')
        finally:
            if connection:
                connection.close()
    return wrapper
