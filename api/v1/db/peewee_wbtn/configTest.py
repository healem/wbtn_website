#!../../bin/python
import ConfigParser

configFile = "/home4/healem/keys/wbtn.cnf"

config = ConfigParser.ConfigParser()
config.read(configFile)
readPw = config.get("db", "healem_read")
print("Read only pw: {0}".format(readPw))

