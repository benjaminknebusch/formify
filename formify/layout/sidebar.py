from PySide2 import QtWidgets, QtCore
import typing
from formify.controls import ControlButton
from formify.controls._mixins import ItemMixin
from formify.controls._events import EventDispatcher

class Sidebar(QtWidgets.QFrame, ItemMixin):
	def __init__(self, items):
		QtWidgets.QFrame.__init__(self)
		self.buttons: typing.List[QtWidgets.QPushButton] = []
		self._make_layout()

		# index change events
		self.index_change = EventDispatcher(self)
		self.index_change.subscribe(self._update_checked_states)

		self._index = -1
		ItemMixin.__init__(self, items)
		self.index = 0


	def _make_button(self, text):
		def make_set_checked(idx):
			def wrapped():
				self.index = idx
			return wrapped

		btn = ControlButton(text)
		self.buttons.append(btn)
		btn.setCheckable(True)
		btn.on_click = make_set_checked(len(self.buttons) - 1)
		self.layout().addWidget(btn)
		return btn


	def _make_layout(self):
		# make layout
		layout = QtWidgets.QVBoxLayout()
		layout.setAlignment(QtCore.Qt.AlignTop)
		layout.setMargin(0)
		self.setLayout(layout)


	def _update_checked_states(self):
		# set checked state on Push Buttons
		for i, btn in enumerate(self.buttons):
			btn.setChecked(i == self._index)


	@property
	def index(self) -> int:
		return self._index


	@index.setter
	def index(self, value: int):
		if value == self._index:
			self._update_checked_states()
			return
		self._index = value
		# cause event
		self.index_change(value)


	def set_display_names(self, display_names):
		def ensure_number_buttons(n):
			if n == len(self.buttons):
				return
			while n < len(self.buttons):
				self.buttons[-1].destroy()
				del self.buttons[-1]
			while n > len(self.buttons):
				self._make_button("")

		ensure_number_buttons(len(display_names))
		for i, name in enumerate(display_names):
			self.buttons[i].setText(name)



class SidebarLight(Sidebar):
	pass