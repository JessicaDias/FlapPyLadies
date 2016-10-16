# encoding: utf-8
import ConfigParser
from hex_encoding import randomstring
from singleton import Singleton

CONFIG_FILE = 'config.ini'
APPKEY = 'appkey'


class ConfigManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.configuration = ConfigParser.ConfigParser()

    def load(self):
        self.configuration.read(CONFIG_FILE)

    def get_session(self, session):
        items = self.configuration.options(session)
        session_dict = {}
        for item in items:
            session_dict.update(
                dict.fromkeys([item], self.__get_config(session, item)))
        return session_dict

    def generate_appkey(self, session):
        key = randomstring(6)
        self.configuration.set(session, APPKEY, key)
        with open(CONFIG_FILE, 'w+') as config_file:
            self.configuration.write(config_file)
        return key

    def __get_config(self, session, key):
        return self.configuration.get(session, key)
