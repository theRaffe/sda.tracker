import sqlite3 as lite
import sys

__author__ = 'macbook'
class SdaTrackerDao:
    'Class for accessing to sqlite database'
    conn = None
    def __init__(self, connectionFile):
        self.conn = lite.connect(connectionFile)

    def get_artifacts(self):
        dict_artifact = {}
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from cat_artifact")
        rows = cur.fetchall()
        for row in rows:
            key = row["id_artifact"]
            value_key = row["path_directory"]
            dict_artifact[key] = value_key

        return dict_artifact
