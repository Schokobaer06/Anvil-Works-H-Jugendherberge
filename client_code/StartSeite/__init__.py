from ._anvil_designer import StartSeiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


from ..BuchungsForm import BuchungsForm
from ..RegistrierungsForm import RegistrierungsForm
from ..LoginForm import LoginForm

class StartSeite(StartSeiteTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Registrieren- und Anmelde-Button hinzufügen
        self.button_registrieren.set_event_handler('click', self.button_registrieren_click)
        self.button_anmelden.set_event_handler('click', self.button_anmelden_click)
        self.button_buchen.set_event_handler('click', self.button_buchen_click)

        # Aktuelle Buchung aus der Session abrufen und anzeigen
        try:
            aktuelle_buchung = anvil.server.call('get_current_booking')
            if aktuelle_buchung:
                self.label_aktuelle_buchung.text = f"Aktuelles Zimmer: Zimmer-ID {aktuelle_buchung['zimmer_id']} am {aktuelle_buchung['datum']}"
            else:
                self.label_aktuelle_buchung.text = "Keine aktuelle Buchung vorhanden."
        except anvil.server.NoServerFunctionError:
            self.label_aktuelle_buchung.text = "Keine aktuelle Buchung vorhanden."

    def button_registrieren_click(self, **event_args):
        # Weiterleitung zur RegistrierungsForm
        open_form(RegistrierungsForm())

    def button_anmelden_click(self, **event_args):
        # Weiterleitung zur LoginForm
        open_form(LoginForm())

    def button_buchen_click(self, **event_args):
        # Zur BuchungsForm wechseln, wenn der Benutzer angemeldet ist
        gast_id = anvil.server.call('get_logged_in_user_id')
        if gast_id:
            open_form('BuchungsForm')
        else:
            alert("Bitte melden Sie sich zuerst an.")


