<a href="url"><img src="./ragu-logo.png" height="48" width="48" align="left"></a>
# RagU
Go-to app for flavorful document chats and intelligent insights for U

## Introduction
This project implements a Retrieval-Augmented Generation (RAG) system, combining the power of retrieval-based and generative models. RAG leverages a knowledge retrieval system to fetch relevant documents and augment a generative model with the retrieved information. This hybrid approach improves accuracy and factual consistency in question answering, summarization, and other tasks that require retrieving up-to-date information.

The RAG architecture is particularly useful for applications where large, dynamic datasets must be referenced, making it a cutting-edge solution for knowledge-driven tasks.

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Gabbosaur/RagU.git
    cd ragu
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv myenv
    source env/bin/activate
    ```

3. **Install the required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download necessary models**
   Depending on the model you are using, you might need to download some pretrained models. Make sure that Ollama is running.
   ```bash
    ollama serve
    ```

## PoC usage (through terminal)

1. **Index your knowledge base**  
   Before running the RAG model, you need to build an index of the documents or data. Use the `populate_database.py` script to do this:
   ```bash
   python3 populate_database.py
   ```
   If necessary, use --reset to clean the vector database.

2. **Run the RAG model**
   Once the index is ready, you can run the model to answer questions, generate text, or perform other tasks:
   ```bash
   python3 query_data.py "Quali sono le sanzioni dal USA alla Cina?"
   ```
   Wait few moments and see the response.


## Usage (through Streamlit UI)

1. **Run Streamlit**  
   Run the following command and navigate to the provided link.
   ```bash
   streamlit run ui.py
   ```

2. **Upload your documents (pdf/md)**
   Through the left section, you can upload your pdf and markdown files

3. **Wait until the script finishes to index the knowledge database**  
   

4. **Ask a question on the right section**
   You can ask the question by using the input form on the right section, wait few seconds and see the answer.

## Authors
- [Gabriele Guo](https://gabbosaur.github.io/)
- [Chenghao Xia](https://github.com/Izanagi95)
- [Florin Dragos Tanasache](https://github.com/fdt15)
