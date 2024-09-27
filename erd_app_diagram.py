import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Load the data
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
    
    # Create a network graph for the selected table
    G = nx.DiGraph()  # Directed graph
    
    # Add nodes and edges for the relationships
    for index, row in references.iterrows():
        G.add_node(row['table_name_filled'], label=row['table_name_filled'])
        G.add_node(row['ref_table'], label=row['ref_table'])
        G.add_edge(row['table_name_filled'], row['ref_table'], label=f"{row['column']} -> {row['ref_column']}")
    
    # Create network visualization using pyvis
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    
    # Save and display the graph
    net.save_graph('network_graph.html')
    HtmlFile = open('network_graph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=600)

# Option 2: Filter by key (ref_column)
elif mode == 'Key':
    # Show a dropdown with unique keys (ref_columns)
    selected_key = st.selectbox('Select a Key (Foreign Column)', df_keys_clean['ref_column'].unique())
    
    # Display all references to the selected key
    st.subheader(f"References for Key: {selected_key}")
    references = df_keys_clean[df_keys_clean['ref_column'] == selected_key]
    st.write(references[['table_name_filled', 'column', 'ref_table', 'ref_column']])
    
    # Create a network graph for the selected key
    G = nx.DiGraph()  # Directed graph
    
    # Add nodes and edges for the relationships
    for index, row in references.iterrows():
        G.add_node(row['table_name_filled'], label=row['table_name_filled'])
        G.add_node(row['ref_table'], label=row['ref_table'])
        G.add_edge(row['table_name_filled'], row['ref_table'], label=f"{row['column']} -> {row['ref_column']}")
    
    # Create network visualization using pyvis
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    
    # Save and display the graph
    net.save_graph('network_graph.html')
    HtmlFile = open('network_graph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=600)

# Deploy instructions
st.write("Deploy this app to [Streamlit Cloud](https://streamlit.io/cloud) to share it with others.")
