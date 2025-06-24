import streamlit as st
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
import os
from tools import fetch_cal
import re
import json
import pandas as pd

load_dotenv()

def clean_json_string(s: str) -> str:
    # 1) Remove // comments
    s = re.sub(r'//.*', '', s)
    # 2) Remove trailing commas before } or ]
    s = re.sub(r',\s*(\}|])', r'\1', s)
    return s

class dietPlanner(BaseModel):
    user_preference: str
    food_type: str
    budget: str
    diet_plan: dict


llm = ChatOpenAI(model='gpt-4.1-mini', api_key=os.environ['API_KEY'])

parser = PydanticOutputParser(pydantic_object=dietPlanner)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a professional dietician.
            Based on the user's food preference (veg/non-veg), occupation (student/office worker/etc.), and budget (low/medium/high), prepare a suitable **daily diet chart**.
        
            Use calorie information fetched from the Nutritionix API to ensure the diet is balanced and realistic.
        
            Ensure:
            - Total daily calories are appropriate for the user type.
            - Meals include breakfast, lunch, snacks, and dinner.
            - For each item, include its approximate calorie count.
            - Ensure variety and simplicity in meals.
            - Avoid luxury or costly items if budget is low.
        
            Respond ONLY in this format:
            {format_instructions}
            """
        ),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [fetch_cal]

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools = tools,
    verbose=True,
)

st.title("AI Diet Planner ")

query = st.text_input("Enter your diet query (e.g., I am a vegetarian student with a low budget)")

if st.button("Sumbmit") and query:
    with st.spinner("Planning your diet..."):
        try:
            raw_response = agent_executor.invoke({"query": query})
            json_str = raw_response["output"]
            cleaned = clean_json_string(json_str)
            structured_response = parser.parse(cleaned)
            # … after parsing into structured_response …

            st.subheader("Your Personalized Diet Plan 🍽️")

            for day, meals in structured_response.diet_plan.items():
                st.markdown(f"## {day}")
                for meal_name, items in meals.items():
                    # Skip the total‐calories key if you have one
                    if meal_name.lower() in ("total_calories", "total_cal"):
                        continue

                    st.markdown(f"### {meal_name.capitalize()}")
                    # items is expected to be a list of dicts with 'name', 'serving', 'calories'
                    for itm in items:
                        if isinstance(itm, dict):
                            name    = itm.get("name", "")
                            serving = itm.get("serving", "")
                            cal     = itm.get("calories", "")
                            # build one line
                            line = name
                            if serving:
                                line += f" ({serving})"
                            if cal != "":
                                line += f" — {cal} kcal"
                            st.markdown(f"- {line}")
                        else:
                            # fallback: just print the string
                            st.markdown(f"- {itm}")

                    # one divider per meal
                    st.markdown("---")

                # finally, if you do have a total_calories field:
                total = meals.get("total_calories") or meals.get("total_cal")
                if total is not None:
                    st.markdown(f"**Total Calories:** {total} kcal")
                    st.markdown("___")  # or '---' but this is thinner


        except Exception as e:
            st.error(f"Something went wrong: {e}")