# -*- coding: UTF-8 -*-
from flask import Flask,jsonify

from shadowsocks import User as user
from shadowsocks import server
from shadowsocks.common import to_bytes, to_str, IPNetwork
from shadowsocks.shell import check_config
import logging
import sys

app = Flask(__name__)


@app.route('/addUser', methods=['GET'])
def addUser():
    newUser = user.User()
    (newName, newPassword) = newUser.addUser()
    return jsonify({'name':newName,'password':newPassword})


@app.route('/addTestUser', methods=['GET'])
def addTestUser():
    newUser = user.User()
    (newName, newPassword) = newUser.addUser(test=True)
    return jsonify({'name':newName,'password':newPassword})


def getSimpleConfig():
    config = {}

    VERBOSE_LEVEL = 5
    config['password'] = to_bytes(config.get('password', b''))
    config['method'] = to_str(config.get('method', 'aes-256-cfb'))
    config['port_password'] = ssDict
    config['timeout'] = int(config.get('timeout', 300))
    config['fast_open'] = config.get('fast_open', False)
    config['workers'] = config.get('workers', 1)
    config['pid-file'] = config.get('pid-file', '/var/run/shadowsocks.pid')
    config['log-file'] = config.get('log-file', '/var/log/shadowsocks.log')
    config['verbose'] = config.get('verbose', False)
    config['local_address'] = to_str(config.get('local_address', '127.0.0.1'))
    config['local_port'] = config.get('local_port', 1080)
    config['server'] = to_str(config.get('server', '0.0.0.0'))

    logging.getLogger('').handlers = []
    logging.addLevelName(VERBOSE_LEVEL, 'VERBOSE')
    level = logging.INFO
    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        config['forbidden_ip'] = \
        IPNetwork(config.get('forbidden_ip', '127.0.0.0/8,::1/128'))
    except Exception as e:
        logging.error(e)
        sys.exit(2)

    check_config(config, False)
    return config


if __name__ == '__main__':
    userDict = {}
    ssDict = {}

    try:
        userFile = open(user.fileName, "r")
        for line in userFile:
            oneUserStr = line.split(",")
            if (cmp(oneUserStr[0], user.port) < 0):
                user.port = oneUserStr[0]
            oneUser = {oneUserStr[0], oneUserStr[1], oneUserStr[2]}
            userDict[oneUserStr[0]] = oneUser
            ssDict[oneUserStr[0]] = oneUserStr[1]
        userFile.close()
    except:
        f = open(user.fileName, 'w')
        f.close()

    newUser = user.User()
    newUser.userDict = userDict

    config = getSimpleConfig()
    server.server_start(config)

    app.run(port=10000,debug=True)
