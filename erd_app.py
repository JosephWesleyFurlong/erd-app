import streamlit as st
import pandas as pd

# Load the data (for demonstration, you might need to replace this with actual data loading logic)
# Assuming df_keys_clean.csv is the cleaned file
@st.cache
def load_data():
    return pd.read_csv('df_keys_clean.csv')

df_keys_clean = load_data()

# Title of the app
st.title('Entity Relationship Explorer')

# Allow user to select a mode: either by table or by key
mode = st.radio("Select mode of exploration:", ('Table', 'Key'))

# Option 1: Filter by table
if mode == 'Table':
    # Show a dropdown with unique table names
    selected_table = st.selectbox('Select a Table', df_keys_clean['table_name_filled'].unique())
    
    # Display all references to the selected table
    st.subheader(f"References for Table: {selected_table}")
    references = df_keys_clean[(df_keys_clean['table_name_filled'] == selected_table) | (df_keys_clean['ref_table'] == selected_table)]
    st.write(references[['table_name_filled', 'column', 'ref_table', 'ref_column']])

# Option 2: Filter by key (ref_column)
elif mode == 'Key':
    # Show a dropdown with unique keys (ref_columns)
    selected_key = st.selectbox('Select a Key (Foreign Column)', df_keys_clean['ref_column'].unique())
    
    # Display all references to the selected key
    st.subheader(f"References for Key: {selected_key}")
    references = df_keys_clean[df_keys_clean['ref_column'] == selected_key]
    st.write(references[['table_name_filled', 'column', 'ref_table', 'ref_column']])

# Deploy instructions
st.write("Deploy this app to [Streamlit Cloud](https://streamlit.io/cloud) to share it with others.")
