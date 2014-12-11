from apns import APNs, Payload
from tornado import httpserver, ioloop, web, gen
import time, os

class APNS:
    def __init__(self,apns,devicetoken):
        self.apns = apns
        self.devicetoken = devicetoken

    def send(self):
        #token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
        payload = Payload(alert="this is a new message", sound="default", badge=1)
        self.apns.gateway_server.send_notification(1111,time.time()+3600,self.devicetoken, payload, self.success)


    def success(self):
        print "Sent push message to APNS gateway."

    def on_response(self,status, seq):
        print "sent push message to APNS gateway error status %s seq %s" % (status, seq)

    def on_connected(self):
        self.apns.gateway_server.receive_response(self.on_response)

class APNSHandler(web.RequestHandler):
    def initialize(self):
        self.apns = APNs(use_sandbox=True, cert_file='cert.pem', key_file='key.pem')

    def get(self):
        devicetoken = self.get_argument('device_token',None)
        testapns = APNS(self.apns,devicetoken)
        self.apns.gateway_server.connect(testapns.on_connected)
        #testapns.send()
        self.write({'response':'Success'})
	testapns.send()

def main():

   handlers = [(r"/",APNSHandler)]
   settings = {'debug':True}
   application = web.Application(handlers,**settings)
   http_server = httpserver.HTTPServer(application)
   port = int(os.environ.get("PORT", 8888))
   http_server.listen(port)

   ioloop.IOLoop.instance().start()
   ioloop.IOLoop.instance().stop()

if __name__=='__main__':
    main()

