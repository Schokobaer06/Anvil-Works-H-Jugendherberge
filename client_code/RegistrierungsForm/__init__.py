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
          try:
              print("TEST 1")
              anvil.server.call('register_gast', benutzername, passwort, name, adresse, preiskategorie)
              # Automatisch anmelden und zur Startseite weiterleiten
              #anvil.server.call('login', benutzername, passwort)
              #print("TEST 2")
              
              #print("TEST 3")
          except Exception as e:
              alert(f"Fehler bei der Registrierung: {str(e)}")
            
          alert("Registrierung erfolgreich!")
          open_form('StartSeite')
        except Exception as e:
          alert(f"Fehler bei der Registrierung: {str(e)}")
      

    def button_zurueck_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('StartSeite')


