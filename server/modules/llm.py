# # from langchain_core.prompts import PromptTemplate
# # from langchain.chains import RetrievalQA
# # from langchain_groq import ChatGroq
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # GROQ_API_KEY = "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"

# # def get_llm_chain(retriever):
# #     llm = ChatGroq(
# #     api_key=GROQ_API_KEY,
# #     model="openai/gpt-oss-120b"
# # )
# #     prompt = PromptTemplate(
# #         input_variables=["context", "question"],
# #         template="""
# # You are **MediBot**, an AI-powered assistant trained to help users understand medical documents and health-related questions.

# # Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

# # ---

# # 🔍 **Context**:
# # {context}

# # 🙋‍♂️ **User Question**:
# # {question}

# # ---

# # 💬 **Answer**:
# # - Respond in a calm, factual, and respectful tone.
# # - Use simple explanations when needed.
# # - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
# # - Do NOT make up facts.
# # - Do NOT give medical advice or diagnoses.
# # """
# #     )

# #     return RetrievalQA.from_chain_type(
# #         llm=llm,
# #         chain_type="stuff",
# #         retriever=retriever,
# #         chain_type_kwargs={"prompt": prompt},
# #         return_source_documents=True
# #     )


# import os 
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA
# from langchain.prompts import ChatPromptTemplate
# # from langcahin_core.output_parsers import StrOutputParser
# from openai import OpenAI
# import json

# load_dotenv()

# QROQ_API_KEY = os.environ.get("QROQ_API_KEY")

# def get_llm_chain(vectorstore):
#     llm = ChatGroq(
#         api_key = QROQ_API_KEY,
#         model = "openai/gpt-oss-120b",
#         temperature=0.4
#     )
#     template = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
# Generate multiple search queries related to: {question} \n
# Output (4 queries):"""

#     prompt = ChatPromptTemplate.from_template(template)
    

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         prompt=prompt,
#         retriever=retriever,
#         return_source_documents=True
#     )
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

GROQ_API_KEY = os.environ.get("QROQ_API_KEY")


def get_llm_chain(vectorstore):

    # LLM
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-120b",
        temperature=0.4
    )

    # Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Prompt (IMPORTANT: must be PromptTemplate, NOT ChatPromptTemplate)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful assistant that answers based ONLY on the provided context.

Context:
{context}

Question:
{question}

Instructions:
- Use only the context.
- If answer is not found, say: "I couldn't find relevant information in the documents."
- Do not hallucinate.

Answer:
"""
    )

    # RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return chain