from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from ..db_models.chat_history import fetch_recent_messages
from langchain_core.prompts import ChatPromptTemplate
from ..db_models.chat_save import save_message
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    provider="auto",
)

llm=ChatHuggingFace(llm=llm)

# Gemini Model Config
# llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

# Openai Model Config
# llm=ChatOpenAI(model="gpt-4o-mini")

def chat_endpoint(user_id: int, user_query: str):

    history=fetch_recent_messages(user_id)
   
    template = ChatPromptTemplate(
        [
            ("system", "You are a helpful AI assistant. Read the user’s query carefully and respond in a short and concise manner. If the answer is available in the previous conversation history, use that information to respond accurately. If not, provide a clear and correct answer"),
            ("placeholder", "{conversation}"),
            ("human","{user_query}"),
        ]
    )
    
    final_prompt = template.invoke(
        {
            "conversation": history,
            "user_query": user_query
        }
    )

    #append User Query to DB
    save_message(user_id=user_id, role="human", message=user_query)
    

    response=llm.invoke(final_prompt)

    # append Response  to DB
    save_message(user_id=user_id, role="ai", message=response.content)
    return response.content

# user_query=input("Ask Something: ")
# chat_endpoint(id=1, user_query=user_query)


