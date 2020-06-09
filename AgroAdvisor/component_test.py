text="""Cotton (Gossypium sp.) is one of the most important commercial crops playing a key role in economics. In India cotton is cultivated in 9 million hectares in varied agro-climatic conditions across nine major States. Cotton cultivation offers 200 mandays/ha of employment. It employs directly and indirectly more than 60 million persons in its production, processing and marketing. India has the largest area under cotton, but its production is just 15.8 million bales, much lower for the vast area. Cotton is a tropical and subtropical crop. For the successful germination of its seeds, a minimum temperature of 15o C is required. The optimum temperature range for vegetative growth is 21 o - 27 o C. It can tolerate temperatures as high as 43 oC, but does not do well if the temperature falls below 21 oC. During the period of fruiting, warm days and cool nights with large diurnal variations are conducive to good boll and fibre development.
In cotton selection on of soil is very important. Cotton is grown on a variety of soils. Soil should be black medium to deep (90cm) having good drainage availability. Cotton does not tolerate water-logging condition. It is grown mainly as a dry crop in the black cotton and medium black soil. Irrigated cotton is taken in the alluvial soils.Cotton is sown on ridges and furrows. For irrigated cotton the land is given a deep ploughing followed by two harrowings. Ridges and furrows having different spacing for irrigated and rainfed cotton. For irrigated cotton shallow ridges on 90cm spacing should be prepared which helps in irrigation. According to slope of land, length of ridges should be 6-9m.
"""
#from app.textprocessor.PreProcessor import *
#from app.textprocessor.CRResolver import *
#from app.textprocessor.NER import *
#from app.textprocessor.SVOExtractor import *
#preprocessor=StandardPreProcessor()
#preprocessedText=preprocessor.preprocess(text)
#crResolver=SpacyCRResolver()
#crText=crResolver.resolve(preprocessedText)
#ner=SpacyNER()
#svoextractor=CustomSpacySVOExtractor()
#entity_dict=ner.recognize(crText)
#svo_list=svoextractor.extract(crText)
#print(crText)
#print(entity_dict)
#print(svo_list)

#svo_labels=[]
#def findNearestEntity(text,entity_dict):
#    if(text in entity_dict.keys()):
#        return entity_dict[text]
#    else:
#        #Try regex matching
#        for key in entity_dict.keys():
#            if key in text:
#                return entity_dict[key]
#    return None
   
#for svo in svo_list:
#    label_sub=findNearestEntity(svo[0],entity_dict)
#    label_obj=findNearestEntity(svo[2],entity_dict)
#    svo_labels.append((label_sub,label_obj))
#print(svo_labels)
svos=[('india cotton', 'cultivated', '9 million hectares'), ('cotton cultivation', 'offers', '200 mandaysha employment'), ('irrigated cotton', 'taken', 'furrows'), ('irrigated', 'followed', 'two harrowings'), ('ridges', 'furrows', 'different spacing'), ('spacing', 'helps', 'irrigation'), ('slope land length', 'ridges', '69m')]
so_labels=[(None, 'CARDINAL'), (None, 'DATE'), (None, None), (None, 'CARDINAL'), (None, None), (None, None), (None, 'CARDINAL')]
title='cotton'
#graph testing
g_uri="bolt://localhost:11003"
g_pass="12qwaszx"
g_user="neo4j"

from app.model import Neo4jGraphLayer
neograph=Neo4jGraphLayer()
#wronmg password
neograph.authorize(g_uri,g_user,"")
#AUrhorization testing
neograph.authorize(g_uri,g_user,g_pass)
#
neograph.insert(svos=svos,title=title,so_labels=so_labels)
print(neograph.get_labels())
print(neograph.get_relationship_types())
#Reinserting same
neograph.insert(svos=svos,title=title,so_labels=so_labels)
print(neograph.get_labels())
print(neograph.get_relationship_types())