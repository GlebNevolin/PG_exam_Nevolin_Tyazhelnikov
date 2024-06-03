import random
import time
import logging
import psycopg2
from concurrent.futures import ThreadPoolExecutor


class Writer:
    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str,
        port: str,
    ):

        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        self.cursor = self.connection.cursor()

    def _task(
        self,
        k,
    ):

        time.sleep(
            random.choice(
                [1, 2, 3]
            )
        )
        self.cursor(
            "INSERT INTO my_table VALUES (%s)",
            (k,)
        )

        self.connection.commit()
        logging.warning(
            f"Values insert - {k}"
        )

    def start_writer(
        self
    ):

        with ThreadPoolExecutor(
            max_workers=5,
        ) as executor:
            futures = [
                executor.submit(
                    self._task,
                    i,
                ) for i in range(500000)
            ]

            [future.result() for future in futures]

        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    try:
        writer = Writer(
            dbname='benchmark',
            user='postgres',
            password='postgres',
            host='pg-master,pg-slave',
            port='5432',
        )

        writer.start_writer()
    except:
        pass

