from ._anvil_designer import StartSeiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


from ..BuchungsForm import BuchungsForm
from ..RegistrierungsForm import RegistrierungsForm

class StartSeite(StartSeiteTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Setze Datenquelle der RepeatingPanel-Komponente
        self.repeating_panel_1.items = anvil.server.call('get_all_jugendherbergen')
        
    def button_buchen_click(self, **event_args):
        # Wechsel zur BuchungsForm
        open_form(BuchungsForm())

    def button_registrieren_click(self, **event_args):
        # Wechsel zur RegistrierungsForm
        open_form(RegistrierungsForm())

