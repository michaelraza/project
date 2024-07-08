import re
import xml.etree.ElementTree as ET

def normalize_xml(xml_input):
    # Supprimer les espaces, retours à la ligne et indentations
    normalized_xml = re.sub(r'>\s+<', '><', xml_input)
    normalized_xml = normalized_xml.replace('\n', '').replace('\r', '').strip()
    return normalized_xml

def xml_to_raml(xml_string):
    root = ET.fromstring(xml_string)
    raml = ["#%RAML 1.0 DataType", "properties:"]

    def parse_element(element, indent_level=1):
        indent = '  ' * indent_level
        elem_dict = []

        tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        elem_dict.append(f"{indent}{tag_name}:")
        elem_dict.append(f"{indent}  type: object")

        # Handle XML attributes
        attributes = element.attrib
        if attributes:
            elem_dict.append(f"{indent}  xml:")
            for attr_key, attr_value in attributes.items():
                elem_dict.append(f"{indent}    {attr_key}: {attr_value}")

        # Handle child elements
        child_elements = list(element)
        if child_elements:
            elem_dict.append(f"{indent}  properties:")
            for child in child_elements:
                child_tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                elem_dict.append(f"{indent}    {child_tag_name}:")
                if len(child) > 0:  # if child has sub-elements
                    elem_dict.append(f"{indent}      type: array")
                    elem_dict.append(f"{indent}      xml:")
                    elem_dict.append(f"{indent}        wrapped: false")
                    elem_dict.append(f"{indent}      items:")
                    elem_dict.append(f"{indent}        type: object")
                    elem_dict.extend(parse_element(child, indent_level + 3))
                else:  # if child has no sub-elements
                    elem_dict.append(f"{indent}      type: {get_element_type(child)}")

        return elem_dict

    def get_element_type(element):
        # Determine the RAML type based on the element content
        if element.text.isdigit():
            return "number"
        elif element.text.count('-') == 2 and all(part.isdigit() for part in element.text.split('-')):
            return "date"
        else:
            return "string"

    for child in root:
        raml.extend(parse_element(child))

    return '\n'.join(raml)

def main():
    print("Entrez le XML à convertir (tapez 'FIN' sur une ligne vide pour terminer l'entrée) :")
    xml_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'FIN':
            break
        xml_lines.append(line)

    xml_input = "\n".join(xml_lines)
    normalized_input = normalize_xml(xml_input)
    print("\nXML normalisé en une seule ligne :")
    print(normalized_input)

    raml_output = xml_to_raml(normalized_input)
    print("\nRésultat en RAML :\n")
    print(raml_output)

if __name__ == "__main__":
    main()
