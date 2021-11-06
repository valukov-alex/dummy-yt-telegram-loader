from psycopg2 import connect, errors

class PostgresID:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        print("host = {}, port = {}".format(self.host, self.port))

    def connect_to_db(self):
        self.conn = connect(
            dbname = self.dbname,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )

    def _rollback(self):
        cursor = self.conn.cursor()
        cursor.execute("ROLLBACK")
        cursor.close()
    
    def create_table(self, table_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("CREATE TABLE {} (user_id varchar);".format(table_name))
            self.conn.commit()
            cursor.close()
            print("create table with name {}".format(Constant.DB_TABLE_NAME))

        except errors.DuplicateTable as e:
            print("Table {} already exists".format(table_name))
            self._rollback()

    def insert_user(self, table_name, user_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO {} VALUES ('{}')".format(table_name, user_id))
        self.conn.commit()
        cursor.close()

    def is_user_exists(self, table_name, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT exists (SELECT 1 FROM {} WHERE user_id = '{}')".format(table_name, user_id))
        is_exists = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return is_exists
