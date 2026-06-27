import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load API Key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_ai(df, question):

    preview = df.head(10).to_string()

    prompt = f"""
You are an Expert AI Data Analyst.

Dataset Columns:
{list(df.columns)}

Dataset Preview:
{preview}

User Question:
{question}

Your job is to understand the user's request.

If a graph is needed, return JSON in this format:

{{
    "analysis": "Short explanation",
    "graph_required": true,
    "chart_type": "bar | line | pie | scatter | histogram | box | heatmap | forecast",
    "x_column": "",
    "y_column": "",
    "aggregation": "sum | mean | count | none"
}}

If the user asks for:
- prediction
- forecast
- future
- next month
- next 30 days
- future trend

Then return:

{{
    "analysis":"Forecast of the selected column.",
    "graph_required":true,
    "chart_type":"forecast",
    "x_column":"",
    "y_column":"<numeric column>",
    "aggregation":"none"
}}

If the user only asks for information (no graph), return:

{{
    "analysis":"Answer to the user's question.",
    "graph_required":false
}}

Rules:
1. Return ONLY valid JSON.
2. Do NOT use markdown.
3. Do NOT write explanations.
4. Use only column names that exist in the dataset.
"""
    
    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        text = text.replace("```json", "").replace("```", "").strip()

        print("Gemini Response:", text)

        result = json.loads(text)

        return result

    except Exception as e:

        print("AI Error:", e)

        return {
            "analysis": f"AI Error: {str(e)}",
            "graph_required": False
        }