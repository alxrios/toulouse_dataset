
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
# second one.
list(map(int, year_counts.index))
years_df = pd.DataFrame({"year": list(map(int, year_counts.index)), "count": year_counts.values, 
                      "percentage": round(100*year_counts/year_counts.sum(), 2).values})

years_df.plot.bar(x='year', y='count', rot = 45, title = "Observations registered per year")
# The year with more observations is 2021 and the one with less is 2013. 








