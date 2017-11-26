import json

def replace(schema_source, equivalents):
    """Replace data types using the equivalents"""
    schema_dest = schema_source
    for type1, type2 in equivalents.items():
        schema_dest = schema_dest.replace(': "' + type1 + '"', ': "' + type2 + '"')
    return schema_dest

if __name__ == '__main__':
    import sys
    schema_source = sys.argv[1]
    equivalents = sys.argv[2]
    output = sys.argv[3]
    schema_source_file = open(schema_source,'r')
    schema_string = schema_source_file.read()
    schema_source_file.close()
    equivalents_file = open(equivalents,'r')
    equivalents_string = equivalents_file.read()
    equivalents_file.close()
    schema_dest = replace(schema_string, json.loads(equivalents_string))
    schema_file_name = schema_source.split('\\')[-1]
    schema_name = schema_file_name.split('.')[0] + '.schema.openehr.json'
    schema_file = open(output + schema_name,'w')
    schema_obj = json.loads(schema_dest)
    schema_file.write(json.dumps(schema_obj,indent=1))
    schema_file.close()
