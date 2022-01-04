import psycopg2
import logging # add logging
class ConnectionContext:
    def __init__(self, id, **con_args):
        self.id = id
        self.conn = psycopg2.connect(**con_args)
        print(f"Connection with id {self.id} created")
        self.busy = False
    
    def close(self):
        # what about the cursor? -> let the query handle this
        self.conn.close()
        print(f"Connection with id {self.id} closed")

    # for use as a context manager
    def __enter__(self):
        self.busy = True
        print(f"Connection {self.id} has been marked as busy")

        return self.conn

    # for use as a context manager
    def __exit__(self, type, value, traceback):
        self.busy = False
        print(f"Connection {self.id} is no longer busy")

class DB:
    def __init__(self, **conn_args):
        self.conn_args = conn_args
        self.pool = []

    def _add_connection(self):
        conn = ConnectionContext(id=len(self.pool)+1, **self.conn_args)
        self.pool.append(conn)
        
        return conn

    def connect_pool(self, num_conns=1):
        for _ in range(num_conns):
            self._add_connection()

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
            conn = self._add_connection()
            self.pool.append(conn)

        print(f"Using conn {conn.id}")

        result = None
        with conn as c:
            with c.cursor() as cursor:
                cursor.execute(query, *args, **kwargs)
                result = cursor.fetchall() # is this good?
                c.commit()

        return result
        # return {}
# class DB:
#     def __init__(self, database, host, port, user, password):
#         self.conn_params = dict(database=database, host=host, port=port, user=user, password=password)
#         self.conn = None
#         self.cur = None

#     def connect(self):
#         if not self.conn:
#             try:
#                 self.conn = psycopg2.connect(**self.conn_params)
#                 print('Successfully connected to db...')
#             except:
#                 print('Failed to connect to db...')
#         return self

#     def execute(self, query, *args, **kwargs):
#         self.cur = self.conn.cursor()
#         self.cur.execute(query, *args, **kwargs) # weird stuff happens when a cursor is still in use and another api endpoint tries to execute a query
#         result = self.cur.fetchall() # not optimized?
#         self.conn.commit() # should this be here?
#         self.cur.close() # close the cursor frequently or it can eat up resources through cached values
#         return result

#     def close(self):
#         self.conn.close()
#         print('Successfully closed db connection...')
#         return self