import json

identifier = 0

def element_object_node(element_obj, terminology, terms):
    """Generate object constraint from element primitive type definition"""
    global identifier
    term = element_obj['id']
    if 'min' in element_obj.keys():
        minimum = element_obj['min']
        maximum = element_obj['max']
    CML = element_obj['CML'][0] #Must be a list of one element
    primitive_type = CML['id']
    terminology["id" + str(identifier)] = term
    if 'reference' in element_obj.keys():
        terms["id" + str(identifier)] = element_obj['reference']
    if 'min' in element_obj.keys():
        object_constraint = "ELEMENT[id" + str(identifier) + "] occurrences matches {" + str(minimum) + ".." + str(maximum) + "} matches { value matches { " + primitive_type +"[id" + str(identifier + 1) + "] } }"
    else:
        object_constraint = "ELEMENT[id" + str(identifier) + "] matches { value matches { " + primitive_type +"[id" + str(identifier + 1) + "] } }"
    identifier = identifier + 2
    return object_constraint

def is_primitive(element_obj):
    """Check if an element type definition is primitive"""
    CML = element_obj['CML']
    if len(CML) == 1:
        if 'CML' not in CML[0]:
            return True
    return False

def cluster_object_node(element_obj, object_constraint, terminology, terms):
    global identifier
    """Generate object constraint from complex primitive type definition"""
    if is_primitive(element_obj) == False:
        term = element_obj['id']
        terminology["id" + str(identifier)] = term
        if 'reference' in element_obj.keys():
            terms["id" + str(identifier)] = element_obj['reference']
        if 'min' in element_obj.keys():
            minimum = element_obj['min']
            maximum = element_obj['max']
        if 'min' in element_obj.keys():
            object_constraint = object_constraint + " CLUSTER[id" + str(identifier) + "]  occurrences matches {" + str(minimum) + ".." + str(maximum) + "} matches { items matches {"
        else:
            object_constraint = object_constraint + " CLUSTER[id" + str(identifier) + "] matches { items matches {"
        identifier = identifier + 1
        for element in element_obj['CML']:
            object_constraint = cluster_object_node(element, object_constraint, terminology, terms)
        object_constraint = object_constraint + " } }"
    else:
        object_constraint = object_constraint + " " + element_object_node(element_obj, terminology, terms)
    return object_constraint

def binding(terminology):
    resp = 'term_definitions\n = <["en"] = < '
    for k, v in terminology.items():
        resp = resp + "[\"" + k +"\"] = < text = <\""+ v + "\"> description = <\"\"> > "
    resp = resp + ' > >'
    return resp

def binding_terms(terms):
    resp = 'term_bindings\n = <["fhir"] = < '
    for k, v in terms.items():
        resp = resp + "[\"" + k +"\"] = <"+ v + "> "
    resp = resp + ' > >'
    return resp

if __name__ == '__main__':
    import sys
    schema_source = sys.argv[1]
    output = sys.argv[2]
    schema_source_file = open(schema_source,'r')
    schema_string = schema_source_file.read()
    schema_source_file.close()
    adl_file_name = schema_source.split('\\')[-1]
    adl_name = adl_file_name.split('.')[0] + '.adls'
    adl_file = open(output + adl_name,'w')
    adl = 'archetype (adl_version=2.0.6; rm_release=1.0.3)\n'
    adl = adl + 'openehr-ehr-CLUSTER.' + schema_source.split('.')[0] + '-fhir.v0.0.1\n'
    adl = adl + "language\n"
    adl = adl + "original_language = <[iso_639-1::en]>\n"
    adl = adl + "description\n"
    adl = adl + 'lifecycle_state = <"unmanaged">\n'
    identifier = 1
    terminology = {}
    terms = {}
    adl = adl + 'definition\n'
    adl = adl + cluster_object_node(json.loads(schema_string),"", terminology, terms) + '\n'
    adl = adl + 'terminology\n' + binding(terminology) + '\n' + binding_terms(terms)
    adl_file.write(adl)
    adl_file.close()
