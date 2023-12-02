import psycopg2


class Deletions:
    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS deletion_table(
            COSPAR text PRIMARY KEY
        )""")
        # extra line
        self.connection.commit()

    def MarkDeletions(self):
        sql_query = """
            INSERT INTO deletion_table (COSPAR)
            (
                SELECT u.COSPAR
                FROM UCS_table u
                JOIN orbitalfocus o ON u.NORAD = o.cat_no AND u.COSPAR = o.designation
            )
            UNION
            (
                SELECT u.COSPAR
                FROM UCS_table u
                JOIN aero a ON u.NORAD = a.norad_num AND u.COSPAR = a.cospar_num
            );
        """
        self.cur.execute(sql_query)
        self.connection.commit()
