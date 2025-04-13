from fastapi import FastAPI
from google.cloud import bigquery

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Transaction Analyzer API is running!"}

@app.get("/top-transactions")
def get_top_transactions():
    client = bigquery.Client()
    query = """
    SELECT sender, receiver, SUM(amount) as total_amount
    FROM `virtualbox-assignmnt.bitcoin_analysis.transactions`
    GROUP BY sender, receiver
    ORDER BY total_amount DESC
    LIMIT 10
    """
    results = client.query(query).result()
    return [{"sender": row.sender, "receiver": row.receiver, "amount": row.total_amount} for row in results]
