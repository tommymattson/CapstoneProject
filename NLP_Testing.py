import gensim
from gensim import corpora
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import csv

data = pd.read_csv('SeniorProject\Project\PromptsToAnalyze.csv')
stemmer = PorterStemmer()

# Tokenize the text
data['Tokenized_Text'] = data['Prompt'].apply(word_tokenize)

toRemoveWords = ['red', 'orange', 'yellow', 'green', 
                 'blue', 'purple', 'black', 'white', 
                 'grey', 'gray',
                 'style', 'background', 'dark', 'lighting']

# Remove stopwords, punctuation, and color names
stop_words = set(stopwords.words('english') + list(string.punctuation) + toRemoveWords)
#data['Processed_Text'] = data['Tokenized_Text'].apply(lambda x: [word.lower() for word in x if word.lower() not in stop_words])
data['Stemmed_Text'] = data['Tokenized_Text'].apply(lambda x: [stemmer.stem(word.lower()) for word in x if word.lower() not in stop_words])



# Create a dictionary from the processed text
#dictionary = corpora.Dictionary(data['Processed_Text'])
dictionary = corpora.Dictionary(data['Stemmed_Text'])

# Create a document-term matrix
#doc_term_matrix = [dictionary.doc2bow(doc) for doc in data['Processed_Text']]
doc_term_matrix = [dictionary.doc2bow(doc) for doc in data['Stemmed_Text']]

# Set the number of topics
num_topics = 7

# Train the LDA model
lda_model = gensim.models.LdaModel(doc_term_matrix, num_topics=num_topics, id2word=dictionary, passes=10)


# Get the topic distribution for each document
topics = lda_model.get_document_topics(doc_term_matrix)

# Extract the dominant topic for each document
data['Dominant_Topic'] = [max(topics[i], key=lambda x: x[1])[0] for i in range(len(topics))]

'''
# Open the text file for writing
with open('lda_results_5_topics.txt', 'w') as file:
    # Iterate over each document
    for index, row in data.iterrows():
        file.write(f"Prompt: {row['Prompt']}\n")
        file.write(f"Dominant Topic: {row['Dominant_Topic']}\n")
        file.write("Keywords: ")
        
        # Get the top keywords for the dominant topic
        keywords = lda_model.show_topic(row['Dominant_Topic'])
        keywords_text = ", ".join([word[0] for word in keywords])
        file.write(keywords_text)
        file.write("\n\n")
'''
# Define the output file path
output_file = 'lda_results_7_topics_NLTK.csv'

# Open the CSV file for writing
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Prompt', 'Dominant_Topic', 'Keywords'])
    
    # Iterate over each document
    for index, row in data.iterrows():
        prompt = row['Prompt']
        dominant_topic = row['Dominant_Topic']
        
        # Get the top keywords for the dominant topic
        keywords = lda_model.show_topic(row['Dominant_Topic'])
        keywords_text = ", ".join([word[0] for word in keywords])
        
        # Write the row to the CSV file
        writer.writerow([prompt, dominant_topic, keywords_text])
