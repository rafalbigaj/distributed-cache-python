import random
import string
from locust import HttpLocust, TaskSequence, task, seq_task, between


class ConfigTaskSet(TaskSequence):

    TEST_PREFIX = 'load_tests'

    def __init__(self, parent):
        super(ConfigTaskSet, self).__init__(parent)
        self._key_name = ''.join(random.choice(string.ascii_letters) for i in range(64))
        self._value = ''.join(random.choice(string.ascii_letters) for i in range(32))
        self._path = '/config/{}/{}'.format(ConfigTaskSet.TEST_PREFIX, self._key_name)
        self._get_params = {'use_cache': 'true'}
        self._request_name = '/config/{}/<key>'.format(ConfigTaskSet.TEST_PREFIX)
        self._get_suffix = '?use_cache=true'

    @seq_task(1)
    @task(1)
    def set(self):
        self.client.put(self._path, json={'test': self._value}, name=self._request_name)

    @seq_task(2)
    @task(20)
    def get(self):
        name = self._request_name + self._get_suffix
        with self.client.get(self._path, name=name, params=self._get_params, catch_response=True) as response:
            try:
                value = response.json()['test']
                if value != self._value:
                    response.failure('Unexpected value: {}'.format(value))
            except Exception:
                response.failure('Unexpected response: {}'.format(response.text))

    @seq_task(3)
    @task(1)
    def delete(self):
        self.client.delete(self._path, name=self._request_name)


class ConfigTaskSetNoCache(ConfigTaskSet):
    def __init__(self, parent):
        super(ConfigTaskSetNoCache, self).__init__(parent)
        self._get_params = {'use_cache': 'false'}
        self._get_suffix = '?use_cache=false'


class ConfigUser(HttpLocust):
    task_set = ConfigTaskSet
    wait_time = between(0.5, 2.0)


class ConfigUserNoCache(HttpLocust):
    task_set = ConfigTaskSetNoCache
    wait_time = between(0.5, 2.0)
