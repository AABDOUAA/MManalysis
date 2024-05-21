import pandas as pd

def uniCollabs(basedf, uniName):

  substring = uniName

  basedf = basedf[basedf['Affiliations'].str.contains(substring)]

  collabList = basedf['Affiliations'].value_counts()
  uniList = basedf['Affiliations'].str.split(';')
  a = collabList.to_numpy()
  dfCollabs = pd.DataFrame({'Institutions': collabList.keys(), 'Occurences': a})
  dfCollabsUnpacked = []
  dfCollabsUnpacked = pd.DataFrame()

  # dfCollabs['Occurences'] = len(dfCollabs['Institutions'].list) - have to use length of split list

  for x in range(len(dfCollabs)):
      names = dfCollabs['Institutions'].iloc[x].split(';')
      numbers = np.repeat(len(dfCollabs['Institutions'].iloc[x].split(';')) - 1, len(dfCollabs['Institutions'].iloc[x].split(';')))
      # names = Leeds_df['Affiliations'].iloc[x].split(';')
      # numbers = np.repeat(len(Leeds_df['Affiliations'].iloc[x].split(';')) - 1,len(Leeds_df['Affiliations'].iloc[x].split(';')))
      dfAdd = pd.DataFrame({'Names': names, 'Numbers': numbers})
      dfCollabsUnpacked = pd.concat([dfCollabsUnpacked, dfAdd], ignore_index = True)

  result_df = dfCollabsUnpacked.groupby('Names').sum().reset_index()
  sorted_df = result_df.sort_values(by='Numbers', ascending = False)

  return sorted_df

# this returns a dataframe of the publication collaboration patterns surrounding a given university search term

def dfCollabs(basedf, uniName):

  basedf = basedf[basedf['Affiliations'].str.contains(uniName)]

  collabList = basedf['Affiliations'].value_counts()
  uniList = basedf['Affiliations'].str.split(';')
  a = collabList.to_numpy()
  title = basedf['Title']
  dfCollabs = pd.DataFrame({'Institutions': collabList.keys(), 'Occurences': a, 'Title': title})
  return dfCollabs

# this returns a datframe of the set of collaborations that a university has been involved in within the dataset
# each having an occurence of 1 - ie this is the unpacked form of the previous function
# perhaps it would also be useful to capture titles at this stage (originally basedf was dfA - which is the originally read csv)
