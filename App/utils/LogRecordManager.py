import logging
import os

class LogRecordManager:

    @staticmethod
    def record(text,name):
        print("Log recording")
        newPath = r'../logs/'
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        path = f'../logs/{name}.log'
        logging.basicConfig(filename=path,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        logging.info(text)
