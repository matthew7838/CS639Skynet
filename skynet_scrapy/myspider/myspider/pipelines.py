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
        hostname = 'localhost' # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet' # make the password 'skynet' when you create the new user
        #database = 'skynet' # we don't need this for this to work
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS orbitalfocus(
                         cat_no text,
                         designation text,
                         name text,
                         date text)""")
    
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
            self.cur.execute(""" insert into orbitalfocus (cat_no, designation, name, date) values (%s, %s, %s, %s)""", (
                    item['cat_no'], #norad num
                    item['designation'], # cospar num
                    item['name'],
                    item['date'],
            ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            #print(f'Error during item processing: {e}')
        return item

class Planet4589Pipeline:
    def __init__(self):
        hostname = 'localhost' # this will be universal
        username = 'skynetapp'  # create a new user with name: 'skynetapp'
        password = 'skynet' # make the password 'skynet' when you create the new user
        #database = 'skynet' # we don't need this for this to work

        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()
        # changed one of the column from primary to primry for obvious reasons
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS planet4589(
                         jcat text,
                         satcat text,
                         piece text,
                         type text,
                         name text,
                         plname text,
                         ldate text,
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
                         mass text,
                         massflag text,
                         drymass text,
                         dryflag text,
                         totmass text,
                         totflag text,
                         length text,
                         lflag text,
                         diameter text,
                         dflag text,
                         span text,
                         spanflag text,
                         shape text,
                         odate text,
                         perigee text,
                         pf text,
                         apogee text,
                         af text,
                         inc text,
                         if text,
                         oporbit text,
                         oqual text,
                         altnames text)""")



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
            self.cur.execute(""" insert into planet4589 (jcat, satcat, piece, type, name, plname, ldate, parent, sdate, primry, ddate, status, dest, owner, state, manufacturer, bus, motor, mass, massflag, drymass, dryflag, totmass, totflag, length, lflag, diameter, dflag, span, spanflag, shape, odate, perigee, pf, apogee, af, inc, if, oporbit, oqual, altnames) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
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
                item['AltNames']
            ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            # print(f'Error during item processing: {e}')
        return item


