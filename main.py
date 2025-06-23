import streamlit as st
from pydantic import BaseModel

from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import PydanticOutputParser

from langchain.prompts import ChatPromptTemplate

from langchain.agents import create_tool_calling_agent, AgentExecutor

from dotenv import load_dotenv
import os

load_dotenv()

class dietPlanner(BaseModel):
    user_preference: str
    food_type: str
    budget: str
    diet_plan: str

llm = ChatOpenAI(model='gpt-4o-mini', api_key=st.secrets['API_KEY'])

parser = PydanticOutputParser(pydantic_object=dietPlanner)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a professional dietician.
            Based on the user's food type, occupation, and budget, prepare a suitable daily diet chart.
            Respond ONLY in this format:\n{format_instructions}
            """
        ),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = []

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools = tools,
    verbose=False,
)

st.title("AI Diet Planner 🥗")

query = st.text_input("Enter your diet query (e.g., I am a vegetarian student with a low budget)")

if st.button("Click To Generate") and query:
    with st.spinner("Generating your diet plan..."):
        try:
            response = agent_executor.invoke({"query": query})
            output = response.get("output", None)
        
            if output:
                result = parser.parse(output)
                st.success("Diet Plan Generated")
                st.write(f"**Preference:** {result.user_preference}")
                st.write(f"**Food Type/Occupation:** {result.food_type}")
                st.write(f"**Budget:** {result.budget}")
                st.write(f"**Diet Plan:**")
                for line in result.diet_plan.split(". "):
                    if line.strip():
                        st.markdown(f"- {line.strip().rstrip('.')}.")

            else:
                st.warning("No Output from Agent")
        
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("Enter Prompt")
