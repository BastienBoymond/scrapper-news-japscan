class Supabase:
    def __init__(self):
        import os
        from dotenv import load_dotenv
        from supabase import create_client, Client
        load_dotenv()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    def check_db_empty(self, table):
        data = self.supabase.table(table).select('*').execute().data
        if not data:
            return True
        return False

    def get(self, table):
        return self.supabase.table(table).select('*').execute().data

    def insert(self, table, data):
        return self.supabase.table(table).insert(data).execute()

    def find(self, table, typeEq, id):
        return self.supabase.table(table).select('*').eq(typeEq, id).execute()

    def find_if_exist(self, table, typeEq, id):
        data = self.find(table, typeEq, id)
        if data.data:
            return data.data
        return None

    def update(self, table, typeEq, id, data):
        return self.supabase.table(table).update(data).eq(typeEq, id).execute()
    
    def delete(self, table, typeEq, id):
        return self.supabase.table(table).delete().eq(typeEq, id).execute()
    
    def getnbrows(self, table):
        return self.supabase.table(table).select('ean', count='exact').execute().count

    def check_exist_string(self, table, typeEq, str):
        data = self.supabase.table(table).select('*').ilike(typeEq, str).execute().data
        if data:
            return True
        return False
    
    def update_str(self, table, typeEq, str, data):
        return self.supabase.table(table).update(data).ilike(typeEq, str).execute()

class Postgres:
    def __init__(self):
        import os
        from dotenv import load_dotenv
        import psycopg2
        load_dotenv()
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        self.cursor = self.conn.cursor()

    def show_tables(self):
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        return self.cursor.fetchall()

    def insert(self, table, type, data, format):
        self.cursor.execute(f"INSERT INTO \"{table}\" {type} VALUES {format};", data)
        self.conn.commit()

    def update(self, table, type, data, format, id):
        self.cursor.execute(f"UPDATE \"{table}\" SET {type} = {format} WHERE id = {id};", data)
        self.conn.commit()

    def update_str(self, table, compare, str, type, data, format):
        self.cursor.execute(f"UPDATE \"{table}\" SET {type} = {format} WHERE {compare} = \'{str}\';", data)
        self.conn.commit()

    def check_if_exist_string(self, table, type, str):
        self.cursor.execute(f"SELECT * FROM \"{table}\" WHERE {type} = \'{str}\';")
        data = self.cursor.fetchall()
        if data:
            return True
        return False
    
    def get(self, table):
        self.cursor.execute("SELECT * FROM \"" + table + "\";")
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
