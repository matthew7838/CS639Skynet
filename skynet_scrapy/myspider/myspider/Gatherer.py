import psycopg2
from psycopg2.errors import UniqueViolation


class Gatherer:

    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        print('creating ucs_new_launches table')

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS ucs_new_launches(
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
                         COSPAR text primary key,
                         NORAD integer,
                         source_used_for_orbital_data text,
                         source text,
                         additional_source text,
                         data_status integer)""")
        self.connection.commit()

    def gather(self):
        sql_query = """
            INSERT INTO ucs_new_launches (
                full_name, 
                official_name, 
                owner_country, 
                owner, 
                users, 
                orbit_class,
                orbit_type,
                in_geo, 
                perigee, 
                apogee, 
                inclination, 
                period, 
                mass, 
                dry_mass, 
                launch_date, 
                contractor, 
                launch_site, 
                launch_vehicle, 
                cospar, 
                norad,
                source_used_for_orbital_data,
                data_status)
            SELECT
                plname,
                name,
                state,
                owner,
                mission_sector,
                oporbit,
                orbit_type,
                CASE 
                    WHEN oporbit LIKE '%GEO%' THEN 1 
                    ELSE 0 
                END,
                perigee,
                apogee,
                inc,
                period,
                mass,
                drymass,
                ldate,
                manufacturer,
                launch_site,
                launch_vehicle,
                piece,
                satcat,
                source_used_for_orbital_data,
                data_status         
            FROM planet4589
            ON CONFLICT (cospar) DO NOTHING
        """
        try:
            self.cur.execute(sql_query)
            self.connection.commit()
        except UniqueViolation as e:
            self.connection.rollback()
            print(f'Error: {e}')
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f'Error during item processing: {e}')
        finally:
            self.cur.close()
            self.connection.close()



            # SET
            #     full_name = EXCLUDED.full_name,
            #     official_name = EXCLUDED.official_name,
            #     owner_country = EXCLUDED.owner_country,
            #     owner = EXCLUDED.owner,
            #     users = EXCLUDED.users,
            #     orbit_class = EXCLUDED.orbit_class,
            #     orbit_type = EXCLUDED.orbit_type,
            #     in_geo = EXCLUDED.in_geo,
            #     perigee = EXCLUDED.perigee,
            #     apogee = EXCLUDED.apogee,
            #     inclination = EXCLUDED.inclination,
            #     period = EXCLUDED.period,
            #     mass = EXCLUDED.mass,
            #     dry_mass = EXCLUDED.dry_mass,
            #     launch_date = EXCLUDED.launch_date,
            #     contractor = EXCLUDED.contractor,
            #     launch_site = EXCLUDED.launch_site,
            #     launch_vehicle = EXCLUDED.launch_vehicle,
            #     cospar = EXCLUDED.cospar,
            #     norad = EXCLUDED.norad,
            #     source_used_for_orbital_data = EXCLUDED.source_used_for_orbital_data,
            #     data_status = EXCLUDED.data_status