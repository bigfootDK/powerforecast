import pandas
import os
from sqlalchemy import create_engine

files = os.listdir('eisman')

columns = ['anlageschl',
           'einsatz_id',
           'projektnummer',
           'dso_schluessel',
           'netzbetreiber_iln_nummer',
           'datum_regelung_ab',
           'uhrzeit_regelung_ab',
           'datum_regelung_bis',
           'uhrzeit_regelung_bis',
           'regelstufe_einspeisermanagement',
           'entschaedigungspflichtig',
           'ursache',
           'ort',
           'anforderer_iln_nummer']

df = pandas.DataFrame()
for f in files:
    x = pandas.read_csv('eisman/'+f, sep=';', encoding='ISO-8859-1', dtype=str,
                        names=columns)
    df = df.append(x)

plants = pandas.read_csv('renewable_power_plants_SH.csv', dtype=str)

df = pandas.merge(df, plants, how='left', left_on='anlageschl',
                  right_on='eeg_id')

# remove entries without matching geo data
df = df[pandas.notnull(df.lon)]

df['datetime_ab'] = df.datum_regelung_ab.str.cat(df.uhrzeit_regelung_ab, sep=' ')
df['datetime_bis'] = df.datum_regelung_bis.str.cat(df.uhrzeit_regelung_bis, sep=' ')

df.datetime_ab= pandas.to_datetime(df.datetime_ab, format='%d.%m.%Y %H:%M:%S')
df.datetime_bis= pandas.to_datetime(df.datetime_bis, format='%d.%m.%Y %H:%M:%S')

for c in [ 'datum_regelung_ab', 'uhrzeit_regelung_ab', 'datum_regelung_bis',
           'uhrzeit_regelung_bis']:
    del df[c]

df.to_csv('eisman.csv', index=False)

engine = create_engine('sqlite:///powerforecast.db')

sql = ['''
        CREATE TABLE eisman (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                anlageschl TEXT, 
                einsatz_id TEXT, 
                projektnummer TEXT, 
                dso_schluessel TEXT, 
                netzbetreiber_iln_nummer TEXT, 
                datetime_ab TEXT,
                datetime_bis TEXT, 
                regelstufe_einspeisermanagement TEXT, 
                entschaedigungspflichtig TEXT, 
                ursache TEXT, 
                ort TEXT, 
                anforderer_iln_nummer TEXT, 
                commissioning_date TEXT, 
                decommissioning_date TEXT, 
                energy_source_level_1 TEXT, 
                energy_source_level_2 TEXT, 
                energy_source_level_3 TEXT, 
                technology TEXT, 
                electrical_capacity TEXT, 
                thermal_capacity TEXT, 
                voltage_level TEXT, 
                tso TEXT, 
                dso TEXT, 
                dso_id TEXT, 
                eeg_id TEXT, 
                bnetza_id TEXT, 
                federal_state TEXT, 
                postcode TEXT, 
                municipality_code TEXT, 
                municipality TEXT, 
                address TEXT, 
                address_number TEXT, 
                utm_zone TEXT, 
                utm_east TEXT, 
                utm_north TEXT, 
                lat TEXT, 
                lon TEXT, 
                data_source TEXT, 
                comment TEXT
                );''',
        'CREATE INDEX ix_eisman_id ON eisman (id);',
        'CREATE INDEX ix_eisman_datetime_ab ON eisman (datetime_ab);',
        'CREATE INDEX ix_eisman_datetime_bis ON eisman (datetime_bis);']

connection = engine.connect()
for s in sql:
    connection.execute(s)

df.to_sql('eisman', engine, index=False, if_exists='append')
