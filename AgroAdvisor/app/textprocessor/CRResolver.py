import neuralcoref
import spacy
import en_core_web_sm
class CRResolver(object):
    """abstract class for co-reference resolution"""
    def resolve(self):
        pass

class SpacyCRResolver(CRResolver):
    """Class for co-reference resolution by spacy libraray using en-core-web-sm"""
    def resolve(self,text):
        nlp = en_core_web_sm.load()
        neuralcoref.add_to_pipe(nlp)
        doc = nlp(text)
        return doc._.coref_resolved



