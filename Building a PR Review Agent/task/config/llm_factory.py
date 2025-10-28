import os

import dotenv
from llama_index.llms.groq import Groq
from llama_index.llms.openai import OpenAI

dotenv.load_dotenv()


def get_llm():
    """
    LLM Provider that initializes LLM and returns a shared LLM instance.

    :return: LLM instance
    """
    llm = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.6,
        max_retries=2,
    )

    # llm = OpenAI("gpt-4o-mini")

    return llm
