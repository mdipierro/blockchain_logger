#
# Created by Massimo Di Pierro
# Date: 2017
# License: MIT
#

import os
import json
import uuid
import csv
import hashlib
import datetime

class BlockchainLogger(object):

    def timestamp(self):
        return datetime.datetime.now().isoformat()

    def __init__(self, filename, data=None):
        self.filename = filename
        data = data or str(uuid.uuid4())
        if os.path.exists(filename):
            with open(filename) as myfile:
                reader = csv.reader(myfile)
                for row in reader:
                    self.last_timestamp, self.last_data, self.last_hash = row
        else:
            self.last_timestamp = self.timestamp()
            self.last_data = data
            self.last_hash = ''
            self.write()

    def write(self):
        with open(self.filename,'a') as myfile:
            writer = csv.writer(myfile)
            row = [self.last_timestamp, self.last_data, self.last_hash]
            writer.writerow(row)

    def record(self, data):
        self.last_timestamp = self.timestamp()
        self.last_data = data
        args = (self.last_timestamp, self.last_data, self.last_hash)
        self.last_hash = BlockchainLogger.hash(*args)
        self.write()

    @staticmethod
    def hash(timestamp, data, hash):
        token = '%s:%s:%s' % (timestamp, data, hash)
        return hashlib.sha1(token).hexdigest()

    @staticmethod
    def verify(filename):
        with open(filename) as myfile:
            reader = csv.reader(myfile)
            prev = None
            for row in reader:
                if prev:
                    new_hash = BlockchainLogger.hash(row[0], row[1], prev[2])
                    if row[2] != new_hash: return False
                prev = row
                print 'x'
        return True

def test():
    bc = BlockchainLogger('test.blockchain')
    for data in ['This','is','a','Test']:
        bc.record(data)
    assert BlockchainLogger.verify('test.blockchain')

if __name__ == '__main__':
    test()
