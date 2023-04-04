from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
import json
import pandas as pd
import sqlite3 as sql
import numpy as np
#def create_app():
#  app = Flask(__name__)
#  app.secret_key = "mykeyisbad"
#  Bootstrap(app)

#  return app

app = Flask(__name__)
app.secret_key = "Ma863187"









#DB Verbindung aufbauen
#conn = sql.connect('Website.db')

# Read data from your prepared example .csv-file into a dataframe (define seperator)
#carinsurance_df = pd.read_csv("car_insurance_claim.csv", delimiter=';', header=None, skiprows=1, names=['ID','KIDSDRIV','AGE','HOMEKIDS','YOJ','INCOME_USD','PARENT1','HOME_VAL_USD','MSTATUS','GENDER','EDUCATION','OCCUPATION','TRAVTIME','CAR_USE','BLUEBOOK_USD','TIF','CAR_TYPE','RED_CAR','OLDCLAIM_USD','CLM_FREQ','REVOKED','MVR_PTS','CLM_AMT_USD','CAR_AGE','CLAIM_FLAG','URBANICITY'], index_col=False)
#carinsurance_df

#carinsurance_df.info()



#df_read = pd.read_sql("SELECT * FROM carinsurance_tbl as T1 INNER JOIN carinsurance_car_types_tbl as T2 ON T1.CAR_TYPE = T2.CAR_TYPE WHERE T2.ID = 4", con=conn)

#df_read_Gemeindeporträt = pd.read_sql("SELECT * FROM Gemeindeporträt_tbl", con=conn)
#df_read_Einwohner_Flawil = pd.read_sql("SELECT Einwohner FROM Gemeindeporträt_tbl WHERE Gemeindename= 'Flawil'", con=conn)
#df_read_Einwohner_Greifensee = pd.read_sql("SELECT Einwohner FROM Gemeindeporträt_tbl WHERE Gemeindename= 'Greifensee'", con=conn)


#conn.close()



@app.route("/hello")
def index():
	flash("")
	return render_template("index.html")

@app.route("/greet", methods=["POST", "GET"])
def greet():

	Eingabe = request.form['name_input']


		#Anzahl Ladestationen aus json File extrahieren
	cities = []

	f = open('Ladestationen.json')
	data = json.load(f)
	for record in data['EVSEData']:
	    for line in record['EVSEDataRecord']:
	        if 'Address' in line:
	            if 'City' in line['Address']:
	                cities.append(line['Address']['City'])

		#DB Verbindung aufbauen und Beste Gemeinde desselben Gemeindetyps wie die der Variable Eingabe rausholen
	conn = sql.connect('Website.db')
	cursor= conn.cursor()
	
	data_Gemeindetyp=cursor.execute("SELECT GdeTypologieg FROM Raumgliederungen_tbl WHERE Gemeindename='%s'" % Eingabe).fetchone()
	
	df_listeGemeindenachGemeindetyp=cursor.execute("SELECT Gemeindename FROM Raumgliederungen_tbl WHERE GdeTypologieg='%s'" % data_Gemeindetyp).fetchall()

	conn.close()

	# Konvertiere die Sucheinträge in eine Liste von Strings
	search_strings = [value[0] for value in df_listeGemeindenachGemeindetyp]

	# Durchsuche die Liste nach den Suchbegriffen und zähle, wie oft sie vorkommen
	counts = {value: cities.count(value) for value in search_strings}

	# Finde den Suchbegriff mit der höchsten Anzahl an Treffern
	besteGemeinde = max(counts, key=counts.get)





	data_Anzahlladestationen = 0

	# Schleife durchläuft den Array und prüft jeden Wert auf Gleichheit mit der Variable Eingabe
	for ort in cities:
	    if ort == Eingabe:
	        data_Anzahlladestationen += 1

	besteAnzahlladestationen = 0

	for ort in cities:
	    if ort == besteGemeinde:
	        besteAnzahlladestationen += 1



	conn = sql.connect('Website.db')
	cursor= conn.cursor()

	data_Einwohner=cursor.execute("SELECT Einwohner FROM Gemeindeporträt_tbl WHERE Gemeindename='%s'" % Eingabe).fetchone()
	data_Gemeindetyp=cursor.execute("SELECT GdeTypologieg FROM Raumgliederungen_tbl WHERE Gemeindename='%s'" % Eingabe).fetchone()
	data_Beschäftigtetotal=cursor.execute("SELECT Beschäftigte_total FROM Gemeindeporträt_tbl WHERE Gemeindename='%s'" % Eingabe).fetchone()
	data_FahrzeugeproGemeinde=cursor.execute("SELECT SUMME FROM FahrzeugeproGemeinde_tbl WHERE Gemeinde LIKE ? AND Treibstoff = 'Ohne Motor'", ('%' + Eingabe,)).fetchone()
	data_BEVproGemeinde=cursor.execute("SELECT Bestand2022 FROM FahrzeugeproGemeinde_tbl WHERE Gemeinde LIKE ? AND Treibstoff = 'Elektrisch'", ('%' + Eingabe,)).fetchone()
	data_Gemeindecode=cursor.execute("SELECT Gemeindecode FROM Gemeindeporträt_tbl WHERE Gemeindename = '%s'" % Eingabe).fetchone()

	besteEinwohner=cursor.execute("SELECT Einwohner FROM Gemeindeporträt_tbl WHERE Gemeindename='%s'" % besteGemeinde).fetchone()
	besteGemeindetyp=cursor.execute("SELECT GdeTypologieg FROM Raumgliederungen_tbl WHERE Gemeindename='%s'" % besteGemeinde).fetchone()
	besteBeschäftigtetotal=cursor.execute("SELECT Beschäftigte_total FROM Gemeindeporträt_tbl WHERE Gemeindename='%s'" % besteGemeinde).fetchone()
	besteFahrzeugeproGemeinde=cursor.execute("SELECT SUMME FROM FahrzeugeproGemeinde_tbl WHERE Gemeinde LIKE ? AND Treibstoff = 'Ohne Motor'", ('%' + besteGemeinde,)).fetchone()
	besteBEVproGemeinde=cursor.execute("SELECT Bestand2022 FROM FahrzeugeproGemeinde_tbl WHERE Gemeinde LIKE ? AND Treibstoff = 'Elektrisch'", ('%' + besteGemeinde,)).fetchone()
	besteGemeindecode=cursor.execute("SELECT Gemeindecode FROM Gemeindeporträt_tbl WHERE Gemeindename = '%s'" % besteGemeinde).fetchone()

	conn.close()

	

	data_Einwohner=int(data_Einwohner[0])
	data_Gemeindetyp=int(data_Gemeindetyp[0])
	data_Beschäftigtetotal=int(data_Beschäftigtetotal[0])

	data_FahrzeugeproGemeinde = int(data_FahrzeugeproGemeinde[0])
	data_BEVproGemeinde = int(data_BEVproGemeinde[0])
	data_Gemeindecode = int(data_Gemeindecode[0])

	data_Personenwagenschweiz = 4721280
	data_Bevölkerungszahlschweiz = 8703000
	data_Bestandelektroautos = 110751


	besteEinwohner=int(besteEinwohner[0])
	besteGemeindetyp=int(besteGemeindetyp[0])
	besteBeschäftigtetotal=int(besteBeschäftigtetotal[0])

	besteFahrzeugeproGemeinde=int(besteFahrzeugeproGemeinde[0])
	besteBEVproGemeinde=int(besteBEVproGemeinde[0])
	besteGemeindecode = int(besteGemeindecode[0])


	LPpro1000BEV = round(data_Anzahlladestationen/(data_BEVproGemeinde/1000),2)
	LPpro1000Fahrzeuge = round(data_Anzahlladestationen/(data_FahrzeugeproGemeinde/1000),2)
	LPpro1000Einwohner = round(data_Anzahlladestationen/(data_Einwohner/1000),2)
	FahrzeugeproLP = round(data_FahrzeugeproGemeinde/data_Anzahlladestationen,2)
	BEVproLP = round((data_BEVproGemeinde)/data_Anzahlladestationen,2)
	EinwohnerproLP = round((data_Einwohner)/data_Anzahlladestationen,2)

	besteLPpro1000BEV = round(besteAnzahlladestationen/(besteBEVproGemeinde/1000),2)
	besteLPpro1000Fahrzeuge = round(besteAnzahlladestationen/(besteFahrzeugeproGemeinde/1000),2)
	besteLPpro1000Einwohner = round(besteAnzahlladestationen/(besteEinwohner/1000),2)
	besteFahrzeugeproLP = round(besteFahrzeugeproGemeinde/besteAnzahlladestationen,2)
	besteBEVproLP = round(besteBEVproGemeinde/besteAnzahlladestationen,2)
	besteEinwohnerproLP = round(besteEinwohner/besteAnzahlladestationen,2)







	flash("Gemeinde: " + str(request.form['name_input']), 'Eingabeheader')
	flash("Gemeindetyp:  " + str(data_Gemeindetyp), 'EingabeGemeinde1')
	flash("Einwohner:  " + str(data_Einwohner), 'EingabeGemeinde1')
	flash("Berufstätige:  " + str(data_Beschäftigtetotal), 'EingabeGemeinde1')
	flash("Ladepunkte:  " + str(data_Anzahlladestationen), 'EingabeGemeinde1')
	flash("Zugelassene Elektrofahrzeuge:  " + str(data_BEVproGemeinde), 'EingabeGemeinde1')
	flash("Zugelassene Fahrzeuge:  " + str(data_FahrzeugeproGemeinde), 'EingabeGemeinde1')


	flash("Einwohner pro Ladepunkt: " +str(EinwohnerproLP), 'EingabeGemeinde2')
	flash("Fahrzeuge pro Ladepunkt: " +str(FahrzeugeproLP), 'EingabeGemeinde2')
	flash("Elektrofahrzeuge pro Ladepunkt: " +str(BEVproLP), 'EingabeGemeinde2')
	flash("Ladepunkte pro 1000 Einwohner: " +str(LPpro1000Einwohner), 'EingabeGemeinde2')
	flash("Ladepunkte pro 1000 Elektrofahrzeuge: " +str(besteLPpro1000Fahrzeuge), 'EingabeGemeinde2')
	flash("Ladepunkte pro 1000 Fahrzeuge: " +str(LPpro1000BEV), 'EingabeGemeinde2')



	flash("  Gemeinde mit den meisten Ladepunkten (Gemeindetyp " + str(besteGemeindetyp) + ")" + ": " + str(besteGemeinde), 'Besteheader')
	flash("Gemeindetyp:  " + str(besteGemeindetyp), 'BesteGemeinde1')
	flash("Einwohner:  " + str(besteEinwohner), 'BesteGemeinde1')
	flash("Berufstätige:  " + str(besteBeschäftigtetotal), 'BesteGemeinde1')
	flash("Ladepunkte:  " + str(besteAnzahlladestationen), 'BesteGemeinde1')
	flash("Zugelassene Elektrofahrzeuge:  " + str(besteBEVproGemeinde), 'BesteGemeinde1')
	flash("Zugelassene Fahrzeuge:  " + str(besteFahrzeugeproGemeinde), 'BesteGemeinde1')


	flash("Einwohner pro Ladepunkt: " +str(besteEinwohnerproLP), 'BesteGemeinde2')
	flash("Fahrzeuge pro Ladepunkt: " +str(besteFahrzeugeproLP), 'BesteGemeinde2')
	flash("Elektrofahrzeuge pro Ladepunkt: " +str(besteBEVproLP), 'BesteGemeinde2')
	flash("Ladestationen pro 1000 Einwohner: " +str(besteLPpro1000Einwohner), 'BesteGemeinde2')
	flash("Ladestationen pro 1000 Elektrofahrzeuge: " +str(besteLPpro1000Fahrzeuge), 'BesteGemeinde2')
	flash("Ladestationen pro 1000 Fahrzeuge: " +str(besteLPpro1000BEV), 'BesteGemeinde2')









	coordinates = []

	f = open('Ladestationen.json')
	data = json.load(f)
	for record in data['EVSEData']:
	    for line in record['EVSEDataRecord']:
	        if 'GeoCoordinates' in line:
	            if 'Google' in line['GeoCoordinates']:
	                coordinates.append(line['GeoCoordinates']['Google'])



	index = cities.index(Eingabe)
	x=coordinates[index]
	print(type(x))
	if type(x) == list:
	    latitude, longitude = x[0].split()
	else:
	    latitude, longitude = x.split()

	latitude = float(latitude)
	longitude = float(longitude)


	from pyproj import Transformer
	transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056")
	easting, northing = transformer.transform(latitude, longitude)


	url = 'https://map.geo.admin.ch/embed.html?lang=de&topic=energie&bgLayer=ch.swisstopo.pixelkarte-grau&zoom=6&layers=ch.bfe.ladestellen-elektromobilitaet&catalogNodes=2419,2420,2427,2480,2429,2431,2434,2436,2767,2441,3206&E=2732550.85&N=1252120.21'
	url = url.replace('N=1252120.21', f'N={northing}').replace('E=2732550.85', f'E={easting}')


	flash(str("Übersichtskarte Ladestationen der Gemeinde " + str(Eingabe)), 'HeaderKarte')
	flash(str(url), 'Karte')


	


	
	urlElCom = 'https://www.strompreis.elcom.admin.ch/municipality/3402?municipality=6136'
	urlElCom = urlElCom.replace('/3402', f'/{data_Gemeindecode}').replace('municipality=6136', f'municipality={besteGemeindecode}')

	flash(str("Strompreisvergleich der Gemeinden  " + str(Eingabe) + " und " + str(besteGemeinde) + " (Indikator für Betriebskosten)"), 'HeaderStrompreise')
	flash(str(urlElCom), 'Strompreise')

	return render_template("index.html")
#	@app.route('/', methods=['GET', 'POST'])
#def index():
#    if request.method == 'POST':
#        user_input = request.form['input-field']
#        print('Benutzereingabe:', user_input)
#    return '''
#        <form method="post">
#            <input type="text" id="input-field" name="input-field" placeholder="Geben Sie hier Ihren Text ein">
#            <input type="submit" value="Absenden">
#        </form>
#    '''
