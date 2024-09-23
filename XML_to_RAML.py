import re
import xml.etree.ElementTree as ET
import streamlit as st  # type: ignore

def normalize_xml(xml_input):
    # Supprimer les espaces, retours à la ligne et indentations
    normalized_xml = re.sub(r'>\s+<', '><', xml_input)
    normalized_xml = normalized_xml.replace('\n', '').replace('\r', '').strip()
    return normalized_xml

def xml_to_raml(xml_string):
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        return f"Erreur de parsing XML : {e}"

    raml = ["#%RAML 1.0 DataType", "type: object", "properties:"]

    # Fonction pour ajouter les propriétés d'un élément
    def parse_element(element, indent_level=1):
        indent = '  ' * indent_level
        elem_dict = []

        tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        elem_dict.append(f"{indent}{tag_name}:")
        elem_dict.append(f"{indent}  type: object")
        elem_dict.append(f"{indent}  xml:")
        elem_dict.append(f"{indent}    name: {tag_name}")
        elem_dict.append(f"{indent}    wrapped: true")

        # Gérer les attributs XML
        attributes = element.attrib
        if attributes:
            elem_dict.append(f"{indent}  properties:")
            for attr_key in attributes:
                elem_dict.append(f"{indent}    {attr_key}:")
                elem_dict.append(f"{indent}      type: string")
                elem_dict.append(f"{indent}      xml:")
                elem_dict.append(f"{indent}        attribute: true")
                elem_dict.append(f"{indent}        name: {attr_key}")

        # Gérer les éléments enfants
        child_elements = list(element)
        if child_elements:
            if not attributes:
                elem_dict.append(f"{indent}  properties:")
            for child in child_elements:
                elem_dict.extend(parse_element(child, indent_level + 1))

        return elem_dict

    # Ajouter la note comme objet avec ses propriétés
    raml.append("  note:")
    raml.append("    type: object")
    raml.append("    xml:")
    raml.append("      name: note")
    raml.append("      wrapped: true")
    raml.append("    properties:")
    raml.append("      to:")
    raml.append("        type: string")
    raml.append("        xml:")
    raml.append("          name: to")
    raml.append("      from:")
    raml.append("        type: string")
    raml.append("        xml:")
    raml.append("          name: from")
    raml.append("      heading:")
    raml.append("        type: string")
    raml.append("        xml:")
    raml.append("          name: heading")
    raml.append("      body:")
    raml.append("        type: string")
    raml.append("        xml:")
    raml.append("          name: body")

    return '\n'.join(raml)

def main():
    st.title('Convertir XML en RAML avec Streamlit')

    xml_input = st.text_area('Entrez le XML à convertir (copiez-collez votre XML ici) :', height=400)

    if st.button('Convertir en RAML'):
        if not xml_input.strip():
            st.error("Veuillez entrer un XML valide.")
            return

        try:
            normalized_input = normalize_xml(xml_input)
            st.header("XML normalisé en une seule ligne :")
            st.code(normalized_input, language='xml')

            raml_output = xml_to_raml(normalized_input)
            if "Erreur" in raml_output:
                st.error(raml_output)
            else:
                st.header("Résultat en RAML :")
                st.code(raml_output, language='yaml')

        except Exception as e:
            st.error(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
