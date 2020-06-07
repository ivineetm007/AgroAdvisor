import textacy
from textacy.extract import subject_verb_object_triples
import neuralcoref
import spacy
import en_core_web_sm
from nltk.stem.wordnet import WordNetLemmatizer
from spacy.lang.en import English

class SVOExtractor(object):
    """abstract class for extracting Subject Verb Object triplets"""
    def extract(self):
        pass

class TextacySVOExtractor(SVOExtractor):
    """Class for extracting Subject Verb Object triplets using Textacy library"""
    def extract(self,text):
        nlp = en_core_web_sm.load()
        neuralcoref.add_to_pipe(nlp)
        doc= nlp(text)
        svos = list(subject_verb_object_triples(doc))
        svos_text = [(str(x[0]).strip(), str(x[1]).strip(), str(x[2]).strip()) for x in svos]
        return svos_text

class CustomSpacySVOExtractor(SVOExtractor):
    """Class for extracting Subject Verb Object triplets. Many functions are taken from https://github.com/KiranMayeeMaddi/NLP/blob/master/Code/SVO_Spacy.ipynb"""

    def __init__(self):
        self.subjects = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
        self.objects = ["dobj", "dative", "attr", "oprd"]

    """This function extract svo using pattern matching"""
    def findSVOs(self,tokens):
        
        def getSubsFromConjunctions(subs):
            moreSubs = []
            for sub in subs:
                # rights is a generator
                rights = list(sub.rights)
                rightDeps = {tok.lower_ for tok in rights}
                if "and" in rightDeps:
                    moreSubs.extend([tok for tok in rights if tok.dep_ in self.subjects or tok.pos_ == "NOUN"])
                    if len(moreSubs) > 0:
                        moreSubs.extend(getSubsFromConjunctions(moreSubs))
            return moreSubs

        def getObjsFromConjunctions(objs):
            moreObjs = []
            for obj in objs:
                # rights is a generator
                rights = list(obj.rights)
                rightDeps = {tok.lower_ for tok in rights}
                if "and" in rightDeps:
                    moreObjs.extend([tok for tok in rights if tok.dep_ in self.objects or tok.pos_ == "NOUN"])
                    if len(moreObjs) > 0:
                        moreObjs.extend(getObjsFromConjunctions(moreObjs))
            return moreObjs

        def getVerbsFromConjunctions(verbs):
            moreVerbs = []
            for verb in verbs:
                rightDeps = {tok.lower_ for tok in verb.rights}
                if "and" in rightDeps:
                    moreVerbs.extend([tok for tok in verb.rights if tok.pos_ == "VERB"])
                    if len(moreVerbs) > 0:
                        moreVerbs.extend(getVerbsFromConjunctions(moreVerbs))
            return moreVerbs

        def findSubs(tok):
            head = tok.head
            while head.pos_ != "VERB" and head.pos_ != "NOUN" and head.head != head:
                head = head.head
            if head.pos_ == "VERB":
                subs = [tok for tok in head.lefts if tok.dep_ == "SUB"]
                if len(subs) > 0:
                    verbNegated = isNegated(head)
                    subs.extend(getSubsFromConjunctions(subs))
                    return subs, verbNegated
                elif head.head != head:
                    return findSubs(head)
            elif head.pos_ == "NOUN":
                return [head], isNegated(tok)
            return [], False

        def isNegated(tok):
            negations = {"no", "not", "n't", "never", "none"}
            for dep in list(tok.lefts) + list(tok.rights):
                if dep.lower_ in negations:
                    return True
            return False

        def findSVs(tokens):
            svs = []
            verbs = [tok for tok in tokens if tok.pos_ == "VERB"]
            for v in verbs:
                subs, verbNegated = getAllSubs(v)
                if len(subs) > 0:
                    for sub in subs:
                        svs.append((sub.orth_, "!" + v.orth_ if verbNegated else v.orth_))
            return svs

        def getObjsFromPrepositions(deps):
            objs = []
            for dep in deps:
                if dep.pos_ == "ADP" and dep.dep_ == "prep":
                    objs.extend([tok for tok in dep.rights if tok.dep_  in OBJECTS or (tok.pos_ == "PRON" and tok.lower_ == "me")])
            return objs

        def getObjsFromAttrs(deps):
            for dep in deps:
                if dep.pos_ == "NOUN" and dep.dep_ == "attr":
                    verbs = [tok for tok in dep.rights if tok.pos_ == "VERB"]
                    if len(verbs) > 0:
                        for v in verbs:
                            rights = list(v.rights)
                            objs = [tok for tok in rights if tok.dep_ in self.objects]
                            objs.extend(getObjsFromPrepositions(rights))
                            if len(objs) > 0:
                                return v, objs
            return None, None

        def getObjFromXComp(deps):
            for dep in deps:
                if dep.pos_ == "VERB" and dep.dep_ == "xcomp":
                    v = dep
                    rights = list(v.rights)
                    objs = [tok for tok in rights if tok.dep_ in self.objects]
                    objs.extend(getObjsFromPrepositions(rights))
                    if len(objs) > 0:
                        return v, objs
            return None, None

        def getAllSubs(v):
            verbNegated = isNegated(v)
            subs = [tok for tok in v.lefts if tok.dep_ in self.subjects and tok.pos_ != "DET"]
            if len(subs) > 0:
                subs.extend(getSubsFromConjunctions(subs))
            else:
                foundSubs, verbNegated = findSubs(v)
                subs.extend(foundSubs)
            return subs, verbNegated

        def getAllObjs(v):
            # rights is a generator
            rights = list(v.rights)
            objs = [tok for tok in rights if tok.dep_ in self.objects]
            objs.extend(getObjsFromPrepositions(rights))

            #potentialNewVerb, potentialNewObjs = getObjsFromAttrs(rights)
            #if potentialNewVerb is not None and potentialNewObjs is not None and len(potentialNewObjs) > 0:
            #    objs.extend(potentialNewObjs)
            #    v = potentialNewVerb

            potentialNewVerb, potentialNewObjs = getObjFromXComp(rights)
            if potentialNewVerb is not None and potentialNewObjs is not None and len(potentialNewObjs) > 0:
                objs.extend(potentialNewObjs)
                v = potentialNewVerb
            if len(objs) > 0:
                objs.extend(getObjsFromConjunctions(objs))
            return v, objs

        svos = []
        verbs = [tok for tok in tokens if tok.pos_ == "VERB" and tok.dep_ != "aux"]
        for v in verbs:
            subs, verbNegated = getAllSubs(v)
            # hopefully there are subs, if not, don't examine this verb any longer
            if len(subs) > 0:
                v, objs = getAllObjs(v)
                for sub in subs:
                    for obj in objs:
                        objNegated = isNegated(obj)
                        svos.append((sub.lower_, "!" + v.lower_ if verbNegated or objNegated else v.lower_, obj.lower_))
        return svos
    def extract(self,text):
        #Loading model and apllying nlp operations
        nlp = en_core_web_sm.load()
        neuralcoref.add_to_pipe(nlp)
        doc= nlp(text)
        #Using pattern matching on the processed text
        spans = list(doc.ents) + list(doc.noun_chunks)
        for span in spans:
            span.merge()
            svos = self.findSVOs(doc)
        return svos
        



