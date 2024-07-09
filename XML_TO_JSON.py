import xml.etree.ElementTree as ET
import json

def xml_to_dict(element):
    data = {}

    # Récupère les attributs de l'élément
    if element.attrib:
        data["_"] = element.attrib

    # Récupère le texte de l'élément s'il existe
    if element.text:
        data["__text"] = element.text.strip()

    # Récupère les sous-éléments récursivement
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in data:
            if isinstance(data[child.tag], list):
                data[child.tag].append(child_data)
            else:
                data[child.tag] = [data[child.tag], child_data]
        else:
            data[child.tag] = child_data

    return data

def xml_input_to_json(xml_input):
    try:
        root = ET.fromstring(xml_input)
        root_tag = root.tag

        data = {}

        # Itère sur les enfants de l'élément racine
        for child in root:
            child_data = xml_to_dict(child)
            if child.tag in data:
                if isinstance(data[child.tag], list):
                    data[child.tag].append(child_data)
                else:
                    data[child.tag] = [data[child.tag], child_data]
            else:
                data[child.tag] = child_data

        # Crée la structure JSON avec le tag racine comme clé principale
        json_data = {
            root_tag: data
        }

        return json.dumps(json_data, indent=2)
    except Exception as e:
        print(f"Erreur lors du traitement du XML : {e}")
        return None

# Fonction pour lire l'entrée XML depuis le terminal
def read_xml_input():
    print("Entrez votre XML (entrez 'EOF' pour terminer l'entrée) :")
    lines = []
    while True:
        line = input().strip()
        if line.lower() == "eof":
            break
        lines.append(line)
    return ''.join(lines)

# Fonction pour afficher le code DataWeave correspondant
def print_dataweave_code(root_tag):
    print(f"Le code DataWeave pour convertir le XML en JSON est :")
    print(f"%dw 2.0")
    print(f"output application/json")
    print(f"---")
    print(f"payload")

# Fonction pour grouper par des balises similaires
def group_by_tag(xml_input, tag):
    try:
        root = ET.fromstring(xml_input)
        tag_data = root.findall(tag)
        grouped_data = [xml_to_dict(elem) for elem in tag_data]
        return json.dumps(grouped_data, indent=2)
    except Exception as e:
        print(f"Erreur lors du regroupement par balise : {e}")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    xml_input = read_xml_input()
    if xml_input:
        print("\nConversion XML vers JSON :")
        json_output = xml_input_to_json(xml_input)
        if json_output:
            print(json_output)
            root = ET.fromstring(xml_input)
            print_dataweave_code(root.tag)
        
        print("\nGroupement par balise (exemple avec 'book') :")
        grouped_output = group_by_tag(xml_input, "book")
        if grouped_output:
            print("""
                  Le code DataWeave correspondant pour le groupement par balise :
                  %dw 2.0
                  output application/json
                  ---
                  payload.{root.tag}.*{tag}
                  """)

