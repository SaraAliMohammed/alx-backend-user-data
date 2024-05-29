#!/usr/bin/env python3
""" Personal data module """
import logging
from os import environ
import re
from typing import List
from mysql.connector import connection


PII_FIELDS = ("name", "email", "password", "phone", "ssn")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns the log message obfuscated """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """ Get the logger obj  """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """ Connection to mysql server with environmental variables """
    user_name = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    user_password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    db_connector = connection.MySQLConnection(
        user=user_name,
        password=user_password,
        host=db_host,
        database=db_name)
    return db_connector


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter class implementation"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ inits class instance """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filters values in incoming log records """
        return filter_datum(
            self.fields, self.REDACTION, super().format(record),
            self.SEPARATOR)


def main() -> None:
    """
    Implement the main function to
    Obtain a database connection using get_db
    and retrieve all rows in the users table and display each row
    """
    db = get_db()
    cursor = db.cursor()

    query = ('SELECT * FROM users;')
    cursor.execute(query)
    fetch_data = cursor.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        logger.info(fields)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
