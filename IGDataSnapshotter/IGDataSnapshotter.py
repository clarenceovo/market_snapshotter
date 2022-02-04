import requests
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IGDataSnapshotter:
    def __init__(self, username, password, api_key):
        self.__IG_ENDPOINT = "https://api.ig.com/gateway/deal"
        self._identifier = username
        self._password = password
        self._api_key = api_key
        self.x_security_token = None
        self.cst = None
        self._create_session()

    def __get_header(self):
        return {
            "X-IG-API-KEY":self._api_key,
            "Version":str(1),
            "Content-Type":"application/json; charset=UTF-8",
            "Accept":"application/json; charset=UTF-8",
            "X-SECURITY-TOKEN":self.x_security_token,
            "CST":self.cst
        }

    def _create_session(self):
        logger.info("Creating IG Session...")
        header = self.__get_header()

        ret = requests.post(url=self.__IG_ENDPOINT+'/session',headers=header,json={
            "identifier":self._identifier,
            "password": self._password,
            "encryptedPassword": None
        })

        if 'X-SECURITY-TOKEN' in ret.headers and 'CST' in ret.headers:
            logger.info('IG Session is created successfully!')
            self.cst = ret.headers['CST']
            self.x_security_token = ret.headers['X-SECURITY-TOKEN']

        else:
            logger.error("Failed to create user session")
            raise Exception



    def get_market(self,market_id):
        header = self.__get_header()
        ret = requests.get(url=self.__IG_ENDPOINT+'/markets/'+market_id,headers=header)
        return ret.json()