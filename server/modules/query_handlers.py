from logger import logger

def query_chain(chain,user_input:str):
    try:
        logger.info(f"Received user query: {user_input}")
        result = chain({"query": user_input})
        response = {
            "result": result["result"],
            "sources":[doc.metadata.get("source","")for doc in result["source_documents"]] }
        
        logger.info(f"Query chain result: {response}")
        return response
    except Exception as e:
        logger.exception("Error in query chain:")
        raise 
