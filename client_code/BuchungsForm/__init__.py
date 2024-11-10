from ._anvil_designer import BuchungsFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class BuchungsForm(BuchungsFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Verfügbare Zimmer abrufen und in der RepeatingPanel-Komponente anzeigen
        zimmer_liste = anvil.server.call('get_verfuegbare_zimmer')
        user = anvil.users.login_with_form()
        #print("Debug - Verfügbare Zimmer: ", zimmer_liste)  # Debug-Ausgabe für verfügbare Zimmer

        if zimmer_liste:
            # Setze Items für das RepeatingPanel
            self.repeating_panel_zimmer.items = zimmer_liste
            
            # Fülle das Dropdown-Menü mit den Zimmern (ID als value und Name zur Anzeige)
            self.drop_down_zimmer.items = [(f"{zimmer['Jugendherberge']} - {zimmer['Preiskategorie']} ({zimmer['Schlafplaetze']} Schlafplätze)", zimmer['ZID']) for zimmer in zimmer_liste]
        else:
            alert("Keine Zimmer verfügbar.")
    def button_buchen_click(self, **event_args):
      # Überprüfen, ob der Benutzer ein Zimmer und ein Datum ausgewählt hat
      zimmer_id = self.drop_down_zimmer.selected_value
      datum = self.date_picker_datum.date
  
      if not zimmer_id:
          alert("Bitte wählen Sie ein Zimmer aus.")
          return
  
      if not datum:
          alert("Bitte wählen Sie ein Datum für die Buchung aus.")
          return
  
      # Hole die ID des angemeldeten Benutzers
      gast_id = anvil.server.call('get_logged_in_user_id')
      
      if not gast_id:
          alert("Bitte melden Sie sich zuerst an.")
          return
      
      # Buchung im Servermodul erstellen
      try:
          anvil.server.call('create_booking', gast_id, zimmer_id, datum)
          alert("Buchung erfolgreich abgeschlossen!")
      except Exception as e:
          alert(f"Fehler bei der Buchung: {str(e)}")

    



