import pandas as pd
import json

# handle the data and exclude cases:
# excluded should be everything wihtout an author, because that indicates something like editorial or toc
# excluded should be types of articles, but which those are we first need to identify


####### Journal of Experimental Psychology: General ########
# Read in the CSV file
dfXge = pd.read_csv('results/Journals/APA/xge_articles.csv')

# Remove rows with "No authorship indicated" and save the result in a new DataFrame
xgeCleaned = dfXge[dfXge['Authors'] != "No authorship indicated"]
print(xgeCleaned["Authors"].isna().sum())  # Sum of rows where Authors is an empty string

# Remove rows with specific article types
excluded_types = ["Commentaries and Replies", "Commentary and Reply", "Commentary", 
                  "Commentaries", "Reply", "Comments", "Editorial", 
                  "Reply to Brown and Coyne (2017)", "Rejoinder", "Introduction"]
xgeCleaned = xgeCleaned[~xgeCleaned['Type'].isin(excluded_types)]

# Print the counts of each unique level in the 'Type' column
print("-"*50)
print(xgeCleaned['Type'].value_counts())

# Check for duplicates in the xgeCleaned DataFrame
duplicates = xgeCleaned[xgeCleaned.duplicated(subset='DOI', keep=False)]
if not duplicates.empty:
    print("Duplicates found in xgeCleaned:")
    print(duplicates['DOI'])
else:
    print("No duplicate DOI found in xgeCleaned.")

# Check for duplicates in the xgeCleaned DataFrame
duplicates = xgeCleaned[xgeCleaned.duplicated(subset='Title', keep=False)]
if not duplicates.empty:
    print("Duplicates found in xgeCleaned:")
    print(duplicates['Title'])
else:
    print("No duplicate Title found in xgeCleaned.")

# Write xgeCleaned to a CSV file
xgeCleaned.to_csv("results/Journals/APA/xge_articles_cleaned.csv", index=False)
# Write xgeCleaned to a JSON file using json.dump
with open("results/Journals/APA/xge_articles_cleaned.json", "w", encoding="utf-8") as json_file:
    json.dump(xgeCleaned.to_dict(orient="records"), json_file, indent=4, ensure_ascii=False)


####### Psychological Science ########
# Read in the CSV file
dfPss = pd.read_csv('results/Journals/Sage/pss_articles.csv')
# Remove rows with empty 'Authors' field
pssCleaned = dfPss.dropna(subset=['Authors'])

# Remove rows with specific article types
excluded_types = ["Correction", "Editorial", "Retraction", "Expression of concern", "Article commentary", "Letter"]
pssCleaned = pssCleaned[~pssCleaned['Type'].isin(excluded_types)]

# Print the counts of each unique level in the 'Type' column
print("="*50)
print(pssCleaned['Type'].value_counts())

# Check for duplicates in the pssCleaned DataFrame
duplicates = pssCleaned[pssCleaned.duplicated(subset='DOI', keep=False)]
if not duplicates.empty:
    print("Duplicates found in pssCleaned:")
    print(duplicates[['DOI']])
else:
    print("No duplicate DOI found in pssCleaned.")

# Check for duplicates in the pssCleaned DataFrame
duplicates = pssCleaned[pssCleaned.duplicated(subset='Title', keep=False)]
if not duplicates.empty:
    print("Duplicates found in pssCleaned:")
    print(duplicates[['Title']])
else:
    print("No duplicate Title found in pssCleaned.")

# Write pssCleaned to a CSV file
pssCleaned.to_csv("results/Journals/Sage/pss_articles_cleaned.csv", index=False)
# Write pssCleaned to a JSON file using json.dump
with open("results/Journals/Sage/pss_articles_cleaned.json", "w", encoding="utf-8") as json_file:
    json.dump(pssCleaned.to_dict(orient="records"), json_file, indent=4, ensure_ascii=False)


# Psychonomic Bulletin and Review
# Read in the CSV file
dfPbr = pd.read_csv('results/Journals/Springer/pbr_articles.csv')
pbrCleaned = dfPbr

# Remove all rows that are duplicates in the 'Title' column from pbrCleaned DataFrame
pbrCleaned = pbrCleaned.drop_duplicates(subset='Title', keep=False)
print("="*50)
# Check for duplicates in the pssCleaned DataFrame
duplicates = pbrCleaned[pbrCleaned.duplicated(subset='DOI', keep=False)]
if not duplicates.empty:
    print("Duplicates found in pbrCleaned:")
    print(duplicates[['DOI']])
else:
    print("No duplicate DOI found in pbrCleaned.")

# Remove rows with empty 'Authors' field
pbrCleaned = pbrCleaned.dropna(subset=['Authors'])

# Remove rows with specific article types
excluded_types = ["Theoretical Review", "Theoretical/Review", "Theoretical and Review Articles", "Notes and Comment", 
                  "Erratum", "Theoretical And Review Articles",
                  "Correction", "Comment", "Editorial", 
                  "Theoretical and review articles", "Preface", "Comment and Reply", "Retraction Note",
                  "Overview", "Corrigendum", "Letter to the Editor", "Psychonomic Society Keynote Address",
                  "THEORETICAL REVIEW", "Reply", "Observation", "Notes and comment", "Addendum"]
pbrCleaned = pbrCleaned[~pbrCleaned['Type'].isin(excluded_types)]

print("-"*50)
print(pbrCleaned['Type'].value_counts())

# Write pbrCleaned to a CSV file
pbrCleaned.to_csv("results/Journals/Springer/pbr_articles_cleaned.csv", index=False)
# Write pbrCleaned to a JSON file using json.dump
with open("results/Journals/Springer/pbr_articles_cleaned.json", "w", encoding="utf-8") as json_file:
    json.dump(pbrCleaned.to_dict(orient="records"), json_file, indent=4, ensure_ascii=False)


# Developmental Science
# Read in the CSV file
dfDs = pd.read_csv('results/Journals/Wiley/ds_articles.csv')
dsCleaned = dfDs

# Remove all rows that are duplicates in the 'Title' column from dsCleaned DataFrame
dsCleaned = dsCleaned.drop_duplicates(subset='Title', keep=False)

print("="*50)
# Check for duplicates in the pssCleaned DataFrame
duplicates = dsCleaned[dsCleaned.duplicated(subset='DOI', keep=False)]
if not duplicates.empty:
    print("Duplicates found in dsCleaned:")
    print(duplicates[['DOI']])
else:
    print("No duplicate DOI found in dsCleaned.")

# Remove rows with empty 'Authors' field
dsCleaned = dsCleaned.dropna(subset=['Authors'])

ds_type_levels = dsCleaned['Type'].unique()

excluded_types = [
    'Elizabeth Bates: a scientific obituary',
    'ARTICLE WITH PEER COMMENTARIES AND RESPONSEArticle',
    'Commentaries',
    'Response',
    'TARGET ARTICLE WITH COMMENTARIES AND RESPONSE',
    'TARGET ARTICLE WITH COMMENTARIES',
    'Editorial',
    '10th ANNIVERSARY SPECIAL ISSUE: A DECADE OF DEVELOPMENTAL SCIENCE: ISSUES, THEMES AND PROSPECTS',
    'TARGET ARTICLE WITH COMMENTARY AND RESPONSE',
    'TARGET ARTICLE WITH COMMENTARY',
    'COMMENTARIES',
    'COMMENTARY',
    'RESPONSE',
    'EDITORIAL',
    'INVITED REVIEW',
    'RESPONSE TO COMMENTARIES',
    'COVER IMAGE',
    'COMMENTARY_REPLY',
    'COMMENTARY_REPLY (INVITED ONLY)',
    'INVITED COMMENTARY (RESPONSE)',
    'INVITED COMMENTARY',
    'INVITED RESPONSE',
    'THIS ARTICLE HAS BEEN RETRACTED'
]
dsCleaned = dsCleaned[~dsCleaned['Type'].isin(excluded_types)]
print("-"*50)
print(dsCleaned['Type'].value_counts())

# Write pbrCleaned to a CSV file
dsCleaned.to_csv("results/Journals/Wiley/ds_articles_cleaned.csv", index=False)
# Write pbrCleaned to a JSON file using json.dump
with open("results/Journals/Wiley/ds_articles_cleaned.json", "w", encoding="utf-8") as json_file:
    json.dump(dsCleaned.to_dict(orient="records"), json_file, indent=4, ensure_ascii=False)


# Behaviour Research and Therapy
dfBrt = pd.read_csv('results/Journals/Elsevier/updated_brt_articles.csv')
brtCleaned = dfBrt

# Remove all rows that are duplicates in the 'Title' column from dsCleaned DataFrame
brtCleaned = brtCleaned.drop_duplicates(subset='Title', keep=False)

print("="*50)
# Check for duplicates in the pssCleaned DataFrame
duplicates = brtCleaned[brtCleaned.duplicated(subset='DOI', keep=False)]
if not duplicates.empty:
    print("Duplicates found in brtCleaned:")
    print(duplicates[['DOI']])
else:
    print("No duplicate DOI found in brtCleaned.")

# Remove rows with empty 'Authors' field
brtCleaned = brtCleaned.dropna(subset=['Authors'])

excluded_types = ["Review article", "Editorial", "Erratum", "Discussion"]
brtCleaned = brtCleaned[~brtCleaned['Type'].isin(excluded_types)]
print("-"*50)
print(brtCleaned['Type'].value_counts())

# Write pbrCleaned to a CSV file
brtCleaned.to_csv("results/Journals/Elsevier/brt_articles_cleaned.csv", index=False)
# Write pbrCleaned to a JSON file using json.dump
with open("results/Journals/Elsevier/brt_articles_cleaned.json", "w", encoding="utf-8") as json_file:
    json.dump(brtCleaned.to_dict(orient="records"), json_file, indent=4, ensure_ascii=False)


# Journal of Experimental Social Psychology
dfJesp = pd.read_csv('results/Journals/Elsevier/jesp_articles.csv')
jespCleaned = dfJesp

# Remove all rows that are duplicates in the 'Title' column from dsCleaned DataFrame
jespCleaned = jespCleaned.drop_duplicates(subset='Title', keep=False)

print("="*50)
# Check for duplicates in the pssCleaned DataFrame
duplicates = jespCleaned[jespCleaned.duplicated(subset='DOI', keep=False)]
if not duplicates.empty:
    print("Duplicates found in jespCleaned:")
    print(duplicates[['DOI']])
else:
    print("No duplicate DOI found in jespCleaned.")

# Remove rows with empty 'Authors' field
jespCleaned = jespCleaned.dropna(subset=['Authors'])

excluded_types = ["Review article", "Editorial", "Erratum", "Discussion"]
jespCleaned = jespCleaned[~jespCleaned['Type'].isin(excluded_types)]
print("-"*50)
print(jespCleaned['Type'].value_counts())

# Write pbrCleaned to a CSV file
jespCleaned.to_csv("results/Journals/Elsevier/jesp_articles_cleaned.csv", index=False)
# Write pbrCleaned to a JSON file using json.dump
with open("results/Journals/Elsevier/jesp_articles_cleaned.json", "w", encoding="utf-8") as json_file:
    json.dump(jespCleaned.to_dict(orient="records"), json_file, indent=4, ensure_ascii=False)

print("="*50)
print(len(xgeCleaned))
print(len(pssCleaned))
print(len(pbrCleaned))
print(len(dsCleaned))
print(len(brtCleaned))
print(len(jespCleaned))

print(sum([len(xgeCleaned), len(pssCleaned), len(pbrCleaned), len(dsCleaned), len(brtCleaned), len(jespCleaned)])) 
