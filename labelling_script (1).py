#!/usr/bin/env python
# coding: utf-8

# In[1]:


INPUT_FILE = 'input_data.xlsx'
OUTPUT_FILE = 'output_data.xlsx'


# In[2]:


from datetime import datetime

import pandas as pd

pd.options.display.max_rows = 999
pd.options.display.max_columns = 999


# In[3]:


# READ INPUT FILE
df = pd.read_excel(INPUT_FILE)
print(df.shape)
df.head()


# In[4]:


# KEEPING ONLY RELEVANT COLUMNS FOR OUR PROBLEM
df = df [
    ['Car Name', 'Car URL', 'Price', 'Description', 'cylinders',
     'fuel', 'odometer', 'title status', 'transmission', 'type',
     'drive', 'paint color', 'condition', 'size', 'VIN',]
]


# # Data Preprocessing

# In[5]:


from re import sub


def process_prices(x):
    # PROCESSING PRICE STRING
    # $1,600 -> 1600.00
    value = None
    if pd.notna(x):
        try:
            value = float(sub(r'[^\d.]', '', x))
        except ValueError:
            value = None
    return value


def process_list_type_columns(x):
    # PROCESSING COLUMNS WHICH ARE LIST TYPE AND BEING READ AS STRING
    value = None
    if pd.notna(x):
        value = eval(x)
        value = value[0].strip()
    return value


# In[6]:


# PROCESSING EACH COLUMN

df['Price'] = df['Price'].apply(process_prices)
df['cylinders'] = df['cylinders'].apply(process_list_type_columns)
df['fuel'] = df['fuel'].apply(process_list_type_columns)
df['odometer'] = df['odometer'].apply(process_list_type_columns)
df['title status'] = df['title status'].apply(process_list_type_columns)
df['transmission'] = df['transmission'].apply(process_list_type_columns)
df['type'] = df['type'].apply(process_list_type_columns)
df['drive'] = df['drive'].apply(process_list_type_columns)
df['paint color'] = df['paint color'].apply(process_list_type_columns)
df['condition'] = df['condition'].apply(process_list_type_columns)
df['size'] = df['size'].apply(process_list_type_columns)
df['VIN'] = df['VIN'].apply(process_list_type_columns)


# ## Text Preprocessing

# In[7]:


from cleantext import clean


# In[8]:


df['Clean_Description'] = df['Description'].apply(lambda x: clean(x, no_line_breaks=True))


# ## Call or Text Flag

# In[9]:


# CHECK IF LISTING CONTAINS PHONE NUMBER
phone_regex = r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}'

contains_call_text = df['Clean_Description'].str.contains(phone_regex, case=False) == True

df['Call_Text_Flag'] = False
df.loc[contains_call_text, 'Call_Text_Flag'] = True


# # Prices

# In[10]:


# FIND EXTREME QUANTILES FOR PRICES
low_quantile = df['Price'].quantile(0.05)
high_quantile = df['Price'].quantile(0.95)
print(low_quantile, high_quantile)


# In[11]:


extreme_prices = (df['Price'] <= low_quantile) | (df['Price'] >= high_quantile)

df['Extreme_Price_Flag'] = False
df.loc[extreme_prices, 'Extreme_Price_Flag'] = True


# # Marking Scams

# In[12]:


df['Probable_Scams'] = df['Extreme_Price_Flag'] & ~df['Call_Text_Flag']


# In[13]:


df.to_excel(OUTPUT_FILE, index=False)



