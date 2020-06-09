from py2neo import Graph, Node, Relationship, NodeMatcher, Schema
class Neo4jGraphLayer(object):
    """Class to manage graph transactions"""
    def __init__(self):
        self.graph=None

    def authorize(self,uri,username,password):
        try:
            self.graph = Graph(uri, auth=(username, password))
            print("Authorization done")
        except Exception as e:
            print("Exception while authorizing:",e)
    """
    This function insert the svo tuplets with their labels
    """
    def insert(self,svos,so_labels,title):
        #Check if database connection is established
        if self.graph==None:
            print("Database is not authorized")
            return False
        count_inserted=0
        count_failed=0
        for svo,so_label in zip(svos,so_labels):
            sub, rel, obj = svo
            sub_label,obj_label=so_label
    
            sub_node = self.graph.nodes.match(name=sub).first()
            obj_node = self.graph.nodes.match(name=obj).first()
            try:
                #If does not find the subject node then create it
                if not sub_node:
                    if sub_label!=None:
                        sub_node = Node(title,sub_label,name = sub)
                    else:
                        sub_node = Node(title,name = sub)

                    self.graph.create(sub_node)
                else:
                    sub_node.add_label(title)
                    if sub_label!=None:
                        sub_node.add_label(sub_label)
                #If does not find the object node then create it
                if not obj_node:
                    if obj_label!=None:
                        obj_node = Node(title,obj_label,name = obj)
                    else:
                        obj_node = Node(title,name = obj)
                    self.graph.create(obj_node)
                else:
                    obj_node.add_label(title)
                    if obj_label!=None:
                        obj_node.add_label(obj_label)

                # Check if relationship exists
                if self.graph.match_one((sub_node, obj_node),r_type=rel)!=None:
                    print("relation existed")
                else:
                    relation = Relationship.type(rel)
                    self.graph.merge(relation(sub_node, obj_node))

                count_inserted+=1
            except Exception as e:
                count_failed+=1
                print("Exception while inserting:", e)
            
        print("Total successful insertion:",count_inserted)
        print("Total failed insertion:",count_failed)
        return True
    """
        Get all labels in the graph
    """
    def get_labels(self):
        schema=Schema(self.graph)
        return schema.node_labels

    """
        Get all relationship types in the graph
    """
    def get_relationship_types(self):
        schema=Schema(self.graph)
        return schema.relationship_types


        


