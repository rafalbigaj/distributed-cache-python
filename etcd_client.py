import base64
import os
import json
import etcd3
import inspect
from threading import Thread, Lock
from time import sleep


class SafeWatcher(etcd3.watch.Watcher):
    def _run(self):
        try:
            super(SafeWatcher, self)._run()
        except ValueError:
            pass


etcd3.watch.Watcher = SafeWatcher


class EtcdClient(object):
    """
    @DynamicAttrs
    """

    def __init__(self, config_path, key_prefix, logger, reconnect_after=240):
        grpc = EtcdClient._load_grpc_config(config_path)
        cert_path = EtcdClient._load_cert_path(
            os.path.dirname(config_path),
            grpc['certificate']['certificate_base64'],
            grpc['certificate']['name']
        )

        self.logger = logger
        self.key_prefix = key_prefix
        self.cache = {}
        self.connection_args = {
            'host': grpc['hosts'][0]['hostname'],
            'port': grpc['hosts'][0]['port'],
            'user': grpc['authentication']['username'],
            'password': grpc['authentication']['password'],
            'ca_cert': cert_path
        }
        self._etcd3_client = None
        self._watch_id = None
        self._lock = Lock()

        self._reconnect()
        if reconnect_after is not None:
            self._schedule_reconnect(reconnect_after)

        self._delegate_client_methods()

    @staticmethod
    def _load_cert_path(config_dir, cert_base64, cert_name):
        cert = base64.b64decode(cert_base64)
        cert_path = os.path.join(config_dir, '{}.cert'.format(cert_name))
        with open(cert_path, 'wb') as f:
            f.write(cert)
        return cert_path

    @staticmethod
    def _load_grpc_config(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config['connection']['grpc']

    def _reconnect(self):
        with self._lock:
            self._close()
            self._connect()

    def _schedule_reconnect(self, reconnect_after):
        def run_scheduler():
            while True:
                sleep(reconnect_after)
                self._reconnect()

        Thread(target=run_scheduler).start()

    def _connect(self):
        self._etcd3_client = etcd3.client(**self.connection_args)

    def _close(self):
        if self._etcd3_client is not None:
            self._etcd3_client.close()

    @staticmethod
    def create_delegator(self, client_method):
        def delegator(*args, **kwargs):
            print(self, *args, **kwargs)
            with self._lock:
                o = getattr(self, '_etcd3_client')
                m = getattr(o, client_method)
                return m(*args, **kwargs)
        return delegator

    def _delegate_client_methods(self):
        etcd3_client_methods = inspect.getmembers(self._etcd3_client, predicate=inspect.ismethod)
        for method, _ in etcd3_client_methods:
            setattr(self, method, EtcdClient.create_delegator(self, method))


