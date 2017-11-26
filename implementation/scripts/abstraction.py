import json
from utils.node import Node

def get_resource_name(resource_json):
    """Return the resource name."""
    resource_obj = json.loads(resource_json)
    resource_name = resource_obj['id']
    return resource_name

def get_resource_elements(resource_json):
    """Return the list of defined data elements of resource"""
    resource_obj = json.loads(resource_json)
    resource_snapshot = resource_obj['snapshot']
    resource_snapshot_element = resource_snapshot['element']
    resource_elements = []
    backbone_element = {'active': False, 'prefix': ''}
    for element in resource_snapshot_element[1:]:  # The first element is not an element resource
        if 'base' not in element:  # Not include the base element
            if not backbone_element['active']:
                resource_elements.append(element)
                if element['type'] == [{'code': 'BackboneElement'}] :
                    backbone_element['active'] = True
                    backbone_element['prefix'] = element['id']
                    element['BackboneElement'] = []
            else:
                if element['id'].startswith(backbone_element['prefix']):
                    resource_elements[-1]['BackboneElement'].append(element)
                else:
                    backbone_element['active'] = False
                    resource_elements.append(element)
                    if element['type'] == [{'code': 'BackboneElement'}] :
                        backbone_element['active'] = True
                        backbone_element['prefix'] = element['id']
                        element['BackboneElement'] = []
    return resource_elements

def get_element_types(element_json):
    """Return the elements type."""
    element_obj = json.loads(element_json)
    element_types = []
    for element_type in element_obj['type']: # Element with Open Type has more than one type
        element_types.append(element_type['code'])
    return element_types

def get_element_max(element_json):
    """Return the element maximum cardinality."""
    element_obj = json.loads(element_json)
    return element_obj['max']

def get_element_min(element_json):
    """Return the element minimum cardinality."""
    element_obj = json.loads(element_json)
    return element_obj['min']

def get_value_set_reference(element_json):
    element_obj = json.loads(element_json)
    if 'binding' in element_obj.keys():
        binding = element_obj['binding']
        if 'valueSetReference' in binding.keys():
            valueSet = binding['valueSetReference']
            if 'reference' in valueSet.keys():
                    return valueSet['reference']
    return None

def add_resource_name_to_tree(root, resource_name):
    """Add resource name to root node of abstraction tree."""
    root.value['id'] = resource_name

def get_element_name(element_json):
    """Return the element name."""
    element_obj = json.loads(element_json)
    element_name = element_obj['id'].split('.')
    return element_name[-1]

def add_element_name_to_tree_node(node, element_name):
    """Add element name to a node of abstraction tree."""
    node.value['id'] = element_name

def add_element_type_to_tree_node(node, element_type):
    """Add element type to a node of abstraction tree."""
    node.value['type'] = element_type

def add_element_min_to_tree_node(node, minimum):
    node.value['min'] = minimum

def add_element_max_to_tree_node(node, maximum):
    node.value['max'] = maximum

def add_element_reference_to_tree_node(node, reference):
    node.value['reference'] = reference

def add_resource_element_to_tree_root(root, resource_element):
    """Add resource element to abstraction tree."""
    root.children.append(resource_element)

def get_type_definition(definitions, data_type):
    """Return data type definition."""
    return definitions[data_type]

def create_dictionary_definitions(type_definitions_json):
    """Create dictionary of types definition."""
    type_definitions_obj = json.loads(type_definitions_json)
    dictionary_definitions = {}
    for type_category, types in type_definitions_obj.items():
        for type_definition in types:
            type_id = type_definition['id']
            dictionary_definitions[type_id] = type_definition
    return dictionary_definitions

def add_type_definition(element, dictionary_definitions):
    """Add type definition to an resource element."""

    if element.value['type'] == 'BackboneElement':
        for element_backbone in element.children:
            type_node = Node()
            element_definition = dictionary_definitions[element_backbone.value['type']]
            add_element_name_to_tree_node(type_node, element_definition['id'])
            add_element_type_to_tree_node(type_node, element_definition['id'])
            element_backbone.children.append(type_node)
            add_type_definition(type_node, dictionary_definitions)
    #elif element.value['id'] != element.value['type']:
    else:
        element_definition = dictionary_definitions[element.value['type']]
        if is_primitive(dictionary_definitions, element.value['type']): # Primitive type case
            type_node = Node()
            add_element_name_to_tree_node(type_node, element_definition['id'])
            add_element_type_to_tree_node(type_node, element_definition['id'])
            element.children.append(type_node)
        else:  # Complex type case
            for element_type in element_definition['CML']:
                type_node = Node()
                add_element_name_to_tree_node(type_node, element_type['name'])
                add_element_type_to_tree_node(type_node, element_type['type'])
                element.children.append(type_node)
                add_type_definition(type_node, dictionary_definitions)

def is_primitive(definitions, data_type):
    """Check if a data type is a primitive data type."""
    data_type_definition = definitions[data_type]
    return 'CML' not in data_type_definition

def add_type_definitions(node, dictionary_definitions):
    """Add for each child its type definition."""
    for element in node.children:
        add_type_definition(element, dictionary_definitions)

def preorder(node):
    """Traverse a tree in preorder."""
    result = {}
    result['id'] = node.value['id']
    if 'min' in node.value.keys():
        result['min'] = node.value['min']
    if 'max' in node.value.keys():
        result['max'] = node.value['max']
    if 'reference' in node.value.keys():
        result['reference'] = node.value['reference']
    if len(node.children) > 0:
        result['CML'] = []
        for child in node.children:
            result['CML'].append(preorder(child))
    return result

def abstract(resource_json, type_definitions):
    """Abstract a resource in a type system"""
    root_node = Node()
    add_resource_name_to_tree(root_node, get_resource_name(resource_json))
    for resource_element in get_resource_elements(resource_json):
        node_element = Node()
        add_element_name_to_tree_node(node_element, get_element_name(json.dumps(resource_element)))
        element_type = get_element_types(json.dumps(resource_element))[0]
        add_element_type_to_tree_node(node_element, element_type)
        add_element_min_to_tree_node(node_element, get_element_min(json.dumps(resource_element)))
        add_element_max_to_tree_node(node_element, get_element_max(json.dumps(resource_element)))
        reference = get_value_set_reference(json.dumps(resource_element))
        if reference != None:
            add_element_reference_to_tree_node(node_element, reference)
        if element_type == 'BackboneElement':
            add_backbone_elements(node_element, get_backbone_elements(json.dumps(resource_element)))
        add_resource_element_to_tree_root(root_node, node_element)
    add_type_definitions(root_node, create_dictionary_definitions(type_definitions))
    return preorder(root_node)

def get_backbone_elements(element_json):
    """Return the backbone elements type."""
    element_obj = json.loads(element_json)
    backbone_elements = []
    for backbone_element in element_obj['BackboneElement']:
        backbone_elements.append(backbone_element)
    return backbone_elements

def add_backbone_elements(node_element, backbone_elements):
    for backbone_element in backbone_elements:
        node = Node()
        add_element_name_to_tree_node(node, get_element_name(json.dumps(backbone_element)))
        add_element_type_to_tree_node(node, get_element_types(json.dumps(backbone_element))[0])
        node_element.children.append(node)

if __name__ == '__main__':
    import sys
    resource = sys.argv[1]
    definition = sys.argv[2]
    output = sys.argv[3]
    resource_file = open(resource,'r')
    resource_json = resource_file.read()
    resource_file.close()
    definition_file = open(definition,'r')
    definition_json = definition_file.read()
    definition_file.close()
    schema = abstract(resource_json, definition_json)
    resource_file_name = resource.split('\\')[-1]
    resource_name = resource_file_name.split('.')[0] + '.schema.fhir.json'
    schema_file = open(output + resource_name,'w')
    schema_file.write(json.dumps(schema,indent=1))
    schema_file.close()
