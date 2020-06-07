import neuralcoref
import spacy
import en_core_web_sm

class NER(object):
    """abstract class for name entity recognition"""
    """
    THis function returns the dictonary of the entities in the text with its tag
    """
    def recognize(self):
        pass
 
class SpacyNER(NER):
    """class for name entity recognition by spacy library"""
    def recognize(self,text):
        nlp = en_core_web_sm.load()
        neuralcoref.add_to_pipe(nlp)
        entity_dict = {}

        doc= nlp(text)
        for ent in doc.ents:
            if ent not in entity_dict.keys():
                entity_dict[str(ent)] = ent.label_
        return entity_dict

