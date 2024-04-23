import sqlite3


def database_wrapper(func):
    def wrapper(*args, **kwargs):
        # Code executed before calling the function
        connection = sqlite3.connect('../data/database/Database.db')
        cursor = connection.cursor()

        result = func(cursor, *args, **kwargs)

        # Code executed after calling the function
        connection.close()

        return result

    return wrapper


def modify_database_wrapper(func):
    def wrapper(*args, **kwargs):
        # Code executed before calling the function
        connection = sqlite3.connect('../data/database/Database.db')
        cursor = connection.cursor()

        result = func(cursor, *args, **kwargs)

        # Code executed after calling the function
        connection.commit()
        connection.close()

        return result

    return wrapper
