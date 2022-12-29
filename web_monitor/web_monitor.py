import argparse
import logging
import sys
import json
import yaml
import asyncio
import aiohttp
import time

import re

from typing import List

from kafka import KafkaProducer
from collections import namedtuple
from time import sleep


CheckInfo = namedtuple('CheckInfo', ['url', 'available', 'request_ts', 'response_time', 'http_code', 'pattern_matched'])


async def check_website(client, url, pattern):
    request_ts = int(time.time())
    try:
        start_t = time.monotonic()
        async with client.get(url) as resp:
            if pattern:
                content = await resp.text()
                pattern_matched = bool(re.search(pattern, content))
            else:
                pattern_matched = None

            return CheckInfo(url=url, available=True, request_ts=request_ts, response_time=time.monotonic() - start_t,
                             http_code=resp.status, pattern_matched=pattern_matched)
    except Exception as ex:
        logging.info('Error {}: {}'.format(type(ex), str(ex)))
        return CheckInfo(url=url, available=False, request_ts=request_ts, response_time=None,
                         http_code=None, pattern_matched=None)


async def check_websites(args):
    with open(args.source_filename, mode="r") as f:
        urls = json.load(f)

        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), conn_timeout=5) as client:
            for item in urls:
                # TODO: check url lenght
                tasks.append(asyncio.create_task(check_website(client, item['url'], item.get('pattern'))))
                print(item['url'], item.get('pattern'))

            return await asyncio.gather(*tasks, return_exceptions=True)


def run(args, config):
    kafka_producer = init_kafka_producer(config)
    topic_name = config['kafka_producer']['topic']

    while True:
        logging.info('Start check websites')

        check_results = asyncio.run(check_websites(args))
        send_data(kafka_producer, topic_name, check_results)

        logging.info('Sleep for {} seconds...'.format(args.frequency))
        sleep(args.frequency)


def send_data(kafka_producer: KafkaProducer, topic_name: str, check_results: List[CheckInfo]):
    # TODO: check errors
    for item in check_results:
        kafka_producer.send(topic_name, dict(item._asdict()))


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--config', required=True, help='configuration file name')
    parser.add_argument('--source_filename', type=str, help='the name of a file with url list')
    parser.add_argument('--frequency', type=int, choices=range(5, 300), help='check frequency (sec)')
    parser.add_argument('--timeout', default=5, type=int, help='web site connection timeout (sec)')
    return parser.parse_args()


def config_logging(args):
    logging.basicConfig(format='%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S', level=logging.INFO)
    logging.info("Web monitor started with options: {}".format(args))


def get_config(args):
    with open(args.config) as config_f:
        return yaml.full_load(config_f)


def init_kafka_producer(config):
    return KafkaProducer(
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        **config['kafka_producer']['connection'],
    )


def main():
    try:
        args = parse_args()
        config_logging(args)

        run(args, get_config(args))
    except KeyboardInterrupt:
        sys.exit('Web monitor stopped.')
