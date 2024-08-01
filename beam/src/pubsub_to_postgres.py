import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from google.auth import default
from google.auth.credentials import Credentials
from google.cloud import pubsub_v1
import json, os, time
import psycopg2

class ParseMessage(beam.DoFn):
    def process(self, element):
        try:
            message = json.loads(element)
            yield message
        except json.JSONDecodeError:
            pass

class SaveToPostgres(beam.DoFn):
    def __init__(self, db_config):
        self.db_config = db_config

    def start_bundle(self):
        retry_count = 0
        max_retries = 5
        while retry_count < max_retries:
            try:
                self.conn = psycopg2.connect(**self.db_config)
                self.cur = self.conn.cursor()
                self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        data JSONB
                    )
                ''')
                return
            except psycopg2.OperationalError as e:
                retry_count += 1
                time.sleep(5)
                if retry_count == max_retries:
                    raise e

    def process(self, element):
        self.cur.execute('INSERT INTO messages (data) VALUES (%s)', (json.dumps(element),))
        self.conn.commit()

    def finish_bundle(self):
        self.conn.close()

def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True

    db_config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'postgres',
        'port': '5432'
    }

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    subscription_id =  os.environ["SUBSCRIPTION_NAME"]
    subscription = f"projects/{project_id}/subscriptions/{subscription_id}"

    with beam.Pipeline(options=options) as p:
        messages = (
            p
            | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(subscription=subscription).with_output_types(bytes)
            | 'Decode' >> beam.Map(lambda x: x.decode('utf-8'))
            | 'ParseMessage' >> beam.ParDo(ParseMessage())
        )

        messages | 'SaveToPostgres' >> beam.ParDo(SaveToPostgres(db_config))

if __name__ == '__main__':
    run()
