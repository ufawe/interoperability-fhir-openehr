import unittest
import abstraction
from utils.node import Node

class TestAbstractionFunctions(unittest.TestCase):

    def test_get_resource_name(self):
        resource_name = abstraction.get_resource_name('{"id":"Patient"}')
        self.assertEqual(resource_name, 'Patient')

    def test_get_resource_elements(self):
        resource_elements = abstraction.get_resource_elements('{"id":"Patient", "snapshot":{"element":[{"id":"Patient"},{"id":"Patient.id", "base":{},"type": [{"code": "id"}]},{"id":"Patient.identifier", "type": [{"code": "Identifier"}]},{"id": "Patient.contact", "type": [{"code": "BackboneElement"}]},{"id": "Patient.contact.gender", "type": [{"code": "code"}]}]}}')
        self.assertEqual(resource_elements, [{'id' : 'Patient.identifier','type': [{'code': 'Identifier'}]},{'id': 'Patient.contact', 'type': [{'code': 'BackboneElement'}], 'BackboneElement':[{'id': 'Patient.contact.gender', 'type': [{'code': 'code'}]}]}])

    def test_get_elements_type(self):
        element_types = abstraction.get_element_types('{"id":"Patient.identifier", "type":[{"code":"Identifier"}]}')
        self.assertEqual(element_types, ['Identifier'])
        element_types = abstraction.get_element_types('{"id":"Patient.identifier", "type":[{"code":"boolean"},{"code":"dateTime"}]}')
        self.assertEqual(element_types, ['boolean', 'dateTime'])

    def test_get_element_max(self):
        element_max = abstraction.get_element_max('{"id":"Patient.identifier", "min":0, "max": "*"}')
        self.assertEqual(element_max, "*")

    def test_get_element_min(self):
        element_min = abstraction.get_element_min('{"id":"Patient.identifier", "min":0, "max": "*"}')
        self.assertEqual(element_min, 0)

    def test_add_resource_name_to_tree(self):
        root = Node()
        abstraction.add_resource_name_to_tree(root, 'Patient')
        self.assertEqual(root.value['id'], 'Patient')

    def test_get_element_name(self):
        element_name = abstraction.get_element_name('{"id":"Patient.identifier"}')
        self.assertEqual(element_name, 'identifier')

    def test_add_element_name_to_tree_node(self):
        node = Node()
        abstraction.add_element_name_to_tree_node(node, 'identifier')
        self.assertEqual(node.value['id'], 'identifier')

    def test_add_element_type_to_tree_node(self):
        node = Node()
        abstraction.add_element_type_to_tree_node(node, 'Identifier')
        self.assertEqual(node.value['type'], 'Identifier')

    def test_add_resource_element_to_tree_root(self):
        root = Node()
        node = Node()
        node.value['id'] = 'identifier'
        abstraction.add_resource_element_to_tree_root(root, node)
        self.assertEqual(root.children[0], node)
        #contact_node = Node()
        #ontact_node.value['id'] = 'contact'
        #contact_node.value['type'] = 'BackboneElement'
        #abstraction.add_resource_element_to_tree_root(root, contact_node)
        #gender_node = Node()
        #gender_node.value['id'] = 'gender'
        #gender_node.value['type'] = 'code'
        #self.assertEqual(root.children[1].children[0], gender_node)

    def test_get_type_definition(self):
        type_definitions = {"boolean" : {"id":"boolean"}, "Identifier" : {"id":"Identifier","CML":[{"name":"use", "type":"code"}]}}
        boolean_definition = {'id' : 'boolean'}
        identifier_definition = {'id' : 'Identifier', 'CML' : [{'name' : 'use', 'type' : 'code'}]}
        self.assertEqual(abstraction.get_type_definition(type_definitions, 'boolean'), boolean_definition)
        self.assertEqual(abstraction.get_type_definition(type_definitions, 'Identifier'), identifier_definition)

    def test_create_dictionary_definitions(self):
        type_definitions = '{"primitiveTypes":[{"id":"boolean"}],"complexTypes":[{"id":"Identifier","CML":[{"name":"use", "type":"code"}]}]}'
        definitions = {"boolean" : {"id":"boolean"}, "Identifier" : {"id":"Identifier","CML":[{"name":"use", "type":"code"}]}}
        self.assertEqual(abstraction.create_dictionary_definitions(type_definitions), definitions)

    def test_node_equality(self):
        node1 = Node()
        node1.value['id'] = 'boolean'
        node1.value['type'] = 'boolean'
        node2 = Node()
        node2.value['id'] = 'boolean'
        node2.value['type'] = 'boolean'
        self.assertEqual(node1, node2)

    def test_add_type_definition(self):
        type_definitions = {"boolean" : {"id":"boolean"},"code" : {"id":"code"}, "Identifier" : {"id":"Identifier","CML":[{"name":"use", "type":"code"}]}}
        active_node = Node()
        active_node.value['id'] = 'active'
        active_node.value['type'] = 'boolean'
        boolean_node = Node()
        boolean_node.value['id'] = 'boolean'
        boolean_node.value['type'] = 'boolean'
        abstraction.add_type_definition(active_node, type_definitions)
        self.assertEqual(active_node.children[0], boolean_node )
        identifier_node = Node()
        identifier_node.value['id'] = 'identifier'
        identifier_node.value['type'] = 'Identifier'
        use_node = Node()
        use_node.value['id'] = 'use'
        use_node.value['type'] = 'code'
        code_node = Node()
        code_node.value['id'] = 'code'
        code_node.value['type'] = 'code'
        use_node.children.append(code_node)
        abstraction.add_type_definition(identifier_node, type_definitions)
        self.assertEqual(identifier_node.children[0], use_node)
        contact_node = Node()
        contact_node.value['id'] = 'contact'
        contact_node.value['type'] = 'BackboneElement'
        gender_node = Node()
        gender_node.value['id'] = 'gender'
        gender_node.value['type'] = 'code'
        contact_node.children.append(gender_node)
        abstraction.add_type_definition(contact_node, type_definitions)
        #Correct this test
        #print(contact_node.children[0].children[0].children[0].value)
        #print(code_node.children)
        #self.assertEqual(contact_node.children[0].children[0], code_node)

    def test_is_primitive(self):
        definitions = {"boolean" : {"id":"boolean"}, "Identifier" : {"id":"Identifier","CML":[{"name":"use", "type":"code"}]}}
        self.assertTrue(abstraction.is_primitive(definitions, 'boolean'))
        self.assertFalse(abstraction.is_primitive(definitions, 'Identifier'))

    def test_add_type_definitions(self):
        type_definitions = {"boolean" : {"id":"boolean"},"code" : {"id":"code"}, "Identifier" : {"id":"Identifier","CML":[{"name":"use", "type":"code"}]}}
        root_node = Node()
        active_node = Node()
        active_node.value['id'] = 'active'
        active_node.value['type'] = 'boolean'
        boolean_node = Node()
        boolean_node.value['id'] = 'boolean'
        boolean_node.value['type'] = 'boolean'
        active_node.children.append(boolean_node)
        root_node.children.append(active_node)
        identifier_node = Node()
        identifier_node.value['id'] = 'identifier'
        identifier_node.value['type'] = 'Identifier'
        use_node = Node()
        use_node.value['id'] = 'use'
        use_node.value['type'] = 'code'
        code_node = Node()
        code_node.value['id'] = 'code'
        code_node.value['type'] = 'code'
        use_node.children.append(code_node)
        identifier_node.children.append(use_node)
        root_node.children.append(identifier_node)
        root_empty = Node()
        active_empty = Node()
        active_empty.value['id'] = 'active'
        active_empty.value['type'] = 'boolean'
        root_empty.children.append(active_empty)
        identifier_empty = Node()
        identifier_empty.value['id'] = 'identifier'
        identifier_empty.value['type'] = 'Identifier'
        root_empty.children.append(identifier_empty)
        abstraction.add_type_definitions(root_empty, type_definitions)
        self.assertEqual(root_empty, root_node )

    def test_preorder(self):
        root_node = Node()
        root_node.value['id'] = 'Patient'
        active_node = Node()
        active_node.value['id'] = 'active'
        active_node.value['type'] = 'boolean'
        boolean_node = Node()
        boolean_node.value['id'] = 'boolean'
        boolean_node.value['type'] = 'boolean'
        active_node.children.append(boolean_node)
        root_node.children.append(active_node)
        identifier_node = Node()
        identifier_node.value['id'] = 'identifier'
        identifier_node.value['type'] = 'Identifier'
        use_node = Node()
        use_node.value['id'] = 'use'
        use_node.value['type'] = 'code'
        code_node = Node()
        code_node.value['id'] = 'code'
        code_node.value['type'] = 'code'
        use_node.children.append(code_node)
        identifier_node.children.append(use_node)
        root_node.children.append(identifier_node)
        result = {}
        result['id']='Patient'
        result['CML']=[{'id':'active','CML':[{'id':'boolean'}]},{'id':'identifier','CML':[{'id':'use','CML':[{'id':'code'}]}]}]
        self.assertEqual(abstraction.preorder(root_node), result)

#    def test_abstract(self):
#        resource = '{"id":"Patient", "snapshot":{"element":[{"id":"Patient"},{"id":"Patient.id", "base":{}},{"id":"Patient.active", "type": [{"code": "boolean"}]}]}}'
#        result = {}
#        result['id']='Patient'
#        result['CML']=[{'id':'active','CML':[{'id':'boolean'}]}]
#        type_definitions = '{"primitiveTypes":[{"id":"boolean"}],"complexTypes":[{"id":"Identifier","CML":[{"name":"use", "type":"code"}]}]}'
#        self.assertEqual(abstraction.abstract(resource,type_definitions), result)

    def test_get_backbone_elements(self):
        contact_element = '{"id": "Patient.contact", "type": [{"code": "BackboneElement"}], "BackboneElement":[{"id": "Patient.contact.gender", "type": [{"code": "code"}]}]}'
        backbone_element = [{'id': 'Patient.contact.gender', 'type': [{'code': 'code'}]}]
        self.assertEqual(abstraction.get_backbone_elements(contact_element), backbone_element)

    def test_add_backbone_elements(self):
        contact = Node()
        contact.value['id'] = 'contact'
        contact.value['type'] = 'BackboneElement'
        backbone_element = [{'id': 'gender', 'type': [{'code': 'code'}]}]
        abstraction.add_backbone_elements(contact, backbone_element)
        self.assertEqual(contact.children[0].value['id'], 'gender')
        self.assertEqual(contact.children[0].value['type'], 'code')

if __name__ == '__main__':
    unittest.main()
