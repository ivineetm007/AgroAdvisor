import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

class PreProcessor(object):
    """abstract class for Text Precprocessing"""
    """
    Function returns the negation handled word if it is presend in the appos dictionary
    Else returns the word itself
    """
    def negationHandling(self,word):
        if word in appos:
            return appos[word]
        else:
            return word
    """    
    Check if a word is a Stopword
    Stopword is a word that is commonly present in most of the documents and does not affect the model
    """
    def isNotStopWord(self,word):
        return word not in stopwords.words('english')
    """
    Function to preprocess text. Suitable to use for wikipedia text.
    """
    def preprocess(self,text):
        pass


class StandardPreProcessor(PreProcessor):
    """standard Text Precprocessing-text->lowercase->stop words->puunctuation->empty strings"""

    def preprocess(self,text):
        text = re.sub("[\(\[].*?[\)\]]", "", text)
        sentences = nltk.sent_tokenize(text)
        tokens = []
        temp = ""
    
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
        
            #Converting to LowerCase
            words = map(str.lower, words)
        
            # Remove stop words
            words = filter(lambda x: self.isNotStopWord(x), words)
        
            # Removing punctuations except '<.>/<?>/<!>'
            punctuations = '"#$%&\'()*+,-/:;<=>@\\^_`{|}~'
            words = map(lambda x: x.translate(str.maketrans('', '', punctuations)), words)
        
            # Remove empty strings
            words = filter(lambda x: len(x) > 0, words)
      
            tokens = tokens + list(words)
            temp = ' '.join(word for word in tokens)
        
        return temp
