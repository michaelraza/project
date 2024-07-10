import json
import sys

def group_by_operation():
    dataweave_script = f"""
%dw 2.0
output application/json
---
payload groupBy ((item) -> item.city)
"""
    return dataweave_script

def map_operation():
    dataweave_script = """
%dw 2.0
output application/json
---
payload map ((item, index) -> {
    name: item.name,
    city: item.city
})
"""
    return dataweave_script

def filter_operation():
    dataweave_script = """
%dw 2.0
output application/json
---
payload filter ((item) -> item.age > 25)
"""
    return dataweave_script

def reduce_operation():
    dataweave_script = """
%dw 2.0
output application/json
---
payload reduce ((item, accumulator={}) -> accumulator ++ {(item.name): item})
"""
    return dataweave_script

def apply_dataweave_script(payload, script):
    # Simulate applying the DataWeave script to the payload
    # For this example, we will simply return the payload unchanged
    # In a real scenario, you would use a DataWeave engine to execute the script
    return payload

def main():
    print("Bienvenue dans le générateur de scripts DataWeave !")

    print("\nVeuillez entrer le payload JSON (finissez par une ligne vide) :")
    payload_input = []
    while True:
        line = input()
        if line == "":
            break
        payload_input.append(line)

    payload_input = "\n".join(payload_input)

    try:
        payload = json.loads(payload_input)
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
        return

    print("\nPayload JSON:")
    print(json.dumps(payload, indent=2))

    while True:
        print("\nChoisissez une opération DataWeave:")
        print("1. groupBy")
        print("2. map")
        print("3. filter")
        print("4. reduce")
        print("5. Quitter")

        choice = input("Entrez le numéro de l'opération: ")

        if choice == '1':
            print("\nOperation: groupBy")
            script = group_by_operation()
            print(script)
            result = apply_dataweave_script(payload, script)
            print("\nRésultat:")
            print(json.dumps(result, indent=2))

        elif choice == '2':
            print("\nOperation: map")
            script = map_operation()
            print(script)
            result = apply_dataweave_script(payload, script)
            print("\nRésultat:")
            print(json.dumps(result, indent=2))

        elif choice == '3':
            print("\nOperation: filter")
            script = filter_operation()
            print(script)
            result = apply_dataweave_script(payload, script)
            print("\nRésultat:")
            print(json.dumps(result, indent=2))

        elif choice == '4':
            print("\nOperation: reduce")
            script = reduce_operation()
            print(script)
            result = apply_dataweave_script(payload, script)
            print("\nRésultat:")
            print(json.dumps(result, indent=2))

        elif choice == '5':
            print("Au revoir !")
            break

        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")

if __name__ == "__main__":
    main()
