import pandas as pd

'''
Todo:
- only use every second article
- makes sense to actually over assign the reviewers, so we just split the 8267 articles into as many parts as we have reviewers
then we randomly choose 10% of the articles and split them also into as many parts as we have reviewers and assign them
'''


updated_csv_path = 'results/Articles/journals_sample_withlinks.csv'
output_csv_path = 'results/Articles/journals_sample_forreview.csv'

# Read the CSV file
df = pd.read_csv(updated_csv_path)

# Remove certain columns
columns_to_remove = ['Author Affiliations', 'Pages', 'Normalized Title', 'Volume', 'Issue']
df.drop(columns=columns_to_remove, inplace=True)

# Rename the column "Publication Year" to "Year"
df.rename(columns={'Publication Year': 'Year'}, inplace=True)

# Add a column with the reviewer name
df['Reviewer Name'] = 'Julius Pfadt'

# Reorder columns to make "Reviewer Name" the first column
df = df.loc[:, ['Reviewer Name', 'Journal', 'Year', 'Title', 'Authors', 'DOI', 'PDF Link']]  #

# Write the result to another CSV file
df.to_csv(output_csv_path, index=False)


