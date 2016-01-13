# coding=utf-8
import logging
import sqlite3 as lite
import time

__author__ = 'macbook'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
            value_key = row["id_artifact"]
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
        cur.execute("select id_environment from ticket_library where id_ticket = :id_ticket",
                    {"id_ticket": id_branch})
        row = cur.fetchone()
        if not row:
            cur.execute(
                "select * from cat_branch_git where id_branch = :id_branch", {"id_branch": id_branch})
            row = cur.fetchone()
            return row["id_environment_def"]

        return row["id_environment"]

    def get_ticket_board_code(self, id_ticket):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute(
            "select ticket_board.id_ticket,"
            "ticket_board.id_environment, "
            "cat_environment.code_environment, "
            "cat_environment.id_list_tracker, "
            "ticket_board.id_card_tracker, "
            "cat_status_ticket.code_status, "
            "date_requested, "
            "datetime(ticket_board.date_requested,'unixepoch','localtime') date_format_requested, "
            "ticket_board.user_request "
            "from ticket_board "
            "inner join cat_environment on cat_environment.id_environment = ticket_board.id_environment "
            "inner join cat_status_ticket on cat_status_ticket.id_status = ticket_board.id_status "
            "where ticket_board.id_ticket = :id_ticket", {"id_ticket": id_ticket})
        return cur.fetchone()

    def get_artifact_code(self, id_ticket):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute(
            "select code_artifact artifact, "
            "code_type_tech tech, "
            "modification_user user "
            "from  ticket_artifact "
            "inner join cat_type_tech on cat_type_tech.id_type_tech = ticket_artifact.id_type_tech "
            "inner join cat_artifact on cat_artifact.id_artifact = ticket_artifact.id_artifact "
            "where id_ticket = :id_ticket", {"id_ticket": id_ticket})
        return cur.fetchall()

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

    def insert_ticket_logging(self, id_ticket, dict_artifact):
        cur = self.conn.cursor()
        date_current = time.time()
        creation_user = dict_artifact["email"]
        id_artifact = dict_artifact["id_artifact"]

        self.conn.row_factory = lite.Row
        cur.execute(
            "select max(id_ticket_row) + 1 id_ticket_row "
            "from ticket_artifact_logging "
            "where id_ticket = :id_ticket", {"id_ticket": id_ticket})
        row = cur.fetchone()
        id_ticket_row = row["id_ticket_row"] if row and row["id_ticket_row"] else 1

        cur.execute(
            "insert into ticket_artifact_logging(id_ticket, id_ticket_row, id_artifact, creation_user, creation_date) "
            "values(:id_ticket, :id_ticket_row, :id_artifact, :creation_user, :creation_date)",
            {"id_ticket": id_ticket, "id_ticket_row": id_ticket_row, "creation_user":
                creation_user, "creation_date": date_current, "id_artifact": id_artifact}
        )

    def update_ticket_board(self, dict_ticket_board):
        print ("update board", dict_ticket_board)
        cur = self.conn.cursor()
        date_requested = time.time()
        cur.execute(
            "update ticket_board set date_requested = :date_requested, "
            "user_request = :user_request, id_card_tracker = :id_card_tracker "
            "where id_ticket = :id_ticket and id_environment = :id_environment",
            {"date_requested": date_requested, "user_request": dict_ticket_board["user_request"],
             "id_card_tracker": dict_ticket_board["id_card_tracker"],
             "id_ticket": dict_ticket_board["id_ticket"], "id_environment": dict_ticket_board["id_environment"]})
        # self.conn.commit()

    def update_ticket_artifact(self, id_ticket, dict_artifact):
        cur = self.conn.cursor()
        date_current = time.time()
        modification_user = dict_artifact["email"]
        id_artifact = dict_artifact["id_artifact"]
        id_type_tech = dict_artifact["id_type_tech"]
        cur.execute(
            "update ticket_artifact set modification_user = :modification_user, "
            "modification_date = :modification_date "
            "where id_ticket = :id_ticket and "
            "id_artifact = :id_artifact and "
            "id_type_tech = :id_type_tech",
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
            "insert into ticket_artifact(id_ticket, id_artifact, id_type_tech, creation_user, creation_date, modification_user) values(:id_ticket, :id_artifact, :id_type_tech, :creation_user, :creation_date, :modification_user)",
            {"id_ticket": id_ticket, "id_artifact": id_artifact, "id_type_tech": id_type_tech, "creation_user":
                creation_user, "creation_date": date_current, "modification_user": creation_user}
        )

    def update_list_tracker(self, code_env, id_list_tracker):
        cur = self.conn.cursor()
        cur.execute(
            "update cat_environment set id_list_tracker = :id_list_tracker "
            "where code_environment = :code_env",
            {"code_env": code_env, "id_list_tracker": id_list_tracker})

    def add_upd_library_ticket(self, dict_ticket):
        cur = self.conn.cursor()
        date_current = time.time()
        id_ticket = dict_ticket["id_ticket"]
        id_environment = dict_ticket["id_environment"]
        description = dict_ticket["description"]

        cur.execute(
            "select * "
            "from ticket_library "
            "where id_ticket = :id_ticket", {"id_ticket": id_ticket})
        row = cur.fetchone()
        if row:
            logger.info("update: %s" % dict_ticket)
            cur.execute("update ticket_library set id_environment = :id_environment, description = :description "
                        "where id_ticket = :id_ticket",
                        {"id_ticket": id_ticket, "id_environment": id_environment, "description": description})
        else:
            logger.info("insert: %s" % dict_ticket)
            cur.execute("insert into ticket_library(id_ticket, id_environment, description, creation_date)"
                        "values(:id_ticket, :id_environment, :description, :creation_date)",
                        {"id_ticket": id_ticket, "id_environment": id_environment, "description": description,
                         "creation_date": date_current})

    def translate_environment(self, dict_defect):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()

        crm = dict_defect["crm"]
        environment = dict_defect["environment"]

        cur.execute("SELECT * from translate_environment where crm = :crm and environment = :environment",
                    {"crm": crm, "environment": environment})
        row = cur.fetchone()

        id_environment = row["id_environment"] if row and row["id_environment"] else None
        return id_environment
