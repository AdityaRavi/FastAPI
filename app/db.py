import psycopg2

# get from environment variables?
db = 'social_media'
host = 'localhost'
port = 5432
user = 'postgres'
password = 'postgres'


class DB:

    def execute(self, query, *args, **kwargs):
        with psycopg2.connect(host=host,
                              port=port,
                              user=user,
                              database=db,
                              password=password) as conn:
            with conn.cursor() as cur:
                cur.execute(query, *args, **kwargs)
                return cur.fetchall()
