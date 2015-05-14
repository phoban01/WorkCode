import os,re,collections
from music21 import *
import matplotlib.pyplot as plt

def translate_pitch_counter(data):
	keys = ["C","C#","D","D#","E","F","F#","G",'G#',"A","A#","B"]
	d = collections.OrderedDict()
	for i,x in enumerate(keys):
		d[x] = data[i]
	return d

def replace_digits(text):
    return re.sub("(-?\d+).|(\+1)", lambda m: '', text)

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]','$', text)

def write_ly_file(score,path):
	# strip out unnecessary formatting information
	removes = [
	"\set stemRightBeamCount = #1\n","\set stemLeftBeamCount = #1\n",
	"\set stemRightBeamCount = #2\n","\set stemLeftBeamCount = #2\n",
	"\set stemRightBeamCount = #3\n","\set stemLeftBeamCount = #3\n",
	"\set stemRightBeamCount = #4\n","\set stemLeftBeamCount = #4\n",
	"\once \override Stem #'direction = #DOWN","\once \override Stem #'direction = #UP",
	"\\break"
	]
	lpc = lily.translate.LilypondConverter()
	lpPartsAndOssiaInit = lpc.lyPartsAndOssiaInitFromScore(score)
	hdr = lpc.setHeaderFromMetadata(score.metadata)
	lpGroupedMusicList = lpc.lyGroupedMusicListFromScoreWithParts(score, scoreInit = lpPartsAndOssiaInit)
	outly = open(path,'w')
	name = str(hdr.lilypondHeaderBody).replace('title = ','').strip().replace('"','')
	header = "\header {{\n\t  title = \"{0}\"\n\t}}\n".format(name)
	outly.write("%%%%% Lilypond File For {0} %%%%%\n\n".format(name))
	name = remove_non_ascii(replace_digits(name).strip().lower())
	trans = ''.join(chr(c) if chr(c).isupper() or chr(c).islower() else ' ' for c in range(256))
	name = '_'.join(name.translate(trans).split())
	outly.write("%s = \n" % name)
	music = lpGroupedMusicList.__str__().replace('nUnnamedgotreblegstaffpp','"Main"')
	for i in removes:
		music = music.replace(i,'').rstrip('\n')
	music = music.split('\n')
	outly.write("\score {\n\t")
	for i in music:
		if not not i.strip():
			outly.write(i+"\n")
			if i.strip().endswith("}") or i.strip().endswith("]"):
				outly.write("\n")
	outly.write("\t%s\n\t}" % header)
	outly.close()
	names.append(name)
	bookfile.write("\\include \"%s\"\n"%path)
	return None

source = os.path.expanduser("~/documents/musXML/ryan-xml")
bookpath = os.path.expanduser("~/documents/musXML/ryan-book.ly")
template_path = os.path.expanduser("~/documents/musXML/ryan-template.ly")
bookfile = open(bookpath,'w')
bookfile.write("\\version \"2.18.2\"\n")
global names
names = []
global pitch_class_counter
pitch_class_counter = [0 for i in range(0,12)]

# need to write a proper lilypond parser
# main things it needs to handle: grace notes and repeats
# at the moment music21 is good because it ignores repeats
# just sort out that space crap and we can use it for stats
# and melodic tests

for mxml in [x for x in os.listdir(source)[:14] if x.endswith('.xml')]:
	path = source + '/' +mxml
	midipath = path.replace('ryan-xml','ryan-midi').replace('.xml','.midi')
	lilypath = path.replace('ryan-xml','ryan-ly').replace('.xml','.ly')
	parsed_xml = converter.parse(path)
	# print parsed_xml.metadata.title
	p = parsed_xml.parts[0]

	for m in p.getElementsByClass('Measure'):
		z = m.timeSignature,m.keySignature,m.leftBarline,m.rightBarline
		for n in m.notes:
			if not n.isChord:
				pitch_class_counter[n.pitchClass] += 1
			else:
				for x in n.pitches:
					pitch_class_counter[x.pitchClass] += 1
			# if len(n.expressions) > 0:
				# print n.expressions
			# slur = n.getSpannerSites('Slur')
			# for sp in slur:
			# 	if sp.isFirst(n): print 'StartSlur \\('
			# 	elif sp.isLast(n): print 'EndSlur \\)'
			# if n.isChord:
			# 	# replace chords with upper tone
			# 	x = note.Note(n.pitches[-1],quarterLength=n.duration.quarterLength)
			# 	m.replace(n,x)
			if n.isGrace == True:
				m.remove(n)
	for el in parsed_xml.recurse():
		if 'Instrument' in el.classes: # or 'Piano'
			el.activeSite.replace(el,instrument.Piano())
		elif 'Dynamic' in el.classes:
			el.activeSite.replace(el,dynamics.Dynamic('p'))
	# grace notes have been stripped out... still complaining about notes at same time
	# .... need to remove chord tones? something to do with spacer voices I think... why are they in
	# in ly file too? Also repeats are not handled at all.
	# !.... need to produce folder of lily files so that we can see exactly where the issues
	# might be 
	# parsed_xml.write(".midi",midipath)
	write_ly_file(parsed_xml,lilypath)

bookfile.write("\n\\include \"%s\"\n\n" % template_path)
bookfile.write("\n\\book {\n")
for i in names:
	bookfile.write("\t \\%s \n"%i)
bookfile.write("}\n%%%EOF")
bookfile.close()

# x = translate_pitch_counter(pitch_class_counter)
# plt.bar(range(len(x)),x.values(),color='black',align='center',width=0.85)
# plt.xticks(range(len(x)),x.keys())
# plt.autoscale()
# plt.title('Note Frequency in Ryans Mammoth Collection')
# plt.savefig(os.path.expanduser("~/documents/musXML/ryan-note-freq.pdf"))

