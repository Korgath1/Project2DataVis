import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("Friendship Network Visualization and Analysis")

G = nx.Graph()
G.add_edges_from([
    ("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "Charlie"),
    ("Charlie", "Diana"), ("Diana", "Eve"), ("Bob", "Diana"),
    ("Frank", "Eve"), ("Eve", "Ian"), ("Diana", "Ian"),
    ("Ian", "Grace"), ("Grace", "Hannah"), ("Hannah", "Jack"),
    ("Grace", "Jack"), ("Charlie", "Frank"), ("Alice", "Eve"),
    ("Bob", "Jack")
])

st.header("Network Graph")
pos = nx.spring_layout(G, seed=42)
betweenness = nx.betweenness_centrality(G)

most_influential = max(betweenness, key=betweenness.get)
st.write(f"**Most influential person (highest betweenness centrality):** {most_influential}")
# Color nodes
color_map = ["red" if node == most_influential else "lightblue" for node in G.nodes()]

fig, ax = plt.subplots(figsize=(10, 7))
nx.draw(
    G, pos,
    with_labels=True,
    node_color=color_map,
    node_size=900,
    font_size=10,
    edge_color="gray",
    ax=ax
)
ax.set_title("Network with Most Influential Person Highlighted (Red)")
st.pyplot(fig)


st.header("Betweenness Centrality Table")
df = pd.DataFrame({
    "Person": list(betweenness.keys()),
    "Betweenness": list(betweenness.values())
})

df = df.sort_values(by="Betweenness", ascending=False)

st.dataframe(df)