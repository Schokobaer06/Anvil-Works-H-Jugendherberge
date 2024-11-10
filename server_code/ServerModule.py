import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import hashlib

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(data_files['jugendherberge.db'])

# Funktion zur Passwort-Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@anvil.server.callable
def add_sample_data():
    cursor = conn.cursor()

    # Jugendherbergen hinzufügen
    cursor.execute("INSERT INTO Jugendherberge (Name, Ort) VALUES ('Alpenblick', 'München')")
    cursor.execute("INSERT INTO Jugendherberge (Name, Ort) VALUES ('Bergblick', 'Garmisch-Partenkirchen')")
    cursor.execute("INSERT INTO Jugendherberge (Name, Ort) VALUES ('Seeblick', 'Chiemsee')")

    # Preiskategorien hinzufügen
    cursor.execute("INSERT INTO Preiskategorie (Kategorie, Preis) VALUES ('Standard', 25.00)")
    cursor.execute("INSERT INTO Preiskategorie (Kategorie, Preis) VALUES ('Komfort', 40.00)")
    cursor.execute("INSERT INTO Preiskategorie (Kategorie, Preis) VALUES ('Premium', 55.00)")

    # Zimmer hinzufügen
    cursor.execute("INSERT INTO Zimmer (JugendherbergeID, PreiskategorieID, Schlafplaetze) VALUES (1, 1, 4)")
    cursor.execute("INSERT INTO Zimmer (JugendherbergeID, PreiskategorieID, Schlafplaetze) VALUES (1, 2, 2)")
    cursor.execute("INSERT INTO Zimmer (JugendherbergeID, PreiskategorieID, Schlafplaetze) VALUES (2, 1, 4)")
    cursor.execute("INSERT INTO Zimmer (JugendherbergeID, PreiskategorieID, Schlafplaetze) VALUES (3, 3, 2)")

    conn.commit()
    return "Beispieldaten hinzugefügt."

@anvil.server.callable
def register_gast(benutzername, passwort, name, adresse, preiskategorie):
    hashed_password = hash_password(passwort)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Gast (Benutzername, Passwort, Name, Adresse, PreiskategorieID) 
        VALUES (?, ?, ?, ?, ?)
    """, (benutzername, hashed_password, name, adresse, preiskategorie))
    conn.commit()
    return "Gast erfolgreich registriert."

@anvil.server.callable
def login(benutzername, passwort):
    hashed_password = hash_password(passwort)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Gast WHERE Benutzername=? AND Passwort=?", (benutzername, hashed_password))
    return cursor.fetchone() is not None

@anvil.server.callable
def get_all_jugendherbergen():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Jugendherberge")
    jugendherbergen = cursor.fetchall()
    return [{"Name": row[1], "Ort": row[2]} for row in jugendherbergen]

@anvil.server.callable
def get_verfuegbare_zimmer():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT z.ZID, j.Name, p.Kategorie, z.Schlafplaetze 
        FROM Zimmer z
        JOIN Jugendherberge j ON z.JugendherbergeID = j.JID
        JOIN Preiskategorie p ON z.PreiskategorieID = p.PID
    """)
    zimmer = cursor.fetchall()

    # Debug-Ausgabe, um sicherzustellen, dass die Zimmerdaten abgerufen werden
    #print("Verfügbare Zimmer: ", zimmer)
    
    return [
        {
            "ZID": row[0],
            "Jugendherberge": row[1],
            "Preiskategorie": row[2],
            "Schlafplaetze": row[3]
        } for row in zimmer
    ]

#@anvil.server.callable
#def get_logged_in_user_id():
#    user = anvil.users.get_user()
#    if user:
#        return user['GID']  # Dies sollte der Primärschlüssel des Benutzers sein, abhängig von der Benennung der Tabelle 'Gast'
#    else:
#        return None
@anvil.server.callable
def get_logged_in_user_id():
    return anvil.server.session.get('user_id', None)

@anvil.server.callable
def create_booking(gast_id, zimmer_id, datum):
    cursor = conn.cursor()

    # Füge eine neue Buchung zur Tabelle hinzu
    cursor.execute("""
        INSERT INTO Buchung (GastID, ZimmerID, Datum)
        VALUES (?, ?, ?)
    """, (gast_id, zimmer_id, datum))
    
    # Änderungen speichern
    conn.commit()
    return "Buchung erfolgreich erstellt."

@anvil.server.callable
def get_preiskategorien():
    #conn = anvil.server.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT PID, Kategorie FROM Preiskategorie")
    preiskategorien = cursor.fetchall()
    conn.close()
    return [(row[1], row[0]) for row in preiskategorien]
# Beispiel-Daten hinzufügen, wenn die Funktion manuell aufgerufen wird
add_sample_data()

