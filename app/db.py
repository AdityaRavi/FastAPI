import psycopg2
from contextlib import contextmanager

# TODO
# Logging
# Improve pool implementation: min conns, max conns, max conns allowed by postgres, prune conns, etc.
# Native pool of psycopg2
# Asyncpg
class Connection:
    def __init__(self, id, **con_args):
        self.id = id
        self.conn = psycopg2.connect(**con_args)
        self.busy = False
        print(f"Connection {self.id} created")
    
    def close(self):
        self.conn.close()
        print(f"Connection {self.id} closed")

    @contextmanager
    def cursor(self):
        cur = None
        # How to gracefully handle exceptions here?
        try:
            cur = self.conn.cursor()
            self.busy = True
            print(f"Connection {self.id} busy")
            yield cur
        finally:
            if cur:
                cur.close()
            self.busy = False
            print(f"Connection {self.id} free")

    def commit(self):
        self.conn.commit()

class DB:
    def __init__(self, **conn_args):
        self.conn_args = conn_args
        self.pool = []

    def __add_connection(self, id):
        conn = Connection(id=id, **self.conn_args)
        self.pool.append(conn)
        
        return conn

    def connect_pool(self, num_conns=1):
        for i in range(num_conns):
            self.__add_connection(i+1)

        return self

    def close_pool(self):
        for conn in self.pool:
            conn.close()
    
    def execute(self, query, *args, **kwargs):
        conn = None

        for _conn in self.pool:
            if not _conn.busy:
                conn = _conn
                break

        if not conn:
            print('All connections busy. Creating new connection...')
            conn = self.__add_connection(len(self.pool)+1)

        result = None
        with conn.cursor() as cur:
            # try except block that rolls back changes if the execute fails?
            cur.execute(query, *args, **kwargs)
            result = cur.fetchall() # this is not good
            conn.commit() # should this be done everytime? If so, use auto commit?

        return result
