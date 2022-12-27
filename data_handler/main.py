import sys
import logging
import argparse
import yaml

from kafka import KafkaConsumer


def run_handler(args, config):
    consumer = init_kafka_consumer(config)
    for msg in consumer:
        print(msg)


def get_config(args):
    with open(args.config) as config_f:
        return yaml.full_load(config_f)


def init_kafka_consumer(config):
    return KafkaConsumer(config['kafka_consumer']['topic'],
                         group_id=config['kafka_consumer']['group_id'],
                         bootstrap_servers=config['kafka_consumer']['bootstrap_servers'])


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--config', required=True, help='configuration file name')
    parser.add_argument('--data_saver_type', type=str, default='postgre_sql', choices=('postgre_sql'),
                        help='the name of a file with url list')
    return parser.parse_args()


def config_logging(args):
    logging.basicConfig(format='%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S', level=logging.INFO)
    logging.info("Data handler started with options: {}".format(args))


if __name__ == '__main__':
    try:
        args = parse_args()
        config_logging(args)

        run_handler(args, get_config(args))
    except KeyboardInterrupt:
        sys.exit('Data handler stopped.')
    except Exception as e:
        msg = 'Data handler stopped unexpectedly. Error: {}'.format(e)
        logging.info(msg)
        sys.exit(msg)
