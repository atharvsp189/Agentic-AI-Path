from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import BaseModel
from typing import List

from dotenv import load_dotenv
load_dotenv()

import asyncio

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
)

# define structure of output post
class post(BaseModel):
    post_title: str
    post_url: str
    caption: str
    comments: List[str]

class Posts(BaseModel):
    posts: List[post]

# opening it on systems browser
# or else open web in inbuilt chromium
browser = Browser(
    config=BrowserConfig(
        browser_binary_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    )
)

# make it use structure we defined
controller = Controller(output_model=Posts)

Task = "Go to Instagram.com and search for virat kohli and get the captions and top3 comments from his 3 latest posts"


async def main():
    # Initialize Agent
    agent = Agent(
        task=Task,
        llm=llm,
        browser=browser,
        controller=controller,
    )
    
    history = await agent.run()
    # getting final result
    result = history.final_result()
    # also we can get visited urls screenshots etc. more details in documentataion
    
    if result:
        try:
            parsed: Posts = Posts.model_validate_json(result)
            for post in parsed.posts:
                print('\n--------------------------------')
                print(f'Title:    {post.post_title}')
                print(f'URL:      {post.post_url}')
                print(f'Captions: {post.caption}')
                print(f'Comments: {post.comments}')
        except Exception as e:
            print("Parsing Error:", str(e))
    else:
        print('No result')

    await browser.close()

asyncio.run(main())
