#!/usr/bin/env python3
"""Regexing
"""

from typing import List
import re
import logging
from os import environ
import mysql.connector



patterns = {
    'extract': lambda fields, separator: r'(?P<field>{})=([^{}]+)'.format('|'.join(map(re.escape, fields)), re.escape(separator)),
    'replace': lambda redaction: r'\g<field>={}'.format(redaction),
}


# tyhe PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List[str], redaction:str, 
        message: str, separator: str) -> str:
    """
    Filters a log file
    """

    pattern = patterns['extract'](fields, separator)
    replacement = patterns['replace'](redaction)
    return re.sub(pattern, replacement, message)


def get_logger() -> logging.Logger:
    """Creates a new logger for user data.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to the database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")        db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_pwd,
            database=db_name,
    )
    return connection

def main():
    """Logs the information about a user records in a table
    """
    fields = "name,email,phone,ssn,password,ip,last_login, user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handler(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for redact in log messages

        Args:
            fields: list of fields to redact in log messages
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using filter_datum
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)

