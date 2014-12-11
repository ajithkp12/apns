from tornado import ioloop
from testapns import APNS
from apns import APNs, Payload
import time

apns = APNs(use_sandbox=True, cert_file='cert.pem', key_file='key.pem')
devicetoken = 'cc093df3b17819d46056a952f491df2ab281fe839363c7d55103e5b9b5d91606'
test = APNS(apns,devicetoken)
apns.gateway_server.connect(test.on_connected)

# Wait for the connection and send a notification
ioloop.IOLoop.instance().add_timeout(time.time()+5, test.send)

ioloop.IOLoop.instance().start()
