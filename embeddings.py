import os
import numpy as np
from openai import OpenAI
import logging
from tools import *

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key, )
logging.basicConfig(level=logging.INFO, format='%(message)s')


def create_embeddings_vectors():
    result = {}
    companies = read_logos_file()

    for company in companies:
        name = company[0]
        description = company[1]
        ticker = company[2]
        
        result[name] = [contact_embeddings(description), ticker]

    make_pickle_file(result, './data/embeddings.pkl')
    

def find_similar_companies(description: str):
    embeddings = load_pickle_file('./data/embeddings.pkl')

    embedding = contact_embeddings(description)

    similar_companies_list = []
    for company, value in embeddings.items():
        similarity = cosine_similarity(value[0], embedding)
        similar_companies_list.append([company, similarity, value[1]])

    similar_companies_list.sort(key=lambda x: x[1])
    similar_companies_list = (similar_companies_list[-3:])[::-1]

    return similar_companies_list

def cosine_similarity(vector1, vector2):
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

def contact_embeddings(description: str):
    logging.info("Contacting embedding")
    response = client.embeddings.create(
    input=description,
    model="text-embedding-ada-002"
    )
    logging.info("Contacted embedding successfully")
    
    return response.data[0].embedding

