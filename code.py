# -*- coding: utf-8 -*-
"""Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15Duv6czDOmqI9ruE5gvwkxLni1C3JET6
"""

!pip install pandas
!pip install openai
!pip install langchain
!pip install "langchain[docarray]"
!pip install tiktoken

!pip install chromadb

import json
import datetime
import pandas as pd
import numpy as np

import openai
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import DocArrayInMemorySearch, Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.schema.document import Document


# Set your OpenAI API key
openai_api_key = "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"

# Define temperature and input_variables if needed
temperature = 0.7
input_variables = {"context": "Some context here", "question": "Some question here"}

def squad_json_to_dataframe(file_path, record_path=['data','paragraphs','qas','answers']):
    """
    input_file_path: path to the squad json file.
    record_path: path to the deepest level in json file default value is
    ['data','paragraphs','qas','answers']
    """

    file = json.loads(open(file_path).read())
    # parsing different level's in the json file
    js = pd.json_normalize(file, record_path)
    m = pd.json_normalize(file, record_path[:-1])
    r = pd.json_normalize(file,record_path[:-2])

    # combining it into single dataframe
    idx = np.repeat(r['context'].values, r.qas.str.len())
    m['context'] = idx
    data = m[['id','question','context','answers']].set_index('id').reset_index()
    data['c_id'] = data['context'].factorize()[0]
    return data

# Load the data from the JSON files
data_train = squad_json_to_dataframe("train-v1.1.json")
data_dev = squad_json_to_dataframe("dev-v1.1.json")

# Merge the training and development data
data = pd.concat([data_train, data_dev])

data['answers'] = data['answers'].apply(lambda x: x[0]['text'] if x else None)

# Create a new data structure combining questions and answers,
# adding "$" at the end for easier chunking later
data['qa'] = data['question'] + data['answers'] + '$'

loader = DataFrameLoader(data, page_content_column="qa")

# Load the data and preprocess it
doc = loader.load()
doc = doc[:1000]

text_splitter = CharacterTextSplitter(
    separator="$",
    chunk_size=125,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

splits = text_splitter.split_documents(doc)

embedding = OpenAIEmbeddings(openai_api_key=openai_api_key, request_timeout=60)

current_date = datetime.datetime.now().date()
print(llm_name)

# Convert data to a list of Document objects
documents = []
for index, row in data.iterrows():
    document = Document(page_content=row['qa'], metadata={'context': row['context'], 'question': row['question']})
    documents.append(document)

# Create a DocArrayInMemorySearch from documents
db = DocArrayInMemorySearch.from_documents(documents, embedding)

vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
)

llm = ChatOpenAI(model_name=llm_name, temperature=temperature, openai_api_key=openai_api_key)

# Define chatbot memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Prompt Originating
template = """
start with a friendly greeting and ask for the user's name. remember their name and use it in your responses. act like a human QA agent. provide concise answers to questions you know, and be honest if you don't know. always greet and ask for the user's name at the beginning. use provided context to answer questions. if you've answered a question before, ask if they have more questions. if they're done, say, "I'm here to help with any other questions."
{context}
question: {question}
helpful answer:
"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

# Run chain

#retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5})
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vectordb.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5}),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

# Define user_message as the user's question
user_message = "What is the capital of France?"

result = qa_chain({"query": user_message})
response = result["result"]

pip install gradio

!pip install typing_extensions --upgrade
!pip install ipykernel

pip uninstall typing_extensions

pip install typing_extensions==3.7.4.3

pip install fastapi==0.65.0

pip install gradio

pip install starlette fastapi

pip install starlette==0.14.2  # Example version number; you can try different versions.