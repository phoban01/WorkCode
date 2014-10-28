import os
from music21 import *

source = os.path.expanduser("~/documents/musXML/ryan-xml")

for mxml in [x for x in os.listdir(source)[:10] if x.endswith('.xml')]:
	path = source + '/' +mxml
	midipath = path.replace('ryan-xml','ryan-midi').replace('.xml','.midi')
	parsed_xml = converter.parse(path)
	print parsed_xml.metadata.title
	for el in parsed_xml.recurse():
		if 'Instrument' in el.classes: # or 'Piano'
			el.activeSite.replace(el,instrument.Piano())
		elif 'Dynamic' in el.classes:
			el.activeSite.replace(el,dynamics.Dynamic('p'))
	# problem isnt chords but grace notes... they occupy the same position... can
	# we just strip them out?
	parsed_xml.write(".midi",midipath)

