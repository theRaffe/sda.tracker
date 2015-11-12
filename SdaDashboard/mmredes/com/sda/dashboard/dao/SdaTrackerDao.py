import sqlite3 as lite
import time
import sys

__author__ = 'macbook'


class SdaTrackerDao:
    'Class for accessing to sqlite database'
    conn = None

    def __init__(self, connectionFile):
        self.conn = lite.connect(connectionFile)

    def do_rollback(self):
        self.conn.rollback()

    def do_commit(self):
        self.conn.commit()

    def get_artifacts(self):
        dict_artifact = {}
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from cat_artifact")
        rows = cur.fetchall()
        for row in rows:
            key = row["path_directory"]
            value_key = row["code_artifact"]
            dict_artifact[key] = value_key

        return dict_artifact

    def get_list_artifacts(self):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from cat_artifact")
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(dict(zip(row.keys(), row)))
        return result

    def get_ticket(self, id_ticket, id_status=1):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from ticket_board where id_ticket = :id_ticket and id_status = :id_status",
                    {"id_ticket": id_ticket, "id_status": id_status})
        return cur.fetchone()

    def get_ticket_artifact(self, id_ticket, id_artifact, id_type_tech):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute(
            "select * from ticket_artifact where id_ticket = :id_ticket and id_artifact = :id_artifact and id_type_tech = :id_type_tech",
            {"id_ticket": id_ticket, "id_artifact": id_artifact, "id_type_tech": id_type_tech})

        return cur.fetchone()

    def get_default_environment(self, id_branch):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute(
            "select * from cat_branch_git where id_branch = :id_branch", {"id_branch": id_branch})
        row = cur.fetchone()
        return row["id_environment_def"]

    def get_ticket_board_code(self, id_ticket):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute(
            "select id_ticket, code_environment, code_status, datetime(date_requested,'unixepoch','localtime') date_requested, user_request"
            "from ticket_board "
            "inner join cat_environment on cat_environment.id_environment = ticket_board.id_environment"
            "inner join cat_status on cat_status.id_status = ticket_board.id_status"
            " where ticket_board.id_ticket = :id_branch", {"id_branch": id_ticket})
        row = cur.fetchone()

    def insert_ticket_board(self, dict_ticket_board):
        cur = self.conn.cursor()
        date_requested = time.time()
        id_ticket = dict_ticket_board["id_ticket"]
        id_environment = dict_ticket_board["id_environment"]
        user_request = dict_ticket_board["user_request"]
        cur.execute(
            "insert into ticket_board(id_ticket, id_environment, id_status, user_request, date_requested) values(:id_ticket, :id_environment, :id_status, :user_request, :date_request)",
            {"id_ticket": id_ticket, "id_environment": id_environment, "id_status": 1, "user_request": user_request,
             "date_request": date_requested}
        )
        # self.conn.commit()

    def update_ticket_board(self, dict_ticket_board):
        cur = self.conn.cursor()
        date_requested = time.time()
        cur.execute(
            "update ticket_board set date_requested = :date_requested, user_request = :user_request where id_ticket = :id_ticket and id_environment = :id_environment",
            {"date_requested": date_requested, "user_request": dict_ticket_board["user_request"],
             "id_ticket": dict_ticket_board["id_ticket"], "id_environment": dict_ticket_board["id_environment"]})
        # self.conn.commit()

    def update_ticket_artifact(self, id_ticket, dict_artifact):
        cur = self.conn.cursor()
        date_current = time.time()
        modification_user = dict_artifact["email"]
        id_artifact = dict_artifact["id_artifact"]
        id_type_tech = dict_artifact["id_type_tech"]
        cur.execute(
            "update ticket_artifact set modification_user = :modification_user, modification_date = :modification_date where id_ticket = :id_ticket and id_artifact = :id_artifact and id_type_tech = :id_type_tech",
            {"modification_user": modification_user, "modification_date": date_current, "id_ticket": id_ticket,
             "id_artifact": id_artifact, "id_type_tech": id_type_tech})
        # self.conn.commit()

    def insert_ticket_artifact(self, id_ticket, dict_artifact):
        cur = self.conn.cursor()
        date_current = time.time()
        creation_user = dict_artifact["email"]
        id_artifact = dict_artifact["id_artifact"]
        id_type_tech = dict_artifact["id_type_tech"]
        cur.execute(
            "insert into ticket_artifact(id_ticket, id_artifact, id_type_tech, creation_user, creation_date) values(:id_ticket, :id_artifact, :id_type_tech, :creation_user, :creation_date)",
            {"id_ticket": id_ticket, "id_artifact": id_artifact, "id_type_tech": id_type_tech, "creation_user":
                creation_user, "creation_date": date_current}
        )
        # self.conn.commit()
