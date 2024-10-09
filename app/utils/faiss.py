import faiss
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# Load the pre-trained transformer model for embeddings (e.g., Sentence-BERT)
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(note_content: str) -> List[float]:
    """
    Create an embedding vector for given note content using a transformer model.
    
    Args:
        note_content (str): The content of the note to create embeddings for.

    Returns:
        List[float]: The generated embedding vector.
    """
    embedding = model.encode(note_content, convert_to_tensor=False)
    return embedding.tolist()

def cluster_notes(notes: List[dict], n_clusters: int = 3) -> Dict[str, List[dict]]:
    """
    Cluster the given notes based on their content embeddings.

    Args:
        notes (List[dict]): A list of note dictionaries. Each note should have a "content" key.
        n_clusters (int, optional): The number of clusters to create. Defaults to 3.

    Returns:
        Dict[str, List[dict]]: A dictionary containing cluster IDs as string keys and detailed note data for each cluster.
    """
    if not notes:
        return {"clusters": "No notes available for clustering"}

    # Create embeddings for all notes
    embeddings = [create_embeddings(note["content"]) for note in notes if "content" in note]
    if not embeddings:
        return {"clusters": "No valid notes available for clustering"}

    # Convert embeddings list to a NumPy array
    embeddings_array = np.array(embeddings).astype("float32")

    # Determine an appropriate number of clusters based on the number of notes
    n_clusters = min(len(notes), n_clusters)

    # Create and train KMeans using Faiss
    kmeans = faiss.Kmeans(d=embeddings_array.shape[1], k=n_clusters, niter=20, verbose=True)
    kmeans.train(embeddings_array)

    # Assign clusters to notes
    cluster_labels = kmeans.index.search(embeddings_array, 1)[1]
    clusters = {}

    for idx, label in enumerate(cluster_labels):
        cluster_id = str(label[0])  # Convert to string to make MongoDB happy
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        
        # Append detailed note information including title, content, and embedding
        clusters[cluster_id].append({
            "title": notes[idx]["title"],
            "content": notes[idx]["content"],
            "embedding": embeddings[idx]
        })

    return clusters
