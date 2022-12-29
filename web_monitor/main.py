import argparse
import asyncio
import json
import logging
import re
import sys
import time
from collections import namedtuple
from time import sleep
from typing import List

import aiohttp
import yaml
from kafka import KafkaProducer
from retry import retry

CheckInfo = namedtuple('CheckInfo', ['url', 'available', 'request_ts', 'response_time', 'http_code', 'pattern_matched'])

logger = logging.getLogger('web_monitor')


def run(args, config: dict):
    kafka_producer = init_kafka_producer(config)
    topic_name = config['kafka_producer']['topic']
    check_frequency = config['web_monitoring']['check_frequency']
    while True:
        logger.info('Start check websites')

        check_results = asyncio.run(check_websites(config))
        send_data(kafka_producer, topic_name, check_results)

        logger.info('Sleep for {} seconds...'.format(args.frequency))
        sleep(check_frequency)


async def check_websites(config: dict):
    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),
                                     conn_timeout=config['web_monitoring']['conn_timeout']) as client:
        for item in get_files(config['web_monitoring']['source_filename']):
            tasks.append(asyncio.create_task(check_website(client, item['url'], item.get('pattern'))))
            print(item['url'], item.get('pattern'))

        return await asyncio.gather(*tasks, return_exceptions=True)


async def check_website(client: aiohttp.ClientSession, url: str, pattern: str) -> CheckInfo:
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
        logger.info('Error {}: {}'.format(type(ex), str(ex)))
        return CheckInfo(url=url, available=False, request_ts=request_ts, response_time=None,
                         http_code=None, pattern_matched=None)


def get_files(source_filename: str) -> dict:
    with open(source_filename, mode="r") as f:
        urls = json.load(f)

        for item in urls:
            yield item


def send_data(kafka_producer: KafkaProducer, topic_name: str, check_results: List[CheckInfo]):
    # TODO: check errors
    for item in check_results:
        kafka_producer.send(topic_name, dict(item._asdict()))


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--config', required=True, help='configuration file name')
    return parser.parse_args()


def config_logging(args):
    logging.basicConfig(format='%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S', level=logging.INFO)
    logging.info("Web monitor started with options: {}".format(args))


def get_config(args) -> dict:
    with open(args.config) as config_f:
        return yaml.full_load(config_f)


@retry(tries=5, delay=1, backoff=2)
def init_kafka_producer(config: dict) -> KafkaProducer:
    return KafkaProducer(
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        **config['kafka_producer']['connection'],
    )


def check_config(config):
    if config['web_monitoring']['check_frequency'] < 5 or config['web_monitoring']['check_frequency'] > 300:
        raise ValueError('Check frequency must be between 5 and 300')


def main():
    try:
        args = parse_args()
        config_logging(args)

        run(args, get_config(args))
    except KeyboardInterrupt:
        sys.exit('Web monitor stopped.')


if __name__ == "__main__":
    main()
