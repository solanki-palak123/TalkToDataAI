import gradio as gr
from data_processor import load_data, get_summary
from ai_agent import ask_ai
from graph_generator import generate_graph
from ml_forecasting import forecast
from insights import generate_insights
from report_generator import generate_report


def analyze(file, question):

    if file is None:
        return "Please upload a CSV file.", "", None, None

    try:
        # Load dataset
        df = load_data(file)

        # Summary
        summary = get_summary(df)

        # Insights
        insights = generate_insights(df)

        summary = summary + "\n\n========== DATASET INSIGHTS ==========\n\n" + insights

        # Empty question
        if question.strip() == "":
            pdf = generate_report(summary, "No question asked.")
            return summary, "Please enter a question.", None, pdf

        # Simple Queries
        q = question.lower()

        if "rows" in q:
            analysis = f"Total Rows: {len(df)}"
            pdf = generate_report(summary, analysis)
            return summary, analysis, None, pdf

        if "columns" in q:
            analysis = f"Columns:\n{list(df.columns)}"
            pdf = generate_report(summary, analysis)
            return summary, analysis, None, pdf

        if "missing" in q:
            analysis = f"Missing Values:\n{df.isnull().sum()}"
            pdf = generate_report(summary, analysis)
            return summary, analysis, None, pdf

        if "data type" in q or "datatype" in q or "dtypes" in q:
            analysis = f"Data Types:\n{df.dtypes}"
            pdf = generate_report(summary, analysis)
            return summary, analysis, None, pdf

        # AI Analysis
        result = ask_ai(df, question)

        if result is None:
            result = {
                "analysis": "AI did not return any response.",
                "graph_required": False
            }

        analysis = result.get("analysis", "")

        graph = None

        if result.get("graph_required", False):

            try:

                if result.get("chart_type", "").lower() == "forecast":

                    column = result.get("y_column")
                    graph = forecast(df, column)

                else:

                    graph = generate_graph(df, result)

            except Exception as e:

                analysis += f"\n\nGraph Error:\n{str(e)}"

        # Generate PDF
        pdf = generate_report(summary, analysis)

        return summary, analysis, graph, pdf

    except Exception as e:

        return "", f"Application Error:\n{str(e)}", None, None


demo = gr.Interface(
    fn=analyze,
    inputs=[
        gr.File(label="📂 Upload CSV"),
        gr.Textbox(
            label="Ask AI",
            placeholder="""Examples:

How many rows are there?
Show column names
Show missing values
Show data types
Show sales by country
Forecast UnitPrice for next 30 days
"""
        )
    ],
    outputs=[
        gr.Textbox(label="Dataset Summary", lines=25),
        gr.Textbox(label="AI Response", lines=12),
        gr.Image(label="Generated Graph"),
        gr.File(label="📄 Download PDF Report")
    ],
    title="📊 TalkToData AI",
    description="Upload a CSV file and ask questions in natural language."
)

demo.launch(debug=True)