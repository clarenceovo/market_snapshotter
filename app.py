import redis
import requests
import schedule
import logging
import json
import os
import sys
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from IGDataSnapshotter.IGDataSnapshotter import IGDataSnapshotter

class app:
    def __init__(self):
        self.get_credential()
        self.get_ticker()
        self.ig_conn = IGDataSnapshotter(self.credential['identifier'], self.credential['password'], self.credential['api_key'])
        self.quote ={}

    def get_credential(self):
        f = open('config/credential.json')
        if f:
            self.credential = json.load(f)
        else:
            self.credential = None

        if self.credential is None:
            logger.error("FATAL: Missing Credential")
            sys.exit()
    def get_ticker(self):
        f = open('config/ticker.json')
        if f:
            self.ticker = json.load(f)
        else:
            self.ticker = None

        if self.ticker is None:
            logger.error("FATAL: Missing Ticker")
            sys.exit()

    def get_bo_dict(self,bid,ask):
        return {
            "bid":bid,
            "ask":ask
        }

    def get_snapshot(self):
        for ticker in self.ticker.keys():
            ret = self.ig_conn.get_market(self.ticker[ticker])
            if 'snapshot' in ret.keys():
                ret = ret['snapshot']
                self.quote[ticker]= self.get_bo_dict(ret['bid'],ret['offer'])
            else:
                logger.info(f"Instrument Error:{ticker}")
                print(ret)

    def get_quote(self):
        #Put the Quote to Redis
        print(self.quote)

    def run(self):
        logger.info("Start running the Data collection loop...")
        self.get_snapshot()
        self.get_quote()
        schedule.every(0.5).minutes.do(self.get_snapshot)
        schedule.every(5).seconds.do(self.get_quote)
        while True:
            try:
                schedule.run_pending()
            except Exception as e:
                logger.error(e)
                self._stop()
                sys.exit(0)
            time.sleep(0.0001)


if __name__ == '__main__':
    bot = app()
    bot.run()




