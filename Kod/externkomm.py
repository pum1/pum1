import os
import socket
import sys
import thread
import struct
import sys


class ExternKomm():
    """The external communication manager handles the messages passed through
    the connection manager and configures the connection manager.
    """
    #_message_id_length = struct.calcsize('l')

    def __init__(self, server_port, pull_port, remote_port):
        self._message_types = {
            0001 : ('Connect', '', self.msg_connect),
            0002 : ('Disconnect', '', self.msg_disconnect),
            0003 : ('Open serve channel', '', self.msg_serve),
            0004 : ('Close serve channel', '', self.msg_stop_serve),
            0005 : ('Authenticate', '', self.msg_auth)
            }

        self._clients     = list()
        self._server_port = server_port
        self._pull_port   = pull_port
        self._pull_forward = None
        self._serve_forwards = {}
        self._connection_handler = ConnectionHandler(remote_port)
        self._connection_handler.set_global_channel_reader(
            1, self._global_message_reader)
        self._connection_handler.set_viewer(self)
        self._init_fake_server(pull_port)
#        self._repo_dir = repo_dir
#        self._setup_server(repo_dir)

    def _init_fake_server(self, local_port, timeout = None):
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listen_socket.settimeout(timeout)
        self._listen_socket.bind(('127.0.0.1', local_port))
        self._listen_socket.listen(0)

    def send_msg(self, connection, id, *args):
        message_type = self._message_types[id]
        pack_args = ('l'+message_type[1],id)+args
        msg = struct.pack(*pack_args)
        print 'Send message:'
        print len(msg)
        print pack_args
        connection.send_channel(1, msg)

    def onconnect(self, connection):
        self._clients.append(connection)

    def get_clients(self):
        return self._clients

    def start(self):
        self._connection_handler.begin_listen()

    def stop(self):
        self._listen_socket.close()
        self._connection_handler.close()

#    def send_msg(self, message_id, *args):
#        #self._connetion_handler.send

    def _global_message_reader(self, connection, msg):
        print 'Receive message:'
        print len(msg)
        print msg
        if len(msg) >= 4:
            message_id = struct.unpack_from('l', msg)[0]
            print message_id
            message_type = self._message_types[message_id]
            if message_type:
                print message_type[0]
                if message_type[2]:
                    args = (connection,)+struct.unpack_from(
                        message_type[1],msg[4:]);
                    message_type[2](*args)
                else:
                    print('Callback for message '+message_type[0]+
                          ' not defined')
            else:
                print('Message id '+message_id+' not defined')

    def open_pull_forward(self, connection):
        self.send_msg(connection, 0003)
        self._pull_forward = self._connection_handler.create_outgoing_forward(self._listen_socket, 3, connection)

    def close_pull_forward(self, connection):
        self._connection_handler.close_forward(self._pull_forward)
        self.send_msg(connection, 0004)


#    def pull(self, connection):
#        self.open_pull_channel(connection)
        
    def msg_connect(self, connection):
        print('msg_connect')

    def msg_disconnect(self, connection):
        print('msg_disconnect')

    def msg_serve(self, connection):
        print 'msg_serve!'
        print connection
        self._serve_forwards[connection] = self._connection_handler.create_incoming_forward(self._server_port, 3, connection)

    def msg_stop_serve(self, connection):
        self._connection_handler.close_forward(self._serve_forwards[connection])

    def msg_auth(self, connection, id):
        pass


class ConnectionHandler():
    """Handles all the remote connections.
    """
    def __init__(self, remote_listen_port):
        #, local_client_port, local_server_port
        self._connections = list()
        #self._last_id    = 0
        self._global_reader = {}
        self._forwards      = list()
        #self._forwards        = {}
        #self._last_forward_id = 0
        #self._server_port = local_server_port
        #thread.start_new_thread(self._local_listener, (local_client_port,))
        self._remote_listen_port = remote_listen_port

    def create_outgoing_forward(self, pull_port, channel, connection):
        forward = OutgoingForwarder(
            pull_port, channel,
            connection)
        self._forwards.append(forward)
        return forward

    def create_incoming_forward(self, local_port, channel, connection):
        forward = IncomingForwarder(
            local_port, channel,
            connection)
        self._forwards.append(forward)
        return forward

    def close_forward(self, forward):
        forward.close()
        self._forwards.remove(forward)

    def set_viewer(self, viewer):
        self._viewer = viewer

    def set_global_channel_reader(self, channel, reader):
        """Sets the global reader of a specified channel. Global readers
        also take the connection as an argument.

        global_channel_reader(connection, msg)
        """
        self._global_reader[channel] = reader
        for connection in self._connections:
            connection.set_channel_reader(channel, lambda msg:
                                              reader(connection, msg))

    def GET_FIRST_CONNECTION(self):
        for conn in self._connections:
            return conn

    def begin_listen(self):
        thread.start_new_thread(
            self._remote_listener, (self._remote_listen_port,))

    def _add_connection(self, socket):
        """Add a connection to the connection table.
        """
        #self._last_id += 1
        #id = self._last_id
        connection = RemoteConnection(socket)
        self._connections.append(connection)
        for channel in self._global_reader:
            connection.set_channel_reader(
                channel, lambda msg:
                    self._global_reader[channel](connection, msg))
        self._viewer.onconnect(connection)
        return connection

    def _remote_listener(self, listen_port):
        """Listens to connections from remote clients
        """
        self._dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._dock_socket.bind(('', listen_port))
        self._dock_socket.listen(5)
        while True:
            remote_socket = self._dock_socket.accept()[0]
            self._add_connection(remote_socket)



    #def end_forward(self, forward_id):
    #    None
                
#     def _tunnel_forwarder(self, local_socket, channel, connection):
#         """Forwards data from the local Bazaar client to the remote connection.
#         """
#         string = ' '
#         while string:
#             string = socket.recv(1024)
#             if string:
#                 connection.send_channel(channel, string)
#             else:
#                 source.shutdown(socket.SHUT_RD)
#                 destination.shutdown(socket.SHUT_WR)

    def connect(self, address):
        """Try to connect to the specified TCP/IP address of type tuple
        (ip-adress, tcp-socket).
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        return self._add_connection(sock)

#     def set_out_tunnel_connection_id(self, out_tunnel_connection_id):
#         """Sets the local tunnel destination.
#         """
#         self._out_tunnel_connection_id = out_tunnel_connection_id

    def close(self):
        """Terminates all connections.
        """
        for forward in self._forwards:
            forward.close()
        for connection in self._connections:
            connection.close()
        if self._dock_socket is not None:
            self._dock_socket.close()

class Forwarder():
    def close(self):
        pass

    def _socket_forwarder(self, local_socket, channel, connection):
        connection.set_channel_reader(channel,
                                      lambda msg:
                                          local_socket.sendall(msg))
        string = ' '
        print 'Forwarding...'
        while string:
            string = local_socket.recv(1024)
            if string:
                connection.send_channel(channel, string)
            else:
                connection.set_channel_reader(channel, None)
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_WR)

class IncomingForwarder(Forwarder):
    def __init__(self, local_port, channel, connection, timeout = None):
        """Connects to the local port and forwards the communication between
        it and the specified channel in the connection.
        """
        thread.start_new_thread(self._incoming_forward_connect,
                                (local_port, channel, connection, timeout))
        print 'Forwarding IN from port'
        print local_port

    def _incoming_forward_connect(self, local_port, channel,
                                  connection, timeout):
        self._local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._local_socket.settimeout(timeout)
        self._local_socket.connect(('127.0.0.1', local_port))
        print 'Connected!'
        self._socket_forwarder(self._local_socket, channel, connection)

    def close(self):
        if self._local_socket is not None:
            self._local_socket.close()
            self._local_socket = None


class OutgoingForwarder(Forwarder):
    def __init__(self, listen_socket, channel, connection, timeout = None):
        """Listens to connections made locally to listen_port and then
        forwards the data communication to the specified channel.
        """
        thread.start_new_thread(self._outgoing_forward_listen,
                                (listen_socket, channel, connection, timeout))
        print 'Forwarding OUT'

    def _outgoing_forward_listen(self, listen_socket, channel,
                                 connection, timeout):
        self._local_socket = listen_socket.accept()[0]
        self._socket_forwarder(self._local_socket, channel, connection)

    def close(self):
        if self._local_socket is not None:
            self._local_socket.close()
            self._local_socket = None



class RemoteConnection():
    """A connection to a remote client.
    """
    #_header_length = struct.calcsize('ll')
    
    def __init__(self, socket):
        self._socket = socket
        self._reader = {}
        self._quantifier = StreamQuantifier()
        thread.start_new_thread(self._listen, ())

    def _listen(self):
        string = ' '
        while string:
            string = self._socket.recv(1024)
            if string:
                self._quantifier.append(string)
                msg = self._quantifier.read()
                print '_listened to message:'
                while msg:
                    print len(msg)
                    if len(msg) >= 4:#RemoteConnection._header_length:
                        channel = (struct.unpack_from('l', msg)[0])
                        if self._reader[channel]:#socket.ntohl
                            self._reader[channel](
                                msg[4:])
                    msg = self._quantifier.read()

            else:
                self._socket.shutdown(socket.SHUT_RD)

    def send_channel(self, channel, msg):
        """Sends a message to the remote connection through the specified
        channel.
        """
        _header_length = struct.calcsize('ll')
        packed_message = struct.pack(
            'll',
            (len(msg) + 8), #socket.htonl#RemoteConnection._header_length
            (channel)) + msg#socket.htonl
        print 'send_channel:'
        print len(packed_message)
        self._socket.sendall(packed_message)

    def set_channel_reader(self, channel, reader):
        """Sets the function that will recieve the messages sent to the
        specified channel.

        channel_reader(msg)
        """
        self._reader[channel] = reader

    def close(self):
        """Terminates the connection.
        """
        self._socket.close()


class StreamQuantifier():
    """Converts a stream of characters into packets of variable length.
    """
    _header_length = struct.calcsize('l')

    def __init__(self):
        self._buff = ''

    def read(self):
        if len(self._buff) >= StreamQuantifier._header_length:
            msg_length = struct.unpack_from('l', self._buff)[0]
            print 'Quantifying:'
            print msg_length
            if len(self._buff) >= msg_length:
                msg = self._buff[StreamQuantifier._header_length:msg_length]
                self._buff = self._buff[msg_length:]
                return msg
        return None

    def append(self, data):
        self._buff += data


