from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #print(anvil.server.call('get_everything',"name"))
    # Any code you write here will run before the form opens.

  def button_registrieren_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Registrieren")

  def button_anmelden_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Anmelden")

