import sys
import logging
import argparse


def run_handler(args):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--data_saver_type', type=str, choices=('postgre_sql'), help='the name of a file with url list')
    return parser.parse_args()


def config_logging(args):
    logging.basicConfig(format='%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S', level=logging.INFO)
    logging.info("Web monitor started with options: {}".format(args))


if __name__ == '__main__':
    try:
        args = parse_args()
        config_logging(args)
        run_handler(args)
    except KeyboardInterrupt:
        sys.exit('Web monitor stopped.')
    except Exception as e:
        msg = 'Web monitor stopped unexpectedly. Error: {}'.format(e)
        logging.info(msg)
        sys.exit(msg)
