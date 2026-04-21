import csv
import json

def generate_quality_report(file_path):
    """
    Génère un rapport de qualité pour un fichier CSV.
    """
    # Initialisation de la structure du rapport (Étape 4)
    report = {
        "row_count": 0,
        "columns": [],
        "missing_values": {},
        "invalid_values": {}
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Extraire les noms des colonnes
            columns = reader.fieldnames
            report["columns"] = list(columns) if columns else []
            
            # Initialiser les compteurs (Étape 5)
            missing_counts = {col: 0 for col in report["columns"]}
            invalid_counts = {}
            row_count = 0

            # Parcourir les lignes pour calculer les métriques
            for row in reader:
                row_count += 1
                
                for col in report["columns"]:
                    # Vérifier les valeurs manquantes
                    value = row.get(col, "")
                    if value == "" or value is None:
                        missing_counts[col] += 1
                    
                    # Vérifier les valeurs invalides pour la colonne 'amount'
                    if col == "amount":
                        try:
                            amount_val = float(row["amount"])
                            if amount_val <= 0:
                                invalid_counts["amount"] = invalid_counts.get("amount", 0) + 1
                        except (ValueError, TypeError):
                            # Si on ne peut pas transformer en nombre (ex: texte "invalid")
                            invalid_counts["amount"] = invalid_counts.get("amount", 0) + 1

            # Mettre à jour le rapport final
            report["row_count"] = row_count
            # On ne garde que les colonnes qui ont au moins une erreur (v > 0)
            report["missing_values"] = {k: v for k, v in missing_counts.items() if v > 0}
            report["invalid_values"] = invalid_counts

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
        
    return report

# Point d'entrée du script (Étape 7)
if __name__ == "__main__":
    csv_file = "transactions.csv"
    report = generate_quality_report(csv_file)
 
    if report:
        output_file = "csv_quality_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"Quality report generated successfully: {output_file}")