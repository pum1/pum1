import os
import socket
import sys
import thread
import struct
import sys
from bzrlib import workingtree
from bzrlib.smart.server import SmartTCPServer
import bzrlib
import bzrlib.smart
from bzrlib.transport.remote import RemoteTCPTransport

from externkomm import ExternKomm


class InternKomm():
    def __init__(self, pull_port):
        self._pull_port = pull_port

    def set_repo(self, repo):
        self._repository = repo

    def set_external_comm(self, ext_comm):
        self._external_comm = ext_comm

    def pull_all(self):
        for connection in self._external_comm.get_clients():
            self._external_comm.open_pull_forward(connection)
            self._repository.pull(self._pull_port)
            self._external_comm.close_pull_forward(connection)

class Repository():
    def __init__(self, directory = None, server_port = 10128):
        self._initialize_bazaar(directory, server_port)

    def _initialize_bazaar(self, directory, server_port):
        self._server_port = server_port
        if directory is None:
            directory = os.getcwd()
        self._working_tree = workingtree.WorkingTree.open(directory)
        self._initialize_bazaar_server(directory, server_port)

    def _initialize_bazaar_server(self, directory, server_port):
        from bzrlib import urlutils
        from bzrlib.transport import get_transport
        from bzrlib.transport.chroot import ChrootServer
        url = urlutils.local_path_to_url(directory)
        url = 'readonly+' + url
        print url
        chroot_server = ChrootServer(get_transport(url))
        chroot_server.setUp()
        t = get_transport(chroot_server.get_url())
        print chroot_server.get_url()
        self._bazaar_server = SmartTCPServer(
            t, 'localhost', server_port)
        self._bazaar_server.start_background_thread()

    def close(self):
        self._bazaar_server.stop_background_thread()

    def pull(self, pull_port):
        from bzrlib.branch import Branch
        other_branch = Branch.open(
            'bzr://localhost:'+str(pull_port)+'/')
        self._working_tree.merge_from_branch(other_branch)
        changes = self._working_tree.changes_from(
            self._working_tree.basis_tree())
        print "%s files modified, %s added, %s removed" % (
            len(changes.modified), len(changes.added), len(changes.removed))




class ConsoleTest():
    def __init__(self, args):
        self._remote_port       = 10126
        self._local_client_port = 10127
        self._local_server_port = 10128
        self._dir = None
        for arg in sys.argv:
            if arg[0:1] == '-':
                cc = arg[1:2]
                if cc == 'c':
                    self._local_client_port = int(arg[2:])
                elif cc == 's':
                    self._local_server_port = int(arg[2:])
                elif cc == 'r':
                    self._remote_port = int(arg[2:])
                elif cc == 'd':
                    self._dir = arg[2:]
        self._extern_comm = ExternKomm(
            self._local_server_port, self._local_client_port,
            self._remote_port)
        self._intern_comm = InternKomm(
            self._local_client_port)
        self._repository = Repository(self._dir, self._local_server_port)
        self._intern_comm.set_repo(self._repository)
        self._intern_comm.set_external_comm(self._extern_comm)
        self._extern_comm.start()

    def cmd_loop(self):
        while True:
            s = raw_input(">")
            cmd = s.split()
            if(cmd):
                if(cmd[0] == 'connect'):
                    self._extern_comm._connection_handler.connect(
                        (cmd[1], int(cmd[2])))
                elif(cmd[0] == 'who'):
                    print self._extern_comm.get_clients()
                elif(cmd[0] == 'tunnel'):
#                    self._extern_comm._connection_handler.set_out_tunnel_connection_id(
 #                       int(cmd[1]))
                    pass
                elif(cmd[0] == 'start'):
                    self._extern_comm.start()
                elif(cmd[0] == 'stop'):
                    self._extern_comm.stop()
                    break
                elif(cmd[0] == 'send'):
                    self._extern_comm._connection_handler._connection[
                        int(cmd[1])].send_channel(int(cmd[2]), cmd[3])
                elif(cmd[0] == 'pull'):
                    self._intern_comm.pull_all()
                else:
                    print 'Unknown command.'




#connection_handler = ConnectionHandler(remote_port, local_client_port, local_server_port)
#comm = Comm(remote_port, local_client_port, local_server_port)
ca = ConsoleTest(sys.argv)
ca.cmd_loop()
