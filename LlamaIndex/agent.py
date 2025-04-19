import asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.chat_engine import SimpleChatEngine

# Step 1: Load your documents (You can replace this with your own source)
documents = SimpleDirectoryReader("../Data").load_data()

# Step 2: Create the index
index = VectorStoreIndex.from_documents(documents)

# Step 3: Initialize the LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Step 4: Create a Chat Engine
chat_engine = index.as_chat_engine(llm=llm, chat_mode="simple")

# Step 5: Stream the response using astream_chat
async def stream_response(query):
    print("Inside stream_reponse")

    # Step 1: Send the query and get streaming response object
    response = await chat_engine.astream_chat(query)
    print("query fired")

    # Step 2: Stream the response token by token
    async for token in response.async_response_gen():
        yield token

async def get_response(query):
    print("Inside get_reponse")
    gen = stream_response(query)
    async for i in gen:
        print(i)

# Run the async function
if __name__ == "__main__":
    asyncio.run(get_response())
