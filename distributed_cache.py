from etcd_client import EtcdClient


class DistributedCache(object):
    def __init__(self, config_path, key_prefix, logger):
        self.etcd_client = EtcdClient(config_path, key_prefix, logger, 240)  # reconnect every 4 minutes
        self.logger = logger
        self.key_prefix = key_prefix
        self.cache = {}

    def get(self, key: str, use_cache: bool = True) -> str:
        pass

    def put(self, key: str, value: str):
        pass

    def delete(self, key: str):
        pass
