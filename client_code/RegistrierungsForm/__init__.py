from ._anvil_designer import RegistrierungsFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RegistrierungsForm(RegistrierungsFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Preiskategorien in Dropdown laden
        self.dropdown_preiskategorie.items = anvil.server.call('get_preiskategorien')
    
    def button_registrieren_click(self, **event_args):
        benutzername = self.text_box_benutzername.text
        passwort = self.text_box_passwort.text
        name = self.text_box_name.text
        adresse = self.text_box_adresse.text
        preiskategorie = self.dropdown_preiskategorie.selected_value
        

        if self.text_box_benutzername.text == "" or self.text_box_passwort.text == "":
          alert("Benutzername/Passwort kann nicht leer sein")
          return

        try:
          benutzername_verfuegbar = anvil.server.call('check_benutzername', benutzername)
          if not benutzername_verfuegbar:
              alert("Dieser Benutzername ist bereits vergeben. Bitte wählen Sie einen anderen.")
              return
      
          # Benutzer registrieren
          anvil.server.call('register_gast', benutzername, passwort, name, adresse, preiskategorie)
          alert("Registrierung erfolgreich!")
          open_form('StartSeite')
      
        except Exception as e:
          alert(f"Fehler bei der Registrierung: {str(e)}")

      

    def button_zurueck_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('StartSeite')


