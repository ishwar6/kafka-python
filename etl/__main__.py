"""Entry point for running the Kafka to Redshift ETL pipeline."""

from .pipeline import KafkaToRedshiftETL


def main():
    """Run the ETL pipeline."""
    pipeline = KafkaToRedshiftETL()
    pipeline.run()


if __name__ == "__main__":
    main()
