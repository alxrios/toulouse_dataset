
# The objective of this script is to explore the dataset toulouse_public_library_loans.

import pandas as pd
import os
# import matplotlib.pyplot as plt
import numpy as np
import re

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

# 5 Variable 'publisher'

toulouse['publisher'].head()

# Has any missing value?
sum(toulouse['publisher'].isnull())

# At first glance there are no missing values in this variable.

# How many unique publishers are registered in the variable?
len(toulouse['publisher'].unique())

# Which are the publishers with more books in the dataset?
toulouse['publisher'].value_counts().head(20)

# If the counts are ordered by descending order, counts.values must be equal
# to sorted(counts.values)
counts = toulouse['publisher'].value_counts()
sum(counts.values == sorted(counts.values, reverse = True)) == counts.values.shape[0]

# Again let's reclassify the values accounted with a '-' as 'unknown'.

indexes = toulouse[toulouse['publisher'] == '-'].index
toulouse.loc[indexes, 'publisher'] = 'unknown'
# Let's obtain again the counts
toulouse['publisher'].value_counts().head(20)
# We can see that almost all the 20 publishers with more presence in the dataset
# correspond to film production companies.

# Let's see the titles of the publisher with more observations in the dataset.
toulouse[toulouse['publisher'] == "[S.l] : Buena Vista Home Intertainment, 2006"]['title'].unique()

# 6 Variable 'classification'

toulouse['classification'].head()
len(toulouse['classification'].unique())

# Are missing values present in the variable?
sum(toulouse['classification'].isnull())
# 5 Missings obtained, let's see them
indexes = toulouse[toulouse['classification'].isnull()].index
toulouse.loc[indexes]

# Let's write the rows into a txt file so we can fully see them.
check_frame = toulouse.loc[indexes]
os.chdir("../../codes/python/toulouse_dataset")
with open('check_frame.txt', 'w') as file:
    for i in range(0, check_frame.shape[0]):
        for j in range(0, check_frame.shape[1]):
            file.write(str(check_frame.iloc[i][j]))
            file.write("|")
        file.write("\n")
        

# All the observations have the same title, let's see if we can find more
# observations with that title in the dataset.

title = check_frame.iloc[0]['title']
toulouse[toulouse['title'] == title].index == check_frame.index

# Let's try to find some "lazy" match with the title
re.findall("minuscule", title, re.I)

for i in range(0, toulouse.shape[0]):
    title = toulouse.iloc[i]['title']
    # re.findall("minuscule", toulouse.iloc[i]['title'], re.I)
    if len(re.findall("minuscule", title, re.I)) > 0:
        print(i)


# So seems that there are more observations that could match the title in a more
# 'lazy' way.
title_indexes = []
for i in range(0, toulouse.shape[0]):
    title = toulouse.iloc[i]['title']
    if len(re.findall("minuscule", title, re.I)) > 0:
        title_indexes.append(i)

# Now let's see the titles
toulouse.iloc[title_indexes]['title']

# Let's write them into a txt file to see them well.
with open('check_titles.txt', 'w') as file:
    for i in title_indexes:
        file.write(toulouse.iloc[i]['title'])
        file.write("\n")

# Now let's write their classification also
with open('check_titles.txt', 'w') as file:
    for i in title_indexes:
        file.write(toulouse.iloc[i]['title'])
        file.write("\t|")
        file.write(str(toulouse.iloc[i]['classification']))
        file.write("\n")

# As can be seen, other DVDs of the same season take the value 'A MINU', so
# let's replace the missing values with this one.
toulouse.loc[indexes]['classification'] = 'A MINU'

# 7 Variable 'library'
toulouse['library'].head()
toulouse['library'].unique()
# It seems there are no missing values
sum(toulouse['library'].isnull())
# Confirmed, no missing values in the variable.
toulouse['library'].value_counts()

toulouse[['library', 'nb_loans']].groupby('library').sum()
# Note: create a dataframe with this information and the corresponding percentage
# for the nb_loans variable. Also quit library from being a row index and put
# it has a column.
libraries = toulouse[['library', 'nb_loans']].groupby('library').sum().index.values
num_loans = toulouse[['library', 'nb_loans']].groupby('library').sum().values
num_loans.shape = (9,)
libFrame = pd.DataFrame({"library" : libraries, "num_loans" : num_loans})
percentage = round(100*libFrame['num_loans']/libFrame['num_loans'].sum(), 2)
libFrame = libFrame.assign(percentage = percentage)
print(libFrame.sort_values(by = "num_loans", ascending = False))

# Author or book with more loans for each library?
toulouse[toulouse['library'] == 'CABANIS']['author'].value_counts().head()
toulouse[toulouse['library'] == 'EMP']['author'].value_counts().head()
toulouse[toulouse['library'] == 'COL']['author'].value_counts().head()
toulouse[toulouse['library'] == 'CYP']['author'].value_counts().head()
toulouse[toulouse['library'] == 'MGM']['author'].value_counts().head()
toulouse[toulouse['library'] == 'FAB']['author'].value_counts().head()
toulouse[toulouse['library'] == 'PRA']['author'].value_counts().head()
toulouse[toulouse['library'] == 'PERIGORD']['author'].value_counts().head()
toulouse[toulouse['library'] == 'EXU']['author'].value_counts().head()

for i in toulouse['library'].unique():
    print("library: ", i, "\n")
    print(toulouse[toulouse['library'] == i]['title'].value_counts().head(2))
    print("--------------------------------------")


for i in toulouse["library"].unique():
    print("library", "\n")
    print(toulouse[toulouse['library'] == i]['author'].value_counts().head(2))
    print("--------------------------------------")


toulouse[toulouse['library'] == i][['author', 'nb_loans']].groupby('author').sum().sort_values(by = 'nb_loans', ascending = False).head(2)

for i in toulouse["library"].unique():
    print("library", i, "\n")
    print(toulouse[toulouse['library'] == i][['author', 'nb_loans']].groupby('author').sum().sort_values(by = 'nb_loans', ascending = False).head(2))
    print("--------------------------------------")

for i in toulouse["library"].unique():
    print("library: ", i, "\n")
    print(toulouse[toulouse['library'] == i][['title', 'nb_loans']].groupby('title').sum().sort_values(by = 'nb_loans', ascending = False).head(2))
    print("--------------------------------------")


# 8 Variable 'spine_label'

toulouse['spine_label'].head()
len(toulouse['spine_label'].unique())
sum(toulouse['spine_label'].isnull())
# No values classified as null.

toulouse['spine_label'].value_counts().head(10)


# 9 Variable 'audience'

toulouse['audience'].head()
len(toulouse['audience'].unique())
toulouse['audience'].unique()
toulouse['audience'].value_counts()
toulouse['audience'].value_counts()/toulouse['audience'].value_counts().sum()

audience = toulouse['audience'].unique()
counts = toulouse['audience'].value_counts().values
percentage = (100*counts/counts.sum()).round(2)
audienceFrame = pd.DataFrame({"audience" : audience, "counts" : counts, 
                              "percentage" : percentage})

audienceFrame

# 10 Variable 'media_subtype'

toulouse['media_subtype'].head()
len(toulouse['media_subtype'].unique())
sum(toulouse["media_subtype"].isnull())
# 4244 nan values
toulouse['media_subtype'].value_counts()

media_subtype = toulouse['media_subtype'].value_counts().index
counts = toulouse['media_subtype'].value_counts().values
percentage = (100*counts/counts.sum()).round(2)
mediasFrame = pd.DataFrame({"media_subtype" : media_subtype, 
                            "counts" : counts, "percentage" : percentage})

# Titles of the observations with nan values?
toulouse[toulouse['media_subtype'].isnull()]['title'].value_counts()
# So there are some that appear more than once. All the appearances are missing
# for this column?
toulouse[toulouse['title'] == 'Alice au pays des merveilles']['media_subtype'].value_counts(dropna = False)
# How many titles have a count bigger than 1?
counts = toulouse[toulouse['media_subtype'].isnull()]['title'].value_counts().values
sum(counts > 1)
# 1002 titles to inspect...
title_counts = toulouse[toulouse['media_subtype'].isnull()]['title'].value_counts()
# Now we store the titles of the media with more than one appearance to observe
# if they take a value different than nan when repeated.
title_names = title_counts[counts > 1].index
# Let's begin inspecting the first ten
for i in title_names[0:10]:
    print(toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby(['title']).value_counts(dropna = False))

# All the titles have two categories?
i = "Rebelle"
print(toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby(['title']).value_counts(dropna = False).shape[0])
# Let's try to store all the shapes in an array and see if all are equal to two
shapes = []
for i in title_names:
    shapes.append(toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby(['title']).value_counts(dropna = False).shape[0])

shapes = np.array(shapes)
sum(shapes == 2)
sum(shapes == 1)
sum(shapes >= 3)
sum(shapes == 3)
# Only 12 observations take the value 3, let's observe them
for i in title_names[shapes == 3]:
    print(toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby(['title']).value_counts(dropna = False))

# Shapes that take the value one only take the value nan?
# Let's sample one observation for check it.
i = title_names[shapes == 1][0]
print(toulouse[toulouse['title'] == i][['title', 'media_subtype']])
# We can give all the observations with two categories and one being NaN for 
# media_subtype the value of the non-missing one, with the risk of being 
# introducing artificially errors in the variable. In this case we will still
# having 125 observations with missing values for this variable, because we don't
# have any reference for their possible value in the case where the observations
# only take the value NaN, and in the case where are two options available we
# would have to choose between the two without a clear criteria other than choose
# the option with more observations, when there is one.
#
# So let's just proceed to impute the values of the observations with two
# categories for the variable 'media_subtype'.
#
# First we have to store the title, and the media label
for i in title_names[shapes == 2][0:10]:
    print(toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby('title').value_counts())

# Let's try to store the data in an auxiliar dataframe.
replaceFrame = pd.DataFrame({"title" : [], "media_subtype" : []})
# Test how to add row
replaceFrame.loc[0] = ["testTitle", "testMediaType"] 
test = toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby('title').value_counts()
[test.index[0][0], test.index[0][1]]
replaceFrame.loc[1] = [test.index[0][0], test.index[0][1]]

row = 0
for i in title_names[shapes == 2][0:10]:
    replace_data = toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby('title').value_counts()
    replaceFrame.loc[row] = [replace_data.index[0][0], replace_data.index[0][1]]
    row += 1
    
i = replaceFrame['title'][0]
toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['title', 'media_subtype']]

# Let's test one replacement
# toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['title', 'media_subtype']] = replaceFrame.iloc[0]['media_subtype']

toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['media_subtype']]

# One way of achieve the replacement of the values would be
indexes = toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['media_subtype']].index
toulouse.loc[indexes, "media_subtype"] = "test"

# Now let's test it in the 10 test rows of replaceFrame
for i in replaceFrame["title"]:
    indexes = toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['media_subtype']].index
    toulouse.loc[indexes, "media_subtype"] = "test"


# Now replacing by the column media_subtype instead of just "test".
for i in replaceFrame["title"]:
    indexes = toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['media_subtype']].index
    toulouse.loc[indexes, "media_subtype"] = replaceFrame.loc[replaceFrame['title'] == i, 'media_subtype']


# Now let's write a version for the whole dataset
replaceFrame = pd.DataFrame({"title" : [], "media_subtype" : []})
row = 0
for i in title_names[shapes == 2]:
    replace_data = toulouse[toulouse['title'] == i][['title', 'media_subtype']].groupby('title').value_counts()
    replaceFrame.loc[row] = [replace_data.index[0][0], replace_data.index[0][1]]
    row += 1

for i in replaceFrame["title"]:
    indexes = toulouse[toulouse['title'] == i][toulouse['media_subtype'].isnull()][['media_subtype']].index
    toulouse.loc[indexes, "media_subtype"] = replaceFrame.loc[replaceFrame['title'] == i, 'media_subtype'].values[0]























