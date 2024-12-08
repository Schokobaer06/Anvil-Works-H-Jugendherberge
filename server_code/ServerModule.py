import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import hashlib
from datetime import date

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(data_files['jugendherberge.db'])
#isSet = None
# Funktion zur Passwort-Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@anvil.server.callable
def add_sample_data():
      cursor = conn.cursor()
      cursor.execute("SELECT COUNT(*) FROM Jugendherberge")
      if cursor.fetchone()[0] > 0:
        return "Daten sind bereits vorhanden."
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
    print(f"DEBUG: Benutzername={benutzername}, Passwort={hashed_password}, Name={name}, Adresse={adresse}, Preiskategorie={preiskategorie}")
    cursor = conn.cursor()
    kategorie = get_preiskategorieID(preiskategorie)
    print(f"DEBUG: Kategorie-ID={kategorie}")
    cursor.execute("""
        INSERT INTO Gast (Benutzername, Passwort, Name, Adresse, PreiskategorieID,RegistrierungDatum) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (benutzername, hashed_password, name, adresse, kategorie, date.today()))
    
    
    conn.commit()
    return "Gast erfolgreich registriert."

@anvil.server.callable
def login(benutzername, passwort):
    hashed_password = hash_password(passwort)
    cursor = conn.cursor()
    cursor.execute("SELECT GID FROM Gast WHERE Benutzername=? AND Passwort=?", (benutzername, hashed_password))
    result = cursor.fetchone()
    if result:
      anvil.server.session['user_id'] = result[0]
    return result[0] if result else None

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
    print("DEBUG: Verfügbare Zimmer: ", zimmer)
    
    return [
        {
            "ZID": row[0],
            "Jugendherberge": row[1],
            "Preiskategorie": row[2],
            "Schlafplaetze": row[3]
        } for row in zimmer
    ]


@anvil.server.callable
def get_verfuegbare_gaeste():
  cursor = conn.cursor()
  cursor.execute("SELECT Benutzername, Passwort, Name, RegistrierungDatum, PreiskategorieID from Gast")
  result = cursor.fetchall()
  return str([{f"""Username: {row[0]}
  Passwort: {row[1]}
  Name:{row[2]}
  RegistrierungDatum: {row[3]}
  PreiskategorieID: {row[4]}
  """} for row in result])
  
  
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
    cursor.execute("SELECT PID, Kategorie, Preis FROM Preiskategorie")
    preiskategorien = cursor.fetchall()
    conn.close()
    return [(row[1]) for row in preiskategorien]
# Beispiel-Daten hinzufügen, wenn die Funktion manuell aufgerufen wird
#add_sample_data()
@anvil.server.callable
def get_preiskategorieID(kategorie):
    #conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT PID FROM Preiskategorie WHERE Kategorie = ?", (kategorie,))
    result = cursor.fetchone()
    #conn.close()
    if not result:
        raise ValueError(f"Preiskategorie '{kategorie}' nicht gefunden.")
    return result[0]
  

@anvil.server.callable
def delete_all_entries():
    cursor = conn.cursor()

    # Tabellen mit Namen (ersetzen Sie die Tabellen mit Ihren Namen)
    tabellen = ["Preiskategorie", "Zimmer", "Jugendherberge", "Gast", "Buchung", "BuchtMit"]
    #, "Gast", "Buchung", "BuchtMit"
    for tabelle in tabellen:
        cursor.execute(f"DELETE FROM {tabelle}")
        print(f"Alle Einträge aus der Tabelle {tabelle} wurden gelöscht.")
    
    conn.commit()
    conn.close()
    return "Alle Tabellen wurden geleert."

@anvil.server.callable
def get_current_user():
    gid = get_logged_in_user_id()  # Hol die Benutzer-ID aus der Session
    if not gid:
        return None  # Kein Benutzer eingeloggt

    cursor = conn.cursor()

    # Erste Abfrage: Gastinformationen abrufen
    cursor.execute(
        "SELECT Benutzername, Name, Adresse, RegistrierungDatum, PreiskategorieID FROM Gast WHERE GID = ?",
        (gid,)
    )
    result1 = cursor.fetchone()

    if result1 and len(result1) >= 5:
        print("DEBUG: result1 funktioniert")
        preiskategorie_id = result1[4]

        # Zweite Abfrage: Preiskategorie abrufen
        cursor.execute(
            "SELECT Kategorie, Preis FROM Preiskategorie WHERE PID = ?",
            (preiskategorie_id,)
        )
        result2 = cursor.fetchone()

        if result2:
            print("DEBUG: result2 funktioniert")
            # Daten zusammenfügen und zurückgeben
            return (
                f"Username: {result1[0]} | Name: {result1[1]} | Adresse: {result1[2]} | "
                f"Registrierungsdatum: {result1[3]} | Kategorie: {result2[0]} ({result2[1]}€)"
            )
        else:
            print("DEBUG: Keine Preiskategorie gefunden")
            return f"Username: {result1[0]} | Name: {result1[1]} | Adresse: {result1[2]} | Registrierungsdatum: {result1[3]} | Kategorie: Unbekannt"
    else:
        print("DEBUG: Kein Benutzer gefunden")
        return None
      
@anvil.server.callable
def debug_check_zimmer():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Zimmer")
    zimmer = cursor.fetchall()
    print("DEBUG: Zimmer-Inhalt: ", zimmer)
    return zimmer

@anvil.server.callable
def debug_check_foreign_keys():
    cursor = conn.cursor()

    # Check Jugendherberge
    cursor.execute("SELECT * FROM Jugendherberge")
    jugendherbergen = cursor.fetchall()
    print("DEBUG: Jugendherberge-Inhalt: ", jugendherbergen)
    
    # Check Preiskategorie
    cursor.execute("SELECT * FROM Preiskategorie")
    preiskategorien = cursor.fetchall()
    print("DEBUG: Preiskategorie-Inhalt: ", preiskategorien)

    # Check Zimmer
    cursor.execute("SELECT * FROM Zimmer")
    zimmer = cursor.fetchall()
    print("DEBUG: Zimmer-Inhalt: ", zimmer)
    
    return {
        "Jugendherberge": [row[0] for row in jugendherbergen],
        "Preiskategorie": [row[0] for row in preiskategorien],
        "Zimmer": [row[0] for row in zimmer]
    }
  
@anvil.server.callable
def debug_get_buchung():
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Buchung")
  result = cursor.fetchall()
  if result:
    return result

@anvil.server.callable
def get_current_booking():
    # Überprüfen, ob ein Benutzer eingeloggt ist
    gast_id = get_logged_in_user_id()
    if not gast_id:
        return None  # Kein Benutzer eingeloggt

    cursor = conn.cursor()

    # Abrufen der neuesten Buchung des Benutzers
    cursor.execute("""
        SELECT b.BID, b.ZimmerID, b.Datum, z.JugendherbergeID, j.Name AS Jugendherberge, z.PreiskategorieID, p.Kategorie
        FROM Buchung b
        JOIN Zimmer z ON b.ZimmerID = z.ZID
        JOIN Jugendherberge j ON z.JugendherbergeID = j.JID
        JOIN Preiskategorie p ON z.PreiskategorieID = p.PID
        WHERE b.GastID = ?
        ORDER BY b.Datum DESC
        LIMIT 1
    """, (gast_id,))
    result = cursor.fetchone()

    if result:
        # Rückgabe der aktuellen Buchung mit Details
        return {
            "buchung_id": result[0],
            "zimmer_id": result[1],
            "datum": result[2],
            "jugendherberge": result[4],
            "preiskategorie": result[6]
        }
    else:
        return None  # Keine Buchung gefunden

@anvil.server.callable
def check_benutzername(username):
  cursor = conn.cursor()
  cursor.execute("SELECT GID FROM Gast WHERE Benutzername = ?",(username,))
  result = cursor.fetchone()
  return result is None

@anvil.server.callable
def get_all_users():
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Gast")
  result = cursor.fetchall()
  return result 

@anvil.server.callable
def get_connection():
    return sqlite3.connect('jugendherberge.db')

@anvil.server.callable
def abmelden():
    if 'user_id' in anvil.server.session:
      del anvil.server.session['user_id']
    return "Benutzer wurde abgemeldet."
  

