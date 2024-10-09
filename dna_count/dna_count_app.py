import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# app title
st.write("""
# DNA Nucleotide Count App
***
""")

# text input
st.header('Enter DNA sequence')

sequence = st.text_area("Sequence input", height=200)
sequence = sequence.splitlines()[1:]
sequence = ''.join(sequence)

st.write("""
***
""")

st.header('Input (DNA Query)')
st.write(sequence)

st.header('Output (DNA Nucleotide Count)')
X = {
    'A': sequence.count('A'),
    'T': sequence.count('T'),
    'G': sequence.count('G'),
    'C': sequence.count('C')
}
df = pd.DataFrame.from_dict(X, orient='index').rename({0: 'count'}, axis="columns")
df = df.reset_index().rename(columns={'index': 'Nucleotide'}).set_index('Nucleotide')
st.subheader('Table view')
st.write(df)

st.subheader('Bar chart')
plt.figure(figsize=(7, 4))
df['count'].plot(kind='bar', color=['skyblue', 'lightgreen', 'orange', 'pink'])
plt.title('DNA Nucleotide Count')
plt.xlabel('Nucleotide')
plt.ylabel('Count')
plt.xticks(rotation=0)

# Show the plot in Streamlit
st.pyplot(plt)
