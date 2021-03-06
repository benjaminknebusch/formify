from formify.controls import *
from formify.layout import *
import formify

table_bh = ControlTable(
	label="B(H)-Curve",
	columns=["H in A/m", "B in T"],
	column_types=[float, float],
	variable_name="bh"
)
plot = ControlMatplotlib()

def _draw_bh():
	fig = plot.fig
	fig.clf()
	ax = fig.gca()

	import numpy as np
	bh = np.array(table_bh.value).T
	if len(bh) > 1:
		ax.plot(bh[0], bh[1])

	plot.draw()

draw_bh = formify.tools.BackgroundMethod(_draw_bh)
table_bh.change.subscribe(draw_bh)

a = """
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor 
invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam 
et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est
Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam 
nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At 
vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea 
takimata sanctus est Lorem ipsum dolor sit amet.
"""

def set_title(sender, value):
	window.title = value


def maybe_boop():
	if formify.tools.ok_dialog():
		print("Boop")

material_form = Form(Row(
	Col(
		Segment(
			h3("General Properties"),
			ControlText("Name", variable_name="name", on_change=set_title),
			ControlButton("Boop?", on_click=maybe_boop),
			Row(
				ControlFloatMega("Conductivity in MS", variable_name="conductivity"),
				ControlFloat("Temperature in °C", variable_name="temperature"),
			),

			h3("Magnetization"),
			ControlDiff("Diff", value=(a.split("\n"), a.replace("nonumy", "nonasy").split("\n"))),
			ConditionalForm({
				"linear": ControlFloat("Relative permeability", variable_name="mur"),
				"non-linear": Row(
					table_bh,
					plot,
				),
			}, variable_name="__flatten__"),
		),
	)
), variable_name="material")

material_form.change.subscribe(lambda : print(material_form.all_values))

import math
voltage = ControlFloat("Verkettete Spannung in V", variable_name="phase_voltage")
voltage_str = ControlFloat("Strangspannung in V")
formify.tools.Relationship(
	(voltage, lambda : voltage_str.value * math.sqrt(3)),
	(voltage_str, lambda : voltage.value / math.sqrt(3))
)

image = ControlImage("nyan_cat.png")
def set_image_width(w):
	image.width = w

sidebar = SidebarContentView({
	"General": SplitterCol(
		voltage,
		voltage_str,
		ControlFloat("Image Width", on_change=lambda _, w: set_image_width(w)),
		image,
		Row(
			ControlList("Drag'n drop", items=["A", "B", "C", "D", "E", "F", "G"]),
			ControlList("2nd List", items=["A", "B"]),
		),
	),
	"Material": material_form,
	"List": ListForm(Form(ControlText(variable_name="blaa")))
})

formify.app.allow_multiple_instances = False

window = formify.MainWindow(sidebar, allowed_file_extensions=["txt", "json"], auto_run=False)
window.show()
formify.run()
