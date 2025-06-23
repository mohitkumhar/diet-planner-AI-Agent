# 🥗 AI Diet Planner using LangChain, Streamlit, and OpenAI

This project is an AI-powered **Diet Planner** built using **LangChain**, **Streamlit**, and **OpenAI GPT-4o mini**. The app intelligently generates a customized diet chart based on the user's food preferences, occupation (like student/professional), and budget.

🚀 **[Live Demo](#)** ← _Add your live Streamlit Cloud or Hugging Face link here._

## 🔍 Features

- 📌 User input for food preference, budget, and occupation
- 🤖 Uses LangChain agent with `ChatOpenAI` to process and generate plans
- ✅ Validates structured response using `PydanticOutputParser`
- 💬 Clean and interactive UI with Streamlit
- 🧠 LLM-powered logic with `GPT-4o-mini`
- 🛠️ Easily extendable for additional tools or dietary constraints

---

## 📷 Preview

![App Screenshot](https://github.com/mohitkumhar/diet-planner-AI-Agent/assets/preview.gif)  
_Add a screenshot or demo GIF here_

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** LangChain Agent + OpenAI API
- **Validation:** Pydantic (for structured LLM outputs)
- **LLM:** GPT-4o-mini (via `langchain_openai`)

---

## 🛠️ How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohitkumhar/diet-planner-AI-Agent
   cd diet-planner-AI-Agent

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt

3. **Set up environment variables**

   Create a `.streamlit/secrets.toml` file and add your OpenAI key:

   ```toml
   API_KEY = "your_openai_api_key"
   ```

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

---

## 📦 Output Format

The AI will return structured diet plans like this:

```
Preference: Non-vegetarian  
Food Type: Student Diet  
Budget: Low  
Diet Plan:
- Breakfast: Boiled eggs, toast, and milk  
- Lunch: Rice, dal, seasonal vegetables  
- Snacks: Banana or peanuts  
- Dinner: Chapati with egg curry  
```

---

## 🙋‍♂️ Author

**Mohit Kumhar**<br>
🧑‍💻 Python | Backend | ML | Data Science<br>
🔗 [LinkedIn](https://www.linkedin.com/in/mohitkumhar/)<br>
💻 [GitHub](https://github.com/mohitkumhar)<br>

---


## 🌐 Live App

👉 Try the app here: [Live Demo](#)

---

## 📌 To Do / Future Improvements

* [ ] Add calorie estimation per meal
* [ ] Export plan as PDF/CSV
* [ ] Add dietary restrictions (e.g. diabetes, keto)
* [ ] Multilingual support
