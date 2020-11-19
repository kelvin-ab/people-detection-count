import os
import logging
import configparser
import tornado.web
import tornado.ioloop
import tornado.websocket as ws

active_clients = set()


class SocketServer(ws.WebSocketHandler):

    @classmethod
    def route_urls(cls):
        return [(r'/', cls, {}), ]

    def open(self):
        if self not in active_clients:
            active_clients.add(self)
            logging.info("New client connected")
            logging.info("# of active connections : " + str(len(active_clients)))

    def on_message(self, message):
        for client in active_clients:
            if client != self:
                logging.info("send")
                client.write_message(message)

    def on_close(self):
        if self in active_clients:
            self.request.connection.no_keep_alive = True
            active_clients.remove(self)
            logging.info("Connection closed")
            logging.info("# of active connections : " + str(len(active_clients)))

    def check_origin(self, origin):
        return True


if __name__ == '__main__':
    logging.basicConfig(
        level=getattr(logging, os.getenv('LOGLEVEL', '').upper(), 'INFO'),
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    )
    config = configparser.ConfigParser()
    config.read('config.ini')
    soc_host = config['SOCKET']['HOST']
    soc_port = int(config['SOCKET']['PORT'])
    app = tornado.web.Application(SocketServer.route_urls(), websocket_max_message_size=50000000)
    app.listen(soc_port)
    tornado.ioloop.IOLoop.instance().start()
