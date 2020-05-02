from flask import Flask, request, jsonify
from distributed_cache import DistributedCache
import os
import http

app = Flask(__name__, instance_relative_config=True)
key_prefix = os.environ['USER_KEY_PREFIX']
distributed_cache = DistributedCache(
    config_path=os.path.join(app.instance_path, 'etcd.config.json'),
    key_prefix=key_prefix,
    logger=app.logger
)


@app.route("/config/<path:config_key>", methods=['GET'])
def get_config(config_key):
    use_cache = request.args.get('use_cache', default='true', type=str) == 'true'
    value = distributed_cache.get(config_key, use_cache)
    app.logger.debug("GET {} -> {}, using cache: {}".format(config_key, value, use_cache))
    return jsonify(value)


@app.route("/config/<path:config_key>", methods=['PUT'])
def set_config(config_key):
    value = request.json
    distributed_cache.put(config_key, value)
    app.logger.debug("SET {} -> {}".format(config_key, value))
    return jsonify(value)


@app.route("/config/<path:config_key>", methods=['DELETE'])
def delete_config(config_key):
    distributed_cache.delete(config_key)
    app.logger.debug("DELETE {}".format(config_key))
    return '', http.HTTPStatus.NO_CONTENT


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
