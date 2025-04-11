import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import re
import os
import tempfile
from collections import Counter
import numpy as np
import random

# Page config
st.set_page_config(
    page_title="Trade Analysis - Word Cloud",
    page_icon="🌎",
    layout="wide"
)

# Title
st.title("North American Trade Analysis - Topic Visualization")
st.markdown("Explore key terms and connections in the trade proposal using word cloud and network graph visualizations.")
st.markdown("---")

# Sidebar
st.sidebar.header("Controls")
max_words = st.sidebar.slider("Maximum Words", 20, 100, 50, 5)
cloud_type = st.sidebar.radio("Visualization Type", ["Word Cloud", "Network Graph"])

# Trade proposal text - extracted from the markdown file
trade_text = """
International trade, particularly between the North American countries of the United States, Canada, and Mexico. 
Understanding the breakdown of international trade in different states of the U.S. and present a visualization 
of the benefits and drawbacks of free trade to different U.S. states. Focus on the potential for tariffs and 
how those would affect the trade conditions and economic indicators of different states.

An interactive online tool that shows the current balance of trade for each U.S. State with Mexico and Canada. 
States color-coded based on their balance of trade with these two countries. States with a negative balance 
of trade with Mexico and Canada (i.e. they have more imports than exports) will be red, and states with a positive 
balance of trade will be green.

Interactive sliders will show a general tariff rate for trade between Mexico, the US, and Canada, assuming that 
the tariffs are reciprocated. This will allow users to adjust hypothetical tariff rates and project how these 
tariff rates would affect the trade situation in each state.

Data will include the current dollar balance of trade data for all 50 U.S. States, along with the most important 
exports and imports for certain states. Special attention to particularly interesting industries or circumstances 
affecting one state. Tariff levels will range from 0% to at least 50%.

Data sources include the WTO, United States Trade Representative, and trade.gov.

The decline of manufacturing capacity has had huge externalities in the Rust Belt and certain New England cities, 
where the social order has been almost completely decimated by the exodus of factory jobs. Cities such as Lawrence, 
Massachusetts and Lowell, Massachusetts have been hard-hit by the closure of mills. The effects are even worse in 
certain Midwestern cities like Detroit, MI or Albany, NY.

Increased globalization has not brought equal prosperity to different regions. The growth of the technological 
sector has been concentrated in places like New York, Boston, and San Francisco, bringing sky-high housing costs, 
yet other regions seem to have been left behind.
"""

# Define custom stopwords
custom_stopwords = [
    "will", "also", "seek", "want", "make", "states", "state", "u.s", "united", "would",
    "the", "and", "of", "to", "in", "that", "is", "for", "on", "with", "by", "as", "this",
    "be", "are", "have", "has", "been", "from", "an", "their", "these", "those", "it", "its",
    "or", "at", "but", "not", "they", "which", "all"
]

# Function to process text
def process_text(text, stopwords):
    # Convert to lowercase and split into words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    # Remove stopwords
    filtered_words = [word for word in words if word not in stopwords]
    # Count word frequency
    word_counts = Counter(filtered_words)
    return word_counts

# Process the text and generate visualization
if cloud_type == "Word Cloud":
    st.header("Word Cloud Visualization")
    st.write("This word cloud highlights the most frequent and important terms in the North American trade analysis proposal.")
    
    # Process text and get word counts
    word_counts = process_text(trade_text, custom_stopwords)
    
    # Take top N words
    top_words = word_counts.most_common(max_words)
    
    # Create a simple matplotlib word cloud
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('white')
    
    # Get the maximum count for normalization
    max_count = max([count for _, count in top_words])
    
    # Random positions for the words
    np.random.seed(42)  # For reproducibility
    positions = {}
    
    for word, count in top_words:
        # Font size based on frequency (normalized)
        font_size = 10 + (count / max_count) * 100
        
        # Try to find a position for the word
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            # Random position
            x = np.random.uniform(0.1, 0.9)
            y = np.random.uniform(0.1, 0.9)
            
            # Check for overlap with existing words
            overlap = False
            for w, (wx, wy, ws) in positions.items():
                # Simple distance check
                dist = np.sqrt((x - wx)**2 + (y - wy)**2)
                if dist < (font_size + ws) / 1000:  # Arbitrary threshold
                    overlap = True
                    break
            
            if not overlap:
                positions[word] = (x, y, font_size)
                placed = True
            
            attempts += 1
    
    # Different colors for the words
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_words)))
    
    # Plot the words
    for i, (word, (x, y, font_size)) in enumerate(positions.items()):
        ax.text(x, y, word, fontsize=font_size, 
                color=colors[i], 
                ha='center', va='center', 
                rotation=np.random.uniform(-30, 30))
    
    # Remove axes and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout(pad=0)
    st.pyplot(fig)
    
    # Save file for download using tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        plt.savefig(tmp_file.name)
        
    # Download option
    with open(tmp_file.name, "rb") as file:
        st.download_button(
            label="Download Word Cloud as PNG",
            data=file.read(),
            file_name="trade_analysis_wordcloud.png",
            mime="image/png"
        )

else:
    st.header("Network Graph of Related Terms")
    st.write("This graph shows connections between important topics in the trade analysis.")
    
    # Process text and get word counts
    word_counts = process_text(trade_text, custom_stopwords)
    
    # Take top N words
    top_words = dict(word_counts.most_common(max_words // 3))
    
    # Create nodes and edges
    G = nx.Graph()
    
    # Add nodes for top words
    for word, count in top_words.items():
        G.add_node(word, size=count*20)
    
    # Process text for graph connections
    words = re.findall(r'\b[a-zA-Z]{3,}\b', trade_text.lower())
    filtered_words = [word for word in words if word not in custom_stopwords]
    
    # Add edges between words that appear close together
    window_size = 3
    for i in range(len(filtered_words) - window_size):
        window = filtered_words[i:i+window_size]
        for j in range(len(window)):
            for k in range(j+1, len(window)):
                word1, word2 = window[j], window[k]
                if word1 in top_words and word2 in top_words:
                    if G.has_edge(word1, word2):
                        G[word1][word2]['weight'] += 1
                    else:
                        G.add_edge(word1, word2, weight=1)
    
    # Visualize the network graph
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.7)
    
    # Draw edges with weights
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.4, edge_color="gray")
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Save file for download using tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        plt.savefig(tmp_file.name)
        
    # Download option
    with open(tmp_file.name, "rb") as file:
        st.download_button(
            label="Download Network Graph as PNG",
            data=file.read(),
            file_name="trade_analysis_network.png",
            mime="image/png"
        )

# Additional information section
with st.expander("About this visualization"):
    st.write("""
    This visualization tool analyzes the North American trade proposal text to identify key topics and their relationships.
    
    - **Word Cloud**: Shows the most frequent terms scaled by their importance
    - **Network Graph**: Displays connections between related terms that appear close together in the text
    
    The visualization helps identify important themes such as trade balances, tariffs, economic impacts on different states,
    and the relationship between the United States, Mexico, and Canada in the context of international trade.
    """) 