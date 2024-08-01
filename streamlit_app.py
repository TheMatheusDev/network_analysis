import streamlit as st
import networkx as nx
import pandas as pd

G = nx.read_graphml('TI11 Playoffs Teams.graphml')

# Streamlit app
st.title("Network Analysis of The International 2021 - Playoffs Teams")

# Degree Distribution
st.header("Distribuição de Degree")
degrees = dict(nx.degree(G))
nx.set_node_attributes(G, name='degree', values=degrees)

degree_df = pd.DataFrame(G.nodes(data='degree'), columns=['node', 'degree'])
degree_df = degree_df.sort_values(by='degree', ascending=False)
st.write(degree_df)

# Adjacency Matrix
st.header("Matriz de Adjacência")
adjacency_matrix = nx.adjacency_matrix(G)
st.write(adjacency_matrix.todense())

# Diameter and Periphery
st.header("Diâmetro e Periferia")
strongs = sorted(nx.strongly_connected_components(G), key=len, reverse=True)
subgrafos = [G.subgraph(s) for s in strongs]
diameter = nx.diameter(subgrafos[0])
periphery = nx.periphery(subgrafos[0])
st.write(f"Diâmetro: {diameter}")
st.write(f"Periferia: {periphery}")

# Assortativity
st.header("Assortatividade")
assortativity = nx.degree_assortativity_coefficient(G)
st.write(f"Coeficiente de Assortatividade: {assortativity}")

# Clustering Coefficient
st.header("Coeficiente de Clustering")
st.subheader("Coeficiente de Clustering Local")
selected_nodes = st.multiselect("Selecione os nós:", list(G.nodes()))
for node in selected_nodes:
  st.write(f"Coeficiente de Clustering para {node}: {nx.clustering(G, node)}")

st.subheader("Coeficiente de Clustering Global")
global_clustering = nx.average_clustering(G)
st.write(f"Coeficiente de Clustering Global: {global_clustering}")

# Connected Components
st.header("Componentes Conectados")
st.subheader("Componentes Fortemente Conectados")
num_strong_components = nx.number_strongly_connected_components(G)
st.write(f"Quantidade de Componentes Fortemente Conectados: {num_strong_components}")

strong_components = list(nx.strongly_connected_components(G))
strong_components_table = pd.DataFrame({'Component': strong_components})
st.write(strong_components_table)

st.subheader("Componentes Fracamente Conectados")
num_weak_components = nx.number_weakly_connected_components(G)
st.write(f"Quantidade de Componentes Fracamente Conectados: {num_weak_components}")

weak_components = list(nx.weakly_connected_components(G))
weak_components_table = pd.DataFrame({'Component': weak_components})
st.write(weak_components_table)

# Centrality Measures
st.header("Medidas de Centralidade")

centrality_measures = {
"Eigenvector Centrality": nx.eigenvector_centrality,
"Closeness Centrality": nx.closeness_centrality,
"Degree Centrality": nx.degree_centrality,
"Betweenness Centrality": nx.betweenness_centrality,
}

selected_measure = st.selectbox("Selecione uma Medida de Centralidade", list(centrality_measures.keys()))

if selected_measure:
    centrality = centrality_measures[selected_measure](G)
    centrality_df = pd.DataFrame(centrality.items(), columns=['Node', selected_measure])
    centrality_df = centrality_df.sort_values(by=selected_measure, ascending=False)
    st.write(centrality_df)
