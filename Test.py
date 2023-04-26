import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

data = pd.read_csv('SeniorProject\Project\PromptsToAnalyze.csv')

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Prompt'])

k = 5  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

# Get cluster labels for each prompt
cluster_labels = kmeans.labels_

# Add cluster labels to the DataFrame
data['Cluster'] = cluster_labels

# Explore cluster distribution
cluster_counts = data['Cluster'].value_counts()
print(cluster_counts)

# Visualize cluster distribution
plt.bar(cluster_counts.index, cluster_counts.values)
plt.xlabel('Cluster')
plt.ylabel('Count')
plt.title('Cluster Distribution')
plt.show()

with open('cluster_analysis_Full.txt', 'w') as file:
    for cluster_id in range(k):
        cluster_data = data[data['Cluster'] == cluster_id]
        file.write(f"Cluster {cluster_id}:\n")
        file.write(cluster_data['Prompt'].head().to_string(index=False))
        file.write('\n\n')