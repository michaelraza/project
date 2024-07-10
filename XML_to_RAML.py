import re
import xml.etree.ElementTree as ET
import streamlit as st # type: ignore

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
        elem_dict.append(f"{indent}  xml:")
        elem_dict.append(f"{indent}    name: {tag_name}")
        elem_dict.append(f"{indent}    wrapped: true")

        # Handle XML attributes
        attributes = element.attrib
        if attributes:
            elem_dict.append(f"{indent}    properties:")
            for attr_key, attr_value in attributes.items():
                elem_dict.append(f"{indent}      {attr_key}:")
                elem_dict.append(f"{indent}        type: string")
                elem_dict.append(f"{indent}        xml:")
                elem_dict.append(f"{indent}          attribute: true")
                elem_dict.append(f"{indent}          name: {attr_key}")

        # Handle child elements
        child_elements = list(element)
        if child_elements:
            if not attributes:
                elem_dict.append(f"{indent}  properties:")
            for child in child_elements:
                elem_dict.extend(parse_element(child, indent_level + 1))

        return elem_dict

    raml.extend(parse_element(root))

    return '\n'.join(raml)

def main():
    st.title('Convertir XML en RAML Datatypes By Michael Rza')

    xml_input = st.text_area('Entrez le XML à convertir (copiez-collez votre XML ici) :', height=800)

    if st.button('Convertir en RAML'):
        normalized_input = normalize_xml(xml_input)

        # Afficher les résultats avant et après en colonnes
        col1, col2 = st.beta_columns(2)
        with col1:
            st.header("XML normalisé en une seule ligne :")
            st.code(normalized_input, language='xml')

        with col2:
            st.header("Résultat en RAML :")
            raml_output = xml_to_raml(normalized_input)
            st.code(raml_output, language='yaml')

if __name__ == "__main__":
    main()

