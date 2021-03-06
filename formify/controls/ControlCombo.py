from formify.controls import ControlBase
from PySide2 import QtWidgets
import typing

from formify.controls._mixins import ItemMixin


class ControlCombo(ControlBase, ItemMixin):
	def __init__(self,
	             label:str=None,
	             items:list=None,
	             value=None,
				 display_name_callback=str,
	             *args,
	             **kwargs):


		ControlBase.__init__(self,
		                     label,
		                     *args,
		                     **kwargs)

		# normalize items array
		ItemMixin.__init__(self, items, display_name_callback)

		if value is not None:
			self.value = value


	@property
	def index(self) -> int:
		return self.control.currentIndex()


	@index.setter
	def index(self, value: int):
		self.control.setCurrentIndex(value)


	def set_display_names(self, display_names):
		# add items
		self.control.clear()
		self.control.addItems(display_names)


	def _make_control_widget(self) -> typing.Optional[QtWidgets.QWidget]:
		self.control = QtWidgets.QComboBox(parent=self)

		# set the on change handler
		self.control.currentTextChanged.connect(
			lambda: self.change()
		)

		return self.control


	@property
	def value(self):
		item = self.selected_item
		if isinstance(item, tuple) and isinstance(item[1], str):
			try:
				item = item[1]
			except:
				pass
		return item


	@value.setter
	def value(self, value):
		for i, item in enumerate(self._items):
			if item == value:
				self.index = i

