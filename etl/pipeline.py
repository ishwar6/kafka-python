"""Module providing a Kafka to Redshift ETL pipeline."""

import json
import os
from kafka import KafkaConsumer
import psycopg2


class KafkaToRedshiftETL:
    """Pipeline extracting messages from Kafka and loading them into Redshift."""

    def __init__(self):
        """Initialize consumer and Redshift connection using environment variables."""
        self.consumer = KafkaConsumer(
            os.environ["KAFKA_TOPIC"],
            bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.connection = psycopg2.connect(
            host=os.environ["REDSHIFT_HOST"],
            port=os.environ.get("REDSHIFT_PORT", "5439"),
            user=os.environ["REDSHIFT_USER"],
            password=os.environ["REDSHIFT_PASSWORD"],
            database=os.environ["REDSHIFT_DB"],
        )
        self.table = os.environ["REDSHIFT_TABLE"]

    def transform(self, record):
        """Transform records before loading."""
        return {k: v.upper() if isinstance(v, str) else v for k, v in record.items()}

    def load(self, record):
        """Insert transformed record into Redshift."""
        columns = ",".join(record.keys())
        placeholders = ",".join(["%s"] * len(record))
        values = list(record.values())
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"insert into {self.table} ({columns}) values ({placeholders})", values
            )
        self.connection.commit()

    def run(self):
        """Consume messages from Kafka and load them into Redshift."""
        for message in self.consumer:
            transformed = self.transform(message.value)
            self.load(transformed)
