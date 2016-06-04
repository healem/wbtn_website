#!../../bin/python

import Models
from peewee_wbtn import PeeweeModels
import ConfigParser

class DbManager():
    wbtnTables = [PeeweeModels.User, PeeweeModels.Whiskey, PeeweeModels.BlogEntry, PeeweeModels.CalculatedScores, PeeweeModels.UserRating]
    configFile = "/home4/healem/keys/wbtn.cnf"
    dbUser = "healem_wbtn"

    def __init__(self, testMode=False):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)
        self.testMode = testMode

        '''Get the password for config file'''
        self.dbPass = self.config.get("db", self.dbUser)

        '''Load test or prod db'''
        if self.testMode:
             self.dbName = self.config.get("db", "test_db")
        else:
             self.dbName = self.config.get("db", "prod_db")

        '''initialize the db'''
        self.db = PeeweeModels.BaseModel.getDbRef()
        self.db.init(self.dbName, user=self.dbUser, passwd=self.dbPass)

        '''make sure db tables are created'''
        self.db.connect()
        self.db.create_tables(self.wbtnTables, safe=True)
        self.db.close

if __name__ == "__main__":
    dbm = DbManager(testMode=True)
