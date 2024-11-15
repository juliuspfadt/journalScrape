import csv
import json

def csv_to_json(csv_filepath, json_filepath):
    data = []
    with open(csv_filepath, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    
    with open(json_filepath, mode='w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
csv_filepath = 'results/Journals/Elsevier/updated_brt_articles.csv'
json_filepath = 'results/Journals/Elsevier/updated_brt_articles.json'
csv_to_json(csv_filepath, json_filepath)