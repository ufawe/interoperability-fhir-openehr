import unittest
import definition

class TestDefinitionFunctions(unittest.TestCase):

#    def test_element_object_node(self):
#        element = {"id": "use","CML": [{"id": "DV_TEXT"}]}
#        object_constraint = "ELEMENT[id1] matches { value matches { DV_TEXT[id2] } }"
#        definition.identifier = 1
#        self.assertEqual(definition.element_object_node(element,{}), object_constraint)
#        definition.identifier = 1

    def test_is_primitive(self):
        element_primitive = {"id": "use","CML": [{"id": "DV_TEXT"}]}
        self.assertEqual(definition.is_primitive(element_primitive), True)
        element_complex = {"id": "period","CML": [{"id": "start","CML": [{"id": "DV_DATE_TIME"}]},{"id": "end","CML": [{"id": "DV_DATE_TIME"}]}]}
        self.assertEqual(definition.is_primitive(element_complex), False)

#    def test_cluster_object_node(self):
#        definition.identifier = 1
#        element_complex = {"id": "period","CML": [{"id": "start","CML": [{"id": "DV_DATE_TIME"}]},{"id": "end","CML": [{"id": "DV_DATE_TIME"}]}]}
#        object_constraint = "CLUSTER[id1] matches { items matches { ELEMENT[id2] matches { value matches { DV_DATE_TIME[id3] } } ELEMENT[id4] matches { value matches { DV_DATE_TIME[id5] } } } }"
#        print(definition.cluster_object_node(element_complex,"",{}))
#        self.assertEqual(definition.cluster_object_node(element_complex,""), object_constraint)
#        print(definition.cluster_object_node(element_complex,"", 1))

if __name__ == '__main__':
    unittest.main()
