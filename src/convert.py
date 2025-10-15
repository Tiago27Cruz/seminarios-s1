#!/usr/bin/env python3

import csv
import json
import sys
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
import argparse

TEST = "../resources/test_games.csv"
FULL = "../resources/steam_wikidata.csv"
CONTEXT = "../resources/steam_context.jsonld"


def load_context(context_file):
    """Load the JSON-LD context file."""
    with open(context_file, 'r') as f:
        return json.load(f)


def create_namespaces(context):
    """Create RDFlib namespace objects from the context."""
    namespaces = {}
    namespaces['xsd'] = XSD
    if 'wd' in context:
        namespaces['wd'] = Namespace(context['wd'])
    namespaces['smvg'] = Namespace('https://purl.org/smvg/')
    namespaces['schema'] = Namespace('https://schema.org/')
    namespaces['dcterms'] = Namespace('http://purl.org/dc/terms/')
    
    return namespaces


def get_property_uri(property_name, context, namespaces):
    """Get the URI for a property based on the context mapping."""
    if property_name in context:
        prop_def = context[property_name]
        if isinstance(prop_def, dict) and '@id' in prop_def:
            return URIRef(prop_def['@id'])
        elif isinstance(prop_def, str):
            return URIRef(prop_def)
    
    # If not found in context, create a property in the SMVG namespace
    return namespaces['smvg'][property_name]


def get_literal_type(property_name, context):
    """
        Get the XSD type for a literal value based on the context.
        Returns None if the property is expected to be a URI.
    """
    if property_name in context:
        prop_def = context[property_name]
        if isinstance(prop_def, dict) and '@type' in prop_def:
            type_str = prop_def['@type']
            if type_str == 'xsd:string':
                return XSD.string
            elif type_str == 'xsd:integer':
                return XSD.integer
            elif type_str == 'xsd:float':
                return XSD.float
            elif type_str == 'xsd:date':
                return XSD.date
            elif type_str == '@id':
                return None
    return XSD.string

def convert_csv_to_jsonld(csv_file, context_file, output_file=None, base_uri=None):
    """Convert CSV file to JSON-LD using the provided context."""
    
    context_data = load_context(context_file)
    context = context_data.get('@context', context_data)
    
    namespaces = create_namespaces(context)
    
    g = Graph()
    for prefix, namespace in namespaces.items():
        g.bind(prefix, namespace)
    
    if base_uri:
        g.bind('', Namespace(base_uri))
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for _, row in enumerate(reader, 1):
            # Define the @id for the subject
            row_id = row.get('id')
            if base_uri:
                subject_uri = URIRef(f"{base_uri}{row_id}")
            else:
                subject_uri = URIRef(f"{row_id}")

            # Define @type as a schema:VideoGame
            g.add((subject_uri, RDF.type, namespaces['schema']['VideoGame']))
            
            for column, value in row.items():
                if column == 'id': continue

                if value and value.strip(): 
                    prop_uri = get_property_uri(column, context, namespaces)
                    literal_type = get_literal_type(column, context)

                    if(column == "categories" or column == "steamspy_tags"):
                        value = value.replace("'", '"') 
                        values_str = value.split(";")

                        for val in values_str:
                            val = val.strip()
                            if val:
                                obj = Literal(val, datatype=XSD.string)
                                g.add((subject_uri, prop_uri, obj))
                        continue

                    elif literal_type is None:
                        value_str = value.strip()

                        if value_str.startswith(('http://', 'https://', 'urn:', 'wd:')): # Single URI
                            obj = URIRef(value_str)
                            g.add((subject_uri, prop_uri, obj))

                        elif value_str.startswith('[') and value_str.endswith(']'): # Handle list of URIs in the format ['uri', 'uri2', 'uri3']

                            uri_list = eval(value_str) # Convert the string to a Python list
                            for uri in uri_list:
                                uri = uri.strip()

                                if(uri.startswith("https://www.wikidata.org/wiki/")):
                                    uri = uri.replace("https://www.wikidata.org/wiki/", "wd:")
                                    
                                if uri.startswith(('http://', 'https://', 'urn:', 'wd:')):
                                    obj = URIRef(uri)
                                    g.add((subject_uri, prop_uri, obj))

                        else: # Fallback to treating as a single URI
                            obj = Literal(value_str, datatype=XSD.string)
                            g.add((subject_uri, prop_uri, obj))
                    else:
                        obj = Literal(value.strip(), datatype=literal_type)
                        g.add((subject_uri, prop_uri, obj))
                    
                    
    
    jsonld_str = g.serialize(format='json-ld', context=context, indent=2)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(jsonld_str)
        print(f"JSON-LD written to {output_file}")
    else:
        print(jsonld_str)


def main():
    parser = argparse.ArgumentParser(description='Convert CSV to JSON-LD using RDFlib')
    parser.add_argument('-i', '--csv_file', help='Input CSV file', default=FULL, type=str)
    parser.add_argument('-c', '--context', default=CONTEXT,
                       help='JSON-LD context file (default: resources/steam_context.jsonld)')
    parser.add_argument('-o', '--output', help='Output JSON-LD file (default: stdout)')
    parser.add_argument('-b', '--base-uri', help='Base URI for resources')
    
    args = parser.parse_args()
    
    if not Path(args.csv_file).exists():
        print(f"Error: CSV file '{args.csv_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not Path(args.context).exists():
        print(f"Error: Context file '{args.context}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        convert_csv_to_jsonld(args.csv_file, args.context, args.output, args.base_uri)
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
