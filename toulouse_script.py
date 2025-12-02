
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

