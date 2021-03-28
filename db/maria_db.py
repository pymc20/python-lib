import pymysql
import re


class MariaDb:
    def __init__(self, config):
        self.conn = None
        self.cur = None
        self.config = config

    def get_schema(self):
        conn = pymysql.connect(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["password"],
            db=self.config["db"],
            charset=self.config["charset"])
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        f = open("orm.py", "w")
        for table in tables:
            cur.execute("SHOW COLUMNS FROM " + table[0])
            columns = cur.fetchall()
            column_text = "class {0}(Base):\n".format("".join([t.title() for t in table[0].split("_")]))
            column_text += "\t__tablename__ = '{0}'\n".format(table[0])
            for column in columns:
                db_type = re.findall(r"[a-z|A-Z]", column[1])
                column_text += "\t{0} = Column('{0}', {1}{2}{3})\n".format(
                    column[0],
                    convert_type("".join(db_type), column[1]),
                    ", nullable=True" if column[2] == "YES" else "",
                    ", primary_key=True" if column[3] == "PRI" else "")
            f.write(column_text)

        conn.close()
        f.close()


def convert_type(db_type, column_type):
    if db_type == "varchar":
        return column_type.replace(db_type, "String")
    elif db_type == "char":
        return column_type.replace(db_type, "String")
    elif db_type == "int":
        return "Integer"
    elif db_type == "bigint":
        return "BigInteger"
    elif db_type == "datetime":
        return "DateTime"
    else:
        return db_type.title()
