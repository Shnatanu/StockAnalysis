# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:26:29 2024

@author: Shantanu R Nakhate
Linked In Contact : https://www.linkedin.com/in/shantanu-nakhate-53b54615/ 
DM me if you are interested in doing data analytics or in developing algorithms.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to convert datetime format
def convert_datetime_format(datetime_str):
    return datetime_str.split()[0]

# Data path
data_path = r"" # insert the data path for your csv here.

# List of CSV file names
csv_files = [
    "BSE.csv",#1
    "IRFC.csv",#2
    "HUDCO.csv",#3
    "MRPL.csv",#4
    "IRCON.csv",#5
    "RECLTD.csv",#6
    "KALYANKJIL.csv",#7
    "RVNL.csv",#8
    "SJVN.csv",#9
    "BHEL.csv",#10
    "ZOMATO.csv",#11
    "SOBHA.csv",#12
    "NBCC.csv",#13
    "TATAMTRDVR.csv",#14
    "SWANENERGY.csv",#15
    "FACT.csv",#16
    "OLECTRA.csv",#17
    "APARINDS.csv",#18
    "NLCINDIA.csv",#19
    "HINDCOPPER.csv"#20
    # Add more file names as needed
]

# Initialize a dictionary to store net values for each file
net_values = {}

# Loop through each CSV file
for file_name in csv_files:
    file_path = os.path.join(data_path, file_name)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_name} does not exist.")
        continue

    # Read CSV file
    df = pd.read_csv(file_path)

    # Convert datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'].apply(convert_datetime_format))

    # Filter data from 3rd April 2023
    df = df[df['Datetime'] >= '2023-04-03']

    # Calculate initial quantity
    initial_amount = 100000
    initial_price = df.loc[df['Datetime'] == '2023-04-03', 'close'].values[0]
    initial_quantity = initial_amount / initial_price

    # Calculate net values
    df['Quantity'] = initial_quantity
    df['Net Value'] = df['close'] * df['Quantity']

    # Store net values for the file
    net_values[file_name] = df.set_index('Datetime')['Net Value']

# Combine net values of all files
combined_df = pd.DataFrame(net_values).fillna(method='ffill').fillna(0)
combined_df['Total Net Value'] = combined_df.sum(axis=1)

# Initialize an empty list to store vol_net_values
vol_net_values_list = []

# Iterate over each row in the combined DataFrame starting from the 15th day and going backward
for i in range(15, len(combined_df)):
    vol_net_values = (combined_df.iloc[i] - combined_df.iloc[i - 15])*100/combined_df.iloc[i - 15]
    vol_net_values_list.append(vol_net_values)

# Concatenate the list of vol_net_values into a DataFrame
vol_net_values_df = pd.concat(vol_net_values_list, axis=1).transpose()
vol_net_values_df.index = combined_df.index[15:]  # Set datetime as index




# Plot date time vs. net value
plt.figure(figsize=(12, 6))
plt.plot(combined_df.index, combined_df['Total Net Value'], color='navy', marker='o', linestyle='-', linewidth=1.5, markersize=4)
plt.title('Net Value Over Time', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Net Value', fontsize=14)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plot Datetime vs. vol_net_values with improved quality
plt.figure(figsize=(12, 8), dpi=120)  # Increased figure size and DPI for better quality
for col in vol_net_values_df.columns:
    plt.plot(vol_net_values_df.index, vol_net_values_df[col], linestyle='-', alpha=0.5, label=col)
plt.title('Time vs. Volatility 15 day Period', fontsize=18)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Volatility 15 day Period', fontsize=14)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()