#!/usr/bin/env python3

import csv
import time
import hashlib
import logging
import requests


if __name__ == '__main__':
    start_time = time.time()

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=f'damballa_tester_{start_time}.log',
        level=logging.INFO
    )
    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info('Starting Damballa Test')
    with open('damballa_sources.csv', 'rt', encoding='utf-8') as csvfile:
        cr = csv.reader(csvfile, delimiter=',', quotechar='"')
        columns = next(cr)
        for row in cr:
            source, testfile, expectedhash, expectedsize = row
            logging.info(f'Downloading "{testfile}" from "{source}" with MD5 {expectedhash} and size {expectedsize}')
            try:
                req = requests.get(f'http://{source}/{testfile}', headers={'User-Agent': 'Damballa Alert Tester'})
                reqhash = hashlib.md5(req.content)
                if reqhash.hexdigest() == expectedhash:
                    logging.info(f'Success downloading "{testfile}" from "{source}" hashes match: {expectedhash}')
                else:
                    logging.info(f'Success downloading "{testfile}" from "{source}" hashes do not match: Expected {expectedhash}, Returned {reqhash}')
            except Exception as e:
                logging.exception(e)

    logging.info(f'Completed Damballa Test in {time.time() - start_time} seconds')
