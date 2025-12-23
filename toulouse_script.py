
# The objective of this script is to explore the dataset toulouse_public_library_loans.

import pandas as pd
import os

# First, let's try to load the data
os.chdir("./documents/datasets/toulouse_public_library_loans_dataset")

toulouse = pd.read_csv(os.listdir()[0], sep = ";")
toulouse.head()
# Let's obtain the column names
toulouse.columns.values
len(toulouse.columns.values)
toulouse.shape
# The dataset has 21446 rows and 11 columns.

# Now let's explore each one of this columns to see what each one of them contains.

# 1 Variable 'year'

toulouse['year'].head()
# Type is float64 maybe it can be converted to int
toulouse['year'].min()
toulouse['year'].max()
[toulouse['year'].min(), toulouse['year'].max()]
# It's range goes from 2011 to 2024
# How many observations have each year?
toulouse['year'].value_counts()

# Let's try to create a pandas dataframe with three columns, one for the 
# years, other for the counts, and the third for the relative frequencies.

# Note: sort values before create the dataframe
year_counts = toulouse["year"].value_counts()
years_df = pd.DataFrame({"year": list(year_counts.index), "count": year_counts.values, 
                      "percentage": round(100*year_counts/year_counts.sum(), 2).values})

year_counts.plot.bar(x='year', y='count', rot = 45)

# Need to remove the float part from the years.
# Option 1
test = list(map(int, [2.5, 7.1, 8.0]))
print(test)

test2 = list(map(int, years_df.year))
print(test2)

# Option 2
years_df.year.apply(int)

# Option 2 only can be used when the dataframe already exists, so let's use the
# first one.
list(map(int, year_counts.index))
years_df = pd.DataFrame({"year": list(map(int, year_counts.index)), "count": year_counts.values, 
                      "percentage": round(100*year_counts/year_counts.sum(), 2).values})

years_df.plot.bar(x='year', y='count', rot = 45, title = "Observations registered per year")
# The year with more observations is 2021 and the one with less is 2013. 

# 2 Variable 'nb_loans'

toulouse['nb_loans'].head()
# It seems to contain the number of loans for each book.
print([toulouse['nb_loans'].min(), toulouse['nb_loans'].max()])

# It has any missing values?

toulouse['nb_loans'].isnull().sum()
toulouse['nb_loans'].notnull().sum() == toulouse.shape[0]

[toulouse['nb_loans'].quantile(0.25), toulouse['nb_loans'].quantile(0.50), 
 toulouse['nb_loans'].quantile(0.75), toulouse['nb_loans'].quantile(0.99)]

# 25% of the observations have a value has much as 45, 50% take a value of 132
# or less and 75% of them take a value as much as 182. 99% of observations take 
# a number of loans lesser than 706.55, so the maximum of 4907 seems to be a
# really extreme value.

toulouse['nb_loans'].plot.hist()

# 3 Variable 'title'

toulouse['title'].head()

# It contains the titles of the books.
# Check that no title is repeated.
# Check that there are no missing values.
# Relate the titles with the previous variable to see which ones are the books
# with more loans.

# Has any missing value?
sum(toulouse['title'].isnull())

# Are there any repeated values?
toulouse['title'].value_counts().head(10)

# Yes, there are many repeated titles, this maybe due to the dataset containing
# different editions of the same book.

# So, how many unique titles there are?
len(toulouse['title'].unique())

# 9458 unique book titles

# Another way of check this
toulouse['title'].value_counts().shape

# Let's try know to group all the books loans with the same title in the same
# observation

toulouse[["title", "nb_loans"]].head()

toulouse['title'].value_counts()
toulouse[toulouse['title'] == "Alice au pays des merveilles"]['title']
len(toulouse[toulouse['title'] == "Alice au pays des merveilles"]['title'])
toulouse[toulouse['title'] == "Alice au pays des merveilles"][['title', 'nb_loans']]
toulouse[toulouse['title'] == "Alice au pays des merveilles"]['nb_loans'].sum()

# For a little practice, first let's try to group the data the "hard way"

# First let's test how to add rows to an empty DataFrame
testFrame = pd.DataFrame({"title" : [], "nb_loans" : []})
addFrame = pd.DataFrame({"title" : ["Alice au pays des merveilles"], 
                         "nb_loans" : [4670]})

testFrame = pd.concat([testFrame, addFrame], ignore_index = True)

# Let's try to add another row
toulouse[toulouse['title'] == 'Peter Pan'][['title', 'nb_loans']]
toulouse[toulouse['title'] == 'Peter Pan']['nb_loans'].sum()
addFrame = pd.DataFrame({"title" : ["Peter Pan"], "nb_loans" : [3879]})
testFrame = pd.concat([testFrame, addFrame], ignore_index = True)


summaryFrame = pd.DataFrame({"title" : [], "nb_loans" : []})
for i in toulouse['title'].unique():
    addFrame = pd.DataFrame({"title" : [i], "nb_loans" : [toulouse[toulouse['title'] == i]['nb_loans'].sum()]})
    summaryFrame = pd.concat([summaryFrame, addFrame], ignore_index = True)


# Let's check it with the values obtained before
summaryFrame.shape
summaryFrame[summaryFrame['title'] == "Alice au pays des merveilles"]
summaryFrame[summaryFrame['title'] == "Peter Pan"]
# Looks ok.
summaryFrame.sort_values(by = ['nb_loans'], ascending = False).head(50)

# Now let's try the "easy way"
summaryFrame2 = toulouse[["title", "nb_loans"]].groupby(['title']).sum()
summaryFrame2.sort_values(by = ['nb_loans'], ascending = False).head(50)

sorted_values1 = summaryFrame.sort_values(by = ['nb_loans'], ascending = False).head(50)['nb_loans']
sorted_values2 = summaryFrame2.sort_values(by = ['nb_loans'], ascending = False).head(50)['nb_loans']

sum(sorted_values1.values == sorted_values2.values)

# Let's check now the whole dataframe
sorted_values1 = summaryFrame.sort_values(by = ['nb_loans'], ascending = False)['nb_loans']
sorted_values2 = summaryFrame2.sort_values(by = ['nb_loans'], ascending = False)['nb_loans']
sum(sorted_values1.values == sorted_values2.values)
# nb_loans ok, now let's check the titles.
sorted_values1 = summaryFrame.sort_values(by = ['nb_loans'], ascending = False)['title'].values
sorted_values2 = summaryFrame2.sort_values(by = ['nb_loans'], ascending = False).index.values
sum(sorted_values1 == sorted_values2)
# Only 1330 have the same value
# Maybe write them to a txt file to check the titles
os.chdir('../../codes/python/toulouse_dataset')
with open("check_titles.txt", "w") as file:
    for i in range(0, len(sorted_values1)):
        file.write(str(i))
        file.write("\t")
        file.write(sorted_values1[i])
        file.write("\t\t\t")
        file.write(sorted_values2[i])
        file.write("\n")

# Problem spotted in value located at position 702.
summaryFrame.iloc[[702]]
summaryFrame2.iloc[[702]]

sorted_values1[702]
sorted_values2[702]

# Let's try to write the txt file again, now with the number of loans also.
summaryFrame_sorted = summaryFrame.sort_values(by = "nb_loans", ascending = False)
summaryFrame2_sorted = summaryFrame2.sort_values(by = "nb_loans", ascending = False)

os.chdir('../../codes/python/toulouse_dataset')
with open("check_titles.txt", "w") as file:
    for i in range(0, summaryFrame_sorted.shape[0]):
        file.write(str(i))
        file.write("\t")
        file.write(summaryFrame_sorted.iloc[i]["title"])
        file.write("\t")
        file.write(str(int(summaryFrame_sorted.iloc[i]["nb_loans"])))
        file.write("\t\t\t|")
        file.write(summaryFrame2_sorted.iloc[i].name)
        file.write("\t")
        file.write(str(int(summaryFrame2_sorted.iloc[i].values)))
        file.write("\n")

# The problem seems to be dued by the alphabetical order of the titles, 
# titles with the same number of loans appear in different order in both 
# dataframes. So let's try to sort the dataframe summaryFrame also by the 
# titles column.

summaryFrame_sorted3 = summaryFrame.sort_values(by = ["nb_loans", "title"], ascending = [False, True])
# This time let's try to convert summaryFrame2 into a two columns dataframe.
summaryFrame2_2 = pd.DataFrame({"title" : summaryFrame2.index, "nb_loans" : summaryFrame2["nb_loans"].values})
summaryFrame_sorted4 = summaryFrame2_2.sort_values(by = ["nb_loans", "title"], ascending = [False, True])

sum(summaryFrame_sorted3["nb_loans"].values == summaryFrame_sorted4["nb_loans"].values)
sum(summaryFrame_sorted3["title"].values == summaryFrame_sorted4["title"].values)
# Now, both are ok.

summaryFrame_sorted3.iloc[702]
summaryFrame_sorted4.iloc[702]
# Observation 702 have now not only the same number of loans, but also the 
# same titles.

# Now we can obtain the 50 titles with more loans.
summaryFrame_sorted3.head(50)

# 4 Variable 'author'

toulouse['author'].head()

# As expected it contains the names of the authors.

# Has any missing value?

sum(toulouse['author'].isnull())
# One of the author names seems to be missing.
toulouse[toulouse['author'] == None].index

toulouse[toulouse['author'].isnull() == True].index
toulouse.iloc[14493]['author']
toulouse.iloc[14493]['title']
toulouse.iloc[14493]

toulouse.loc[14493, 'author'] = 'unknown'

# Let's see how many different authors are registered in the dataset.
len(toulouse['author'].unique())

# 50 authors most readed
summaryAuthors = toulouse[["author", "nb_loans"]].groupby(['author']).sum()
summaryAuthors = summaryAuthors.sort_values(by = ['nb_loans'], ascending = False)
summaryAuthors.head(50)

# Let's reclassify the observations with an author '-' as 'unknown'.

indexes = toulouse[toulouse['author'] == '-'].index
toulouse.loc[indexes, 'author'] = 'unknown'

# Let's summarize again
summaryAuthors = toulouse[["author", "nb_loans"]].groupby(['author']).sum()
summaryAuthors = summaryAuthors.sort_values(by = ['nb_loans'], ascending = False)
summaryAuthors.head(20)

# Books of the author with more loans

toulouse[toulouse['author'] == "Saint-Mars, Dominique de"]["title"].unique()
























