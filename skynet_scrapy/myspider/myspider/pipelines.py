# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
from datetime import datetime
import psycopg2


class OrbitalfocusPipeline:

    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'postgres'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        print("creating orbitalfocus table")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS orbitalfocus(
                         cat_no integer,
                         designation text,
                         name text,
                         date date)""")
        # extra line
        #self.connection.commit()

    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            field_names = adapter.field_names()
            for field_name in field_names:
                if field_name in ['cat_no', 'designation']:
                    if field_name is 'cat_no':
                        value = adapter.get(field_name).replace(u"\xa0\xa0", "")
                        adapter[field_name] = value
                    if field_name is 'designation':
                        value = adapter.get(field_name).replace(u"\xa0", "")
                        adapter[field_name] = value
                if field_name is 'date':
                    value = adapter.get(field_name)
                    parsed_date = datetime.strptime(value, '%Y %b %d')
                    value = parsed_date.strftime('%-m/%-d/%y')
                    adapter[field_name] = value
            self.cur.execute(""" insert into orbitalfocus (cat_no, designation, name, date) values (%s, %s, %s, %s)""",
                             (
                                 item['cat_no'],  # norad num
                                 item['designation'],  # cospar num
                                 item['name'],
                                 item['date'],
                             ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            # print(f'Error during item processing: {e}')
        return item


class ReentrypredictorPipeline:
    # this class is for https://aerospace.org/reentries
    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'postgres'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work

        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        print("creating aero table")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS aero(
                         object text,
                         mission text,
                         reentry_type text,
                         launch_date date,
                         predicted_reentry_date date,
                         norad_num integer,
                         cospar_num text)""")
        # extra line
        #self.connection.commit()

    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            field_names = adapter.field_names()
            for field_name in field_names:
                if field_name is 'predicted_reentry_date':
                    value = adapter.get(field_name)
                    parsed_date = datetime.strptime(value, '%b %d, %Y %H:%M:%S')
                    value = parsed_date.strftime('%-m/%-d/%y')
                    adapter[field_name] = value
            self.cur.execute(
                """insert into aero (object, mission, reentry_type, launch_date, predicted_reentry_date, norad_num, 
                cospar_num) values (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['object'],
                    item['mission'],
                    item['reentry_type'],
                    item['launch_date'],
                    item['predicted_reentry_date'],
                    item['norad_num'],
                    item['cospar_num'],
                ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            # print(f'Error during item processing: {e}')
        return item


class Planet4589Pipeline:
    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'postgres'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work

        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        print("creating orbitalfocus table")
        
        # changed one of the column from primary to primry for obvious reasons
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS planet4589(
                         jcat text,
                         satcat integer,
                         piece text,
                         type text,
                         name text,
                         plname text,
                         ldate date,
                         parent text,
                         sdate text, 
                         primry text,
                         ddate text,
                         status text,
                         dest text,
                         owner text,
                         state text,
                         manufacturer text,
                         bus text,
                         motor text,
                         mass double precision,
                         massflag text,
                         drymass double precision,
                         dryflag text,
                         totmass double precision,
                         totflag text,
                         length double precision,
                         lflag text,
                         diameter double precision,
                         dflag text,
                         span double precision,
                         spanflag text,
                         shape text,
                         odate date,
                         perigee integer,
                         pf text,
                         apogee integer,
                         af text,
                         inc double precision,
                         if text,
                         oporbit text,
                         oqual text,
                         altnames text,
                         data_status integer)""") # check sdate, odate type
        # extra line
        #self.connection.commit()

    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            field_names = adapter.field_names()
            for field_name in field_names:
                if field_name is 'LDate':
                    value = adapter.get(field_name)
                    parsed_date = datetime.strptime(value, '%Y %b %d')
                    value = parsed_date.strftime('%-m/%-d/%y')
                    adapter[field_name] = value
            self.cur.execute(
                """insert into planet4589 (jcat, satcat, piece, type, name, plname, ldate, parent, sdate, primry, 
                ddate, status, dest, owner, state, manufacturer, bus, motor, mass, massflag, drymass, dryflag, 
                totmass, totflag, length, lflag, diameter, dflag, span, spanflag, shape, odate, perigee, pf, apogee, 
                af, inc, if, oporbit, oqual, altnames, data_status) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s)""",
                (
                    item['JCAT'],
                    item['Satcat'],
                    item['Piece'],
                    item['Type'],
                    item['Name'],
                    item['PLName'],
                    item['LDate'],
                    item['Parent'],
                    item['SDate'],
                    item['Primary'],
                    item['DDate'],
                    item['Status'],
                    item['Dest'],
                    item['Owner'],
                    item['State'],
                    item['Manufacturer'],
                    item['Bus'],
                    item['Motor'],
                    item['Mass'],
                    item['MassFlag'],
                    item['DryMass'],
                    item['DryFlag'],
                    item['TotMass'],
                    item['TotFlag'],
                    item['Length'],
                    item['LFlag'],
                    item['Diameter'],
                    item['DFlag'],
                    item['Span'],
                    item['SpanFlag'],
                    item['Shape'],
                    item['ODate'],
                    item['Perigee'],
                    item['PF'],
                    item['Apogee'],
                    item['AF'],
                    item['Inc'],
                    item['IF'],
                    item['OpOrbit'],
                    item['OQUAL'],
                    item['AltNames'],
                    item['data_status']
                ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            # print(f'Error during item processing: {e}')
        return item

class UcsdataPipeleine:

    def __init__(self):
        hostname = 'localhost'  # this will be universal
        username = 'postgres'  # create a new user with name: 'skynetapp'
        password = 'skynet'  # make the password 'skynet' when you create the new user
        # database = 'skynet' # we don't need this for this to work

        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        # changed one of the column from primary to primry for obvious reasons
        print('creating ucs_master table')
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS ucs_master(
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
                        in_geo text,
                        perigee text,
                        apogee text,
                        eccentricity text,
                        inclination text,
                        period text,
                        mass text,
                        dry_mass text,
                        power text,
                        launch_date text,
                        expected_lifetime text,
                        contractor text,
                        contractor_country text,
                        launch_site text,
                        launch_vehicle text,
                        cospar text,
                        norad text,
                        source text,
                        additional_source text,
                        data_status integer)""")
        #self.connection.commit()

        print('creating ucs_master_duplicates table')
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS ucs_master_duplicates (
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
                        in_geo text,
                        perigee text,
                        apogee text,
                        eccentricity text,
                        inclination text,
                        period text,
                        mass text,
                        dry_mass text,
                        power text,
                        launch_date text,
                        expected_lifetime text,
                        contractor text,
                        contractor_country text,
                        launch_site text,
                        launch_vehicle text,
                        cospar text,
                        norad text,
                        source text,
                        additional_source text,
                        data_status integer)""")
        #self.connection.commit()



    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            field_names = adapter.field_names()
            if int(item['data_status']) == 5:
                self.cur.execute(
                    """ insert into ucs_master_duplicates (
                        full_name,
                        official_name,
                        country,
                        owner_country,
                        owner,
                        users,
                        purpose,
                        detail_purpose,
                        orbit_class,
                        orbit_type,
                        in_geo,
                        perigee,
                        apogee,
                        eccentricity,
                        inclination,
                        period,
                        mass,
                        dry_mass,
                        power,
                        launch_date,
                        expected_lifetime,
                        contractor,
                        contractor_country,
                        launch_site,
                        launch_vehicle,
                        cospar,
                        norad,
                        source,
                        additional_source,
                        data_status
                    ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        item['full_name'],
                        item['official_name'],
                        item['country'],
                        item['owner_country'],
                        item['owner'],
                        item['users'],
                        item['purpose'],
                        item['detail_purpose'],
                        item['orbit_class'],
                        item['orbit_type'],
                        item['in_geo'],
                        item['perigee'],
                        item['apogee'],
                        item['eccentricity'],
                        item['inclination'],
                        item['period'],
                        item['mass'],
                        item['dry_mass'],
                        item['power'],
                        item['launch_date'],
                        item['expected_lifetime'],
                        item['contractor'],
                        item['contractor_country'],
                        item['launch_site'],
                        item['launch_vehicle'],
                        item['cospar'],
                        item['norad'],
                        item['source'],
                        item['additional_source'],
                        item['data_status']
                    ))
            else:
                self.cur.execute(
                    """ insert into ucs_master (
                        full_name,
                        official_name,
                        country,
                        owner_country,
                        owner,
                        users,
                        purpose,
                        detail_purpose,
                        orbit_class,
                        orbit_type,
                        in_geo,
                        perigee,
                        apogee,
                        eccentricity,
                        inclination,
                        period,
                        mass,
                        dry_mass,
                        power,
                        launch_date,
                        expected_lifetime,
                        contractor,
                        contractor_country,
                        launch_site,
                        launch_vehicle,
                        cospar,
                        norad,
                        source,
                        additional_source,
                        data_status
                    ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        item['full_name'],
                        item['official_name'],
                        item['country'],
                        item['owner_country'],
                        item['owner'],
                        item['users'],
                        item['purpose'],
                        item['detail_purpose'],
                        item['orbit_class'],
                        item['orbit_type'],
                        item['in_geo'],
                        item['perigee'],
                        item['apogee'],
                        item['eccentricity'],
                        item['inclination'],
                        item['period'],
                        item['mass'],
                        item['dry_mass'],
                        item['power'],
                        item['launch_date'],
                        item['expected_lifetime'],
                        item['contractor'],
                        item['contractor_country'],
                        item['launch_site'],
                        item['launch_vehicle'],
                        item['cospar'],
                        item['norad'],
                        item['source'],
                        item['additional_source'],
                        item['data_status']
                    ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during item processing: {e}')
        return item

class NtwoYOPipeline:
    # this class is for https://www.n2yo.com/database/?q=#results
    def __init__(self):
        hostname = 'localhost' # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet' # make the password 'skynet' when you create the new user
        #database = 'skynet' # we don't need this for this to work
        
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS period(
                         NORAD text,
                         Period text)""")
        
    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()
    
    def process_item(self, item, spider):
        try:
            self.cur.execute("INSERT INTO period (NORAD, Period) VALUES (%s, %s)", (item["NORAD"], item["Period"]))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during item processing: {e}')
        return item

class NanoSatsPipeline:
    # this class is for https://www.nanosats.eu/database
    def __init__(self):
        hostname = 'localhost' # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet' # make the password 'skynet' when you create the new user
        #database = 'skynet' # we don't need this for this to work
        
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS nanosats(
                         NAME text,
                         Type text,
                         Units text,
                         Status text,
                         Launched text,
                         NORAD text,
                         Deployer text,
                         Launcher text,
                         Organization text,
                         Institution text,
                         Entity text,
                         Nation text,
                         Launch_Brokerer text,
                         Partners text,
                         Oneliner text,
                         Description text)""")
        
    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()


    def process_item(self, item, spider):
        try:
            self.cur.execute("""INSERT INTO nanosats VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                                item["Name"],
                                item["Type"],
                                item["Units"],
                                item["Status"],
                                item["Launched"],
                                item["NORAD"],
                                item["Deployer"],
                                item["Launcher"],
                                item["Organisation"],
                                item["Institution"],
                                item["Entity"],
                                item["Nation"],
                                item["Launch_Brokerer"],
                                item["Partners"],
                                item["Oneliner"],
                                item["Description"]
                            ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during item processing: {e}')
        return item
    
class TheSpaceReportPipeline:
    # this class is for https://www.thespacereport.org/resources/launch-log-2023/
    def __init__(self):
        hostname = 'localhost' # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet' # make the password 'skynet' when you create the new user
        #database = 'skynet' # we don't need this for this to work
        
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS data_spacereport (
                         LaunchID text,
                         DateTime text,
                         LaunchVehicle text,
                         OperatorCountry text,
                         LaunchSite text,
                         Status text,
                         MissionSector text,
                         Crewed text,
                         FirstStageRecovery text)
                         """)
        
    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during commit: {e}')
        finally:
            self.cur.close()
            self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute("""INSERT INTO data_spacereport VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                                item["LaunchID"],
                                item["DateTime"],
                                item["LaunchVehicle"],
                                item["OperatorCountry"],
                                item["LaunchSite"],
                                item["Status"],
                                item["MissionSector"],
                                item["Crewed"],
                                item["FirstStageRecovery"]
                            ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f'Error during item processing: {e}')
        return item
