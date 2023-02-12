import pandas as pd
from sentence_transformers.util import cos_sim
from itertools import chain
from collections import Counter
import ast
import pickle
import re
import json
from nltk.tokenize import sent_tokenize

path = "Embeddings/"

def tokenize_paragraph(paragraph):
    # Use regular expressions to split the paragraph into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
    return sentences

def correct_text(text):
    corrected_text = re.sub(r'â\b([a-z]+)\b', r'\1', text)
    corrected_text = re.sub(r'â([A-Z][a-z]+)\b', r'\1', corrected_text)
    corrected_text = re.sub(r'â([A-Z])', r'\1', corrected_text)
    corrected_text = re.sub(r'â', '', corrected_text)
    corrected_text = re.sub(r'\b([a-z]+)([A-Z])', r'\1 \2', corrected_text)
    corrected_text = corrected_text.replace("of Youth", "of Youth ")
    corrected_text = corrected_text.replace("low Women", "low women ")
    words = corrected_text.split()
    split_words = []
    for word in words:
        if len(word) > 14:
            split_word = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)
            split_word = re.sub(r'([a-z]+)([0-9])', r'\1 \2', split_word)
            split_word = re.sub(r'([0-9]+)([a-z]+)', r'\1 \2', split_word)
            split_word = re.sub(r'([a-z]+)([A-Z][a-z]+)', r'\1 \2', split_word)
            split_words.append(split_word)
        else:
            split_words.append(word)
    corrected_text = " ".join(split_words)
    return corrected_text

def newcosine(first_name, second_name, df, com_no):
    name_a_df = df.query("Names == @first_name")
    name_b_df = df.query("Names == @second_name")

    sentences_a = sent_tokenize(name_a_df["Processed_data"].to_list()[0])
    sentences_b = sent_tokenize(name_b_df["Processed_data"].to_list()[0])
    
    # Load the respective embeddings 
    embed_path1 = path+first_name+".pkl"
    with open(embed_path1, "rb") as f:
        embeddings_a = pickle.load(f)
    embed_path2 = path+second_name+".pkl"
    with open(embed_path2, "rb") as f:
        embeddings_b = pickle.load(f)
    
    # Create an empty dataframe for the results
    output_df = pd.DataFrame(columns=["index", "score_data", "text_a", "text_b"])
    # Iterate over each sentence of the first name
    for i, embed_a in enumerate(embeddings_a):
        scores = cos_sim(embed_a,embeddings_b)
        # Flattern the score
        flattened_scores_list = list(chain.from_iterable(scores))
        # Find the max score 
        max_score = max(flattened_scores_list).item()
        # Find the max index
        max_index = flattened_scores_list.index(max_score)

        # encoding
        sentences_a[i] = sentences_a[i].encode('utf-8', errors='ignore').decode()
        sentences_b[max_index] = sentences_b[max_index].encode('utf-8', errors='ignore').decode()

        # Append each row in the output dataframe
        output_df.loc[i] = [max_index, max_score, sentences_a[i],sentences_b[max_index]]
    output_df = output_df.sort_values(by='score_data', ascending=False)

    sentences_a = output_df["text_a"].to_list()
    sentences_b = output_df["text_b"].to_list()
    sent_a = []
    sent_b = []
    for i in range(com_no):
        if sentences_b[i] != sentences_b[i+1]:
            sentences_a[i] = correct_text(sentences_a[i])
            sentences_b[i] = correct_text(sentences_b[i])
            sent_a.append(sentences_a[i])
            sent_b.append(sentences_b[i])

    return sent_a, sent_b


        

