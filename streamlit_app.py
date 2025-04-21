#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph using NetworkX
def build_graph(weight_type="miles"):
    G = nx.DiGraph()

    # Common edges, each with their weights
    edges = [
        ("Chicago", "Mclain", 40), ("Chicago", "Aurora", 60), ("Chicago", "Parker", 50),
        ("Mclain", "Aurora", 10), ("Mclain", "Smallville", 70),
        ("Aurora", "Parker", 20), ("Aurora", "Smallville", 55), ("Aurora", "Farmer", 40),
        ("Parker", "Farmer", 50),
        ("Smallville", "Farmer", 10), ("Smallville", "Bayview", 60),
        ("Farmer", "Bayview", 80),
    ]

    # Add weights based on type (miles, cost, or time)
    for u, v, val in edges:
        weight = val
        if weight_type == "cost":
            weight = val * 1.5  # Example: cost is 1.5 times the miles
        elif weight_type == "time":
            weight = val * 2  # Example: time is 2 times the miles
        G.add_edge(u, v, weight=weight)

    return G

# Draw network
def draw_graph(G, path=None):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    st.pyplot(plt)

# Streamlit interface
st.title("📍Shortest Path Finder: Town to Town")

option = st.selectbox(
    "Choose what the numbers represent:",
    ("Miles", "Cost", "Time")
)

if option == "Miles":
    weight_type = "miles"
elif option == "Cost":
    weight_type = "cost"
else:
    weight_type = "time"

G = build_graph(weight_type=weight_type)

# Shortest path and distance
path = nx.dijkstra_path(G, source="Origin", target="Destination", weight="weight")
distance = nx.dijkstra_path_length(G, source="Origin", target="Destination", weight="weight")

st.subheader("🗺️ Network Graph")
draw_graph(G, path)

st.subheader("📌 Shortest Path Result")
st.write(" ➡️ → ".join(path))
st.write(f"Total {option.lower()}: **{distance:.2f}**")

