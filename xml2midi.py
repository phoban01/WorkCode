from music21 import *

xml = converter.parse("/users/piarashoban/documents/schbavmasample.xml")

# lots of scope for doing analytics in music21
print xml.metadata.title

xml.write(".midi","/users/piarashoban/documents/schubert.midi")git

#end of file