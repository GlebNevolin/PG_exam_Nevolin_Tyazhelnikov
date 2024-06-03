from fastapi import FastAPI
import psycopg2


app = FastAPI()


@app.get('/check/{host}')
def check_master(host: str):
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            port=5432,
            host=host
        )

        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM test"
        )
        conn.commit()
        cur.close()
        conn.close()

        return {"Result": "Very good"}
    except:
        return {}
