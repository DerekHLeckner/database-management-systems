from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    content = """
    <html>
        <head>
            <title>SQLite Query Tool</title>
        </head>
        <body>
        <img src="https://futuretechnologies.njit.edu/sites/futuretechnologies/files/njit%20logo_0.png" alt="Example Image">
        <h1>CS 631 | Spring 2023 | Derek and Andrew UI</h1>  
        	<style>
		h1 {
			font-style: italic;
			color: green;
		}
	</style>  
            <form action="/query" method="post">
                <textarea name="query" rows="10" cols="50"></textarea>
                <br>
                <button type="submit">Execute Query</button>
            </form>
        <img src="https://media.bizj.us/view/img/5803721/bank*1200xx684-385-0-64.jpg" alt="Bank Picture">
        </body>
    </html>
    """
    return content


@app.post("/query", response_class=HTMLResponse)
async def execute_query(request: Request):
    query = await request.form()
    query_text = query["query"]

    # Connect to the SQLite database
    conn = sqlite3.connect("new.db")

    # Execute the query and retrieve the results
    cur = conn.cursor()
    cur.execute(query_text)
    rows = cur.fetchall()

    # Format the results as an HTML table
    table_html = "<table>"
    table_html += "<tr>"
    for description in cur.description:
        table_html += f"<th>{description[0]}</th>"
    table_html += "</tr>"
    for row in rows:
        table_html += "<tr>"
        for value in row:
            table_html += f"<td>{value}</td>"
        table_html += "</tr>"
    table_html += "</table>"

    # Close the database connection
    conn.close()

    # Render the results as an HTML page
    content = f"""
    <html>
        <head>
            <title>SQLite Query Results</title>
        </head>
        <body>
            <h2>Query:</h2>
            <p>{query_text}</p>
            <h2>Results:</h2>
            {table_html}
        </body>
    </html>
    """
    return content
