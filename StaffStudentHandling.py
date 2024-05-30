import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def find_fuzzy_match(name_to_match, uni_names):
  best_match = process.extractOne(name_to_match, uni_names)
  return best_match[0], best_match[1]

def matchNetworkUniToHEP(network, dataFrame):
  dataFrame['HE Provider']
  dfNames = []

  # Step 1: Create an empty DataFrame with the desired columns
  dfNames = pd.DataFrame(columns=['Uni', 'Similarity', 'Matched HEP'])

  rows = []

  for x in list(network):
    best_match, highest_similarity = find_fuzzy_match(x, dataFrame['HE Provider'])

    new_row = {
          'Uni': x,
          'Similarity': highest_similarity,
          'Matched HEP': best_match
    }

    rows.append(pd.Series(new_row))

  dfNames = pd.concat([dfNames, pd.DataFrame(rows)], ignore_index=True)

  return dfNames

  def create_sets_of_shared_objects(df, object_col='Uni', value_col='Matched HEP'):
    # Group by the associated value and create sets of objects
    grouped_sets = df.groupby(value_col)[object_col].apply(set)

    # Convert to list of sets
    list_of_sets = grouped_sets.tolist()

    return list_of_sets

