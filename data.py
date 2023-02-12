import pandas as pd
import fitz
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
import torch

import re
import os
from os import listdir
import pickle

# Assign the Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Model for creating embeddings
model = SentenceTransformer('all-mpnet-base-v2',device=device)
# Embedding folder
path = "Embeddings/"

# Data preprocessing ----------------------------------------------------------------------
def process_text(text,name):
    text = re.sub("(@\S+)|(https?:\/\/.*[\r\n]*)|(-- Britannica Online Encyclopedia)", "", text)
    text = re.sub(r"\d+/\d+/\d+, \d+:\d+ [AP]M", "", text)
    text = re.sub(r"\d+/\d+", "", text)
    text = re.sub(r"Citation Information\n.+", "", text, flags=re.DOTALL)
    text = re.sub("\n"," ",text)
    return text

def processed_data(df):
    # Define the pronouns
    pronouns = "He|Him|His|She|Her|he|him|his|she|her"
    # Create an empty column in the dataframe for processed data
    df["processed"] = ""
    df["Processed_data"] = ""
    # Iterate over each row in the dataframe
    for i, row in df.iterrows():
        name = row["Names"]
        text = process_text(row["data"],name)
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        sentences[0] = re.sub(name+".*?"+name, name, sentences[0])
        sentences[0] = sentences[0].strip()
        sentences[0] = re.sub(r'\b(\w+)( \1\b)+', r'\1', sentences[0])
        #sentences[0] = re.sub(r"(\b"+name+"\b)(\s+\b"+name+"\b)+",name, sentences[0])
        text = " ".join(sentences)
        df.at[i, "Processed_data"] = text
        # Remove newline characters
        sentences = [sentence.replace("\n", "") for sentence in sentences]
        # Replace pronouns with the name
        sentences = [re.sub(r"\b("+pronouns+r")\b", name, sentence) for sentence in sentences]
        # Assign the processed sentences to the 'processed' column
        df.at[i, "processed"] = sentences
    return df

def embeddings(df):
    # Find the maximum sequence length of all the sentences in the processed data
    max_seq_length = max([len(sentence.split()) for item in df['processed'] for sentence in item])
    # Set the maximum sequence length for the model
    model.max_seq_length = max_seq_length
    # Create an empty column in the dataframe for embeddings
    people_names = df['Names']
    df["embeddings"] = ""
    # Iterate over each row in the dataframe
    for i, text in enumerate(df['processed']):
        # Generate embeddings for the text
        embeddings = model.encode(text)
        # Get the Person name and the path for saving the file
        name = people_names[i]
        embed_path = path+name+".pkl"
        # Save the file
        with open(embed_path, "wb") as f:
            pickle.dump(embeddings, f)
        # Assign the embeddings to the 'embeddings' column
        #df.at[i, 'embeddings'] = embeddings
    return df

def extract_text_df(folder):
    # Take all the people names into a list
    #people_names = [file.replace(".pdf", "" ) for file in listdir(folder)]
    people_names = [file.replace(" -- Britannica Online Encyclopedia.pdf", "" ) for file in listdir(folder)]
    # Create a dataframe with the names and an empty data column
    df = pd.DataFrame(people_names,columns=['Names'])
    df['data'] = ''
    # Iterate over the file names and update the df
    for file_name in os.listdir(folder):
        # Open the pdf file and read the content
        doc = fitz.open(os.path.join(folder,file_name))
        text = ""
        for page in doc:
            text += page.get_text()
        # Lookup the index of the current file in the dataframe
        file_index = os.listdir(folder).index(file_name)
        # Set the data for the current file in the dataframe
        df.at[file_index, 'data'] = text
    return df

def create_dataFrame(data_path):
    df = extract_text_df(data_path)
    df = processed_data(df)
    df = embeddings(df)
    df.to_csv(r"data.csv")
#data_path = r"C:\Users\personal\Projects\Britannica-Independence\Data"
#create_dataFrame(data_path)










