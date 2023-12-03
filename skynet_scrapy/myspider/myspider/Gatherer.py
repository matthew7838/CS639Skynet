import psycopg2


class Gatherer:

    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS UCS_table(
                         full_name text,
                         official_name text,
                         country text,
                         owner_country text,
                         owner text,
                         users text,
                         purpose text,
                         detail_purpose text,
                         orbit_class text,
                         orbit_type text,
                         in_GEO INT,
                         perigee integer,
                         apogee integer,
                         eccentricity TEXT,
                         inclination double precision,
                         period text,
                         mass double precision,
                         dry_mass double precision,
                         power text,
                         launch_date date,
                         expected_lifetime TEXT,
                         contractor text,
                         contractor_country text,
                         launch_site text,
                         launch_vehicle text,
                         COSPAR text PRIMARY KEY,
                         NORAD integer,
                         source text,
                         additional_source text)""")
        # extra line
        self.connection.commit()

    def gather(self):
        sql_query = """
            INSERT INTO UCS_table (full_name, official_name, owner_country, owner, orbit_class, in_geo, perigee, apogee, inclination, mass, dry_mass, launch_date, contractor, cospar, norad)
            SELECT
                plname,
                name,
                state,
                owner,
                oporbit,
                CASE 
                    WHEN oporbit LIKE '%GEO%' THEN 1 
                    ELSE 0 
                END,
                perigee,
                apogee,
                inc,
                mass,
                drymass,
                ldate,
                manufacturer,
                piece,
                satcat           
            FROM planet4589
        """
        self.cur.execute(sql_query)
        self.connection.commit()




