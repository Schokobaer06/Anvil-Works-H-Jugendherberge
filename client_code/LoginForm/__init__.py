from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#from ..StartSeite import StartSeite

class LoginForm(LoginFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
    def button_login_click(self, **event_args):
        benutzername = self.text_box_benutzername.text
        passwort = self.text_box_passwort.text
        login_successful = anvil.server.call('login', benutzername, passwort)
        
      
        if login_successful is not None:
            alert("Anmeldung erfolgreich!")
            #print("DEBUG: ANMELDUNG erfolgreich")
            open_form('StartSeite')
        else:
            alert("Login fehlgeschlagen. Bitte prüfen Sie Ihre Anmeldedaten.")

    def button_zurueck_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('StartSeite')

