from .db_connect import connection_dec
from typing import Dict, Tuple


class ConnectDB:
    """ Includes methods to interact with database """

    @connection_dec
    def __init__(self, cursor=None):
        """Creates table is not exists"""
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            sex TEXT,
            course TEXT,
            photo_path TEXT
        )
        ''')

    @connection_dec
    async def write_user_data(self, user_data: Dict, cursor=None):
        write_query = '''
        INSERT INTO bot_users (id, name, sex, course, photo_path)
        VALUES (?, ?, ?, ?)
        '''
        data: Tuple = (user_data['name'], user_data['sex'], user_data['course'], user_data['photo_path'])
        cursor.execute(write_query, data)


