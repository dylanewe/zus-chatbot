import bs4
import dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = InMemoryVectorStore(embeddings)

loader = WebBaseLoader(
    web_paths=("https://shop.zuscoffee.com/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("product-card__title","text-subdued"),
        )
    ),
)

docs = loader.load()

assert len(docs) == 1
drinkware = docs[0].page_content[1094:1883]

_ = vector_store.add_documents(documents=docs)

prompt_template = """
    You are a salesperson at Zus Coffee. Your job is to get or promote items and prices based on customer requirements.
    Use the following context to answer questions. The product name comes before the price. Be as accurate as possible, but don't
    make up any information that's not from the context. If you don't know the answer, say you don't know.
    {context}
"""

system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=prompt_template)
)

human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [system_prompt, human_prompt]

prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

product_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(k=3),
)

product_chain.combine_documents_chain.llm_chain.prompt = prompt

