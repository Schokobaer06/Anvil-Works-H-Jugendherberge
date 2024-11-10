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
        
        anvil.server.call('register_gast', benutzername, passwort, name, adresse, preiskategorie)
        alert("Registrierung erfolgreich!")

