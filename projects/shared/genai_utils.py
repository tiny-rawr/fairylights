import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

def count_tokens(text):
  tokenizer = tiktoken.get_encoding('cl100k_base')
  tokens = tokenizer.encode(
    text,
    disallowed_special=()
  )
  return len(tokens)

def chunk_text(text, chunk_size=10000):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=100,
        length_function=count_tokens,
        separators=['\n\n', '\n', ' ', '']
    )

    return text_splitter.split_text(text)