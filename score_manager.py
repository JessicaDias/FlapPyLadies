# encoding: utf-8
import json
import os
from hex_encoding import (encode, decode)
from config_manager import (ConfigManager, APPKEY)


CONFIG_SESSION = 'saveconf'


class ScoreManager(object):

    def __init__(self):
        self.configuration = ConfigManager()

    def initialize(self):
        self.configuration.load()
        self.saveconfigs = self.configuration.get_session(CONFIG_SESSION)
        self.savefolder = self.saveconfigs.get('savepath')
        self.filepath = os.path.join(self.savefolder,
                                     self.saveconfigs.get('filename'))

        self.code_key = self.__retrieve_appkey()
        self.load_score()

    def load_score(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as savefile:
                self.highscore = self.__read(savefile)
        else:
            if not os.path.exists(self.savefolder):
                os.makedirs(self.savefolder)
            self.highscore = 0
            self.save_score(self.highscore)

    def save_score(self, points):
        if points < self.highscore:
            return

        with open(self.filepath, 'w+') as savefile:
            scores = {
                "highscores": points
            }
            self.__write(savefile, json.dumps(scores))
        self.highscore = points

    def __retrieve_appkey(self):
        appkey = self.saveconfigs.get(APPKEY)
        if not appkey:
            return self.configuration.generate_appkey(CONFIG_SESSION)
        return appkey

    def __write(self, savefile, scores):
        string_scores = encode(self.code_key, str(scores))
        savefile.write(string_scores)

    def __read(self, savefile):
        string_scores = decode(self.code_key, savefile.read())
        return json.loads(string_scores).get('highscores')
