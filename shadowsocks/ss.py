# -*- coding: UTF-8 -*-
import threading

from flask import Flask,jsonify

from shadowsocks import User as user
from shadowsocks import server, task
from shadowsocks.common import to_bytes, to_str, IPNetwork
from shadowsocks.shell import check_config
import logging
import sys
import thread
import time

app = Flask(__name__)

#全局变量
config = {}


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

def timer_start():
    t = threading.Timer(5, test_func, ("msg1", "msg2"))
    t.start()

def test_func(msg1,msg2):
    print "I'm test_func,",msg1,msg2
    print ssDict
    timer_start()

userDict = {}
ssDict = {}

if __name__ == '__main__':
    class myThread (threading.Thread):   #继承父类threading.Thread
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter

        def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
            self.taskLoad()

        def taskLoad(self):
            timer_start()
            while True:
                time.sleep(1)

    class serverThread (threading.Thread):   #继承父类threading.Thread
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
        def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
            config = getSimpleConfig()
            server.server_start(config)

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

    thread1 = myThread(1, "Thread-1", 1)
    thread1.start()

    thread2 = myThread(2, "Thread-2", 1)
    thread2.start()

    app.run(port=10000,debug=True)



