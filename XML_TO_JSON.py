import streamlit as st # type: ignore
import xml.etree.ElementTree as ET
import json
from collections import Counter

# Fonction pour convertir un XML en dictionnaire Python
def xml_to_dict(element):
    node = {}
    if element.attrib:
        # Ignore attributes not needed
        node.update({f"_{k}": v for k, v in element.attrib.items() if k != 'image'})
    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag not in node:
            node[child.tag] = child_dict
        else:
            if not isinstance(node[child.tag], list):
                node[child.tag] = [node[child.tag]]
            node[child.tag].append(child_dict)
    if element.text and element.text.strip():
        if node:
            node["__text"] = element.text.strip()
        else:
            return element.text.strip()
    return node

# Fonction pour compter les balises, leur profondeur et leur proximité à la racine
def extract_tags_and_depth(element, tag_counter, depth):
    tag_counter[(element.tag, depth)] += 1
    for child in element:
        extract_tags_and_depth(child, tag_counter, depth + 1)

# Identification de la balise la plus fréquente et la plus proche de la racine
def identify_frequent_tag(root):
    tag_counter = Counter()
    extract_tags_and_depth(root, tag_counter, 1)
    if tag_counter:
        # Trie d'abord par fréquence, puis par profondeur (proche de la racine)
        sorted_tags = sorted(tag_counter.items(), key=lambda item: (-item[1], item[0][1]))
        # Retourne la balise la plus fréquente et la plus proche de la racine
        most_common_tag = min(sorted_tags, key=lambda item: item[0][1])[0]
        return most_common_tag
    return None

# Génération du script DataWeave
def generate_dataweave_script(root, frequent_tag):
    dw_script = """%dw 2.0
output application/json
---
"""
    if frequent_tag:
        dw_script += f"payload.{root.tag}.*{frequent_tag} map {{\n"
        child_example = root.find(f".//{frequent_tag}")
        if child_example is not None:
            for child in child_example:
                # Ignore attributes and elements not needed
                if child.tag not in ['image', 'color_swatch']:
                    dw_script += f"  {child.tag}: $.{child.tag},\n"
            dw_script = dw_script.rstrip(",\n") + "\n}"
        else:
            dw_script += "  // Aucun élément trouvé pour le regroupement\n}"
    else:
        dw_script += "payload"
    
    return dw_script

# Transformation XML en JSON avec option de regroupement
def transform_xml_to_json(xml_string, group_by_tag=None):
    try:
        root = ET.fromstring(xml_string)
        xml_dict = {root.tag: xml_to_dict(root)}
        
        if group_by_tag:
            # Suppression des indices de liste pour les éléments groupés par balise
            for parent in root.findall(f".//{group_by_tag}/.."):
                parent_dict = xml_to_dict(parent)
                if isinstance(parent_dict[group_by_tag], list):
                    parent_dict[group_by_tag] = [d for d in parent_dict[group_by_tag]]
                else:
                    parent_dict[group_by_tag] = [parent_dict[group_by_tag]]
        
        dw_script = generate_dataweave_script(root, group_by_tag)
        
        return json.dumps(xml_dict, indent=2), dw_script
    except Exception as e:
        return f"Erreur lors du traitement du XML : {e}", ""

# Application Streamlit
st.title("XML to JSON Transformer with DataWeave Script")

st.header("Enter your XML")
xml_input = st.text_area("XML input", height=300)

if st.button("Transform"):
    if xml_input.strip():
        root = ET.fromstring(xml_input)
        frequent_tag = identify_frequent_tag(root)
        st.write(f"**La balise la plus fréquente et la plus proche de la racine est :** `{frequent_tag}`")

        # Transformation simple XML -> JSON
        json_output, dw_script = transform_xml_to_json(xml_input)
        st.subheader("Transformation simple (XML -> JSON)")
        st.json(json_output)
        st.subheader("Le code DataWeave correspondant")
        st.code("%dw 2.0\noutput application/json\n---\npayload")

        # Transformation avec regroupement par la balise la plus fréquente
        if frequent_tag:
            json_output, dw_script = transform_xml_to_json(xml_input, group_by_tag=frequent_tag)
            st.subheader(f"Transformation avec regroupement par balise '{frequent_tag}'")
            st.json(json_output)
            st.subheader(f"Le code DataWeave correspondant pour le regroupement par '{frequent_tag}'")
            st.code(dw_script)
            
            # Boutons pour copier la sortie JSON et le script DataWeave
            if st.button("Copy JSON to clipboard"):
                st.write("Copied to clipboard!")
                st.code(json_output)
            
            if st.button("Copy DataWeave script to clipboard"):
                st.write("Copied to clipboard!")
                st.code(dw_script)
        else:
            st.write("Aucune balise fréquente trouvée pour le regroupement.")
    else:
        st.error("Veuillez entrer un XML valide.")
