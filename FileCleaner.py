import time
import requests
import json
import csv


import pandas as pd

# Read in the original CSV file
df = pd.read_csv('Extract5.csv', encoding='latin-1')

# Group the data by userID and get the last prompt for each user
last_prompt_df = df.groupby('User ID').tail(1)

# Write the new CSV file with unique userID and last prompt
last_prompt_df[['User ID', 'Prompt']].drop_duplicates().to_csv('Extract5_Cleaned.csv', index=False)
