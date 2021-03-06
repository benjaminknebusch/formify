from formify.layout import *
from formify.controls import *
import formify

def change_langauge(sender, language):
	formify.app.translator.language = language

ui = Form(Col(
	ControlCombo("Mode", items=[("de", "Deutsch"), ("en", "English")], variable_name="language", on_change=change_langauge),
	ControlFile(),
))

main_window = formify.MainWindow(ui, margin=8)
