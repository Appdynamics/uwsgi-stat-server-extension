#!/usr/bin/env python

import socket

try:
    import simplejson as json
except ImportError:
    import json

# Update the namespace for the custom metric
APPD_METRIC_TEMPLATE = "name=Custom Metrics|Hardware Resources|%s|Processes|uwsgi" % (socket.gethostname())

# TODO: Move this to an input from the shell script
WSGI_STATS_SERVER_SOCKET_PATH = "/tmp/corpsite-stat.sock"

class uWSGIStatsProcessor:

    def __init__(self):
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.connect(WSGI_STATS_SERVER_SOCKET_PATH)

    def read_from_socket(self):
        chunks = []
        bytes_recd = 0
        while True:
            chunk = self.s.recv(2048)
            if chunk == '':
                break;
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        return json.loads(''.join(chunks))


class uWSGIStats:

    def __init__(self, data):
        self._uwsgi_workers = [ uWSGIWorker(worker) for worker in data.get('workers') ]


    def total_workers(self):
        return len(self._uwsgi_workers)


    def active_workers(self):
        active_workers = 0

        for uwsgi_worker in self._uwsgi_workers:
            if uwsgi_worker.is_active():
                active_workers += 1

        return active_workers


    def total_harakiri_count(self):
        total_harakiri_count = 0

        for uwsgi_worker in self._uwsgi_workers:
            total_harakiri_count += uwsgi_worker.harakiri_count

        return total_harakiri_count


    def get_metrics(self):
        # Collect global metrics related to uwsgi processes.
        global_uwsgi_metrics = "\n".join([
            "%s|Total Workers, value=%d" % (APPD_METRIC_TEMPLATE, self.total_workers()),
            "%s|Active Workers, value=%d" % (APPD_METRIC_TEMPLATE, self.active_workers()),
            "%s|Total Harakiri Count, value=%d" % (APPD_METRIC_TEMPLATE, self.total_harakiri_count()),
        ])

        # Collect metrics specific for each uwsgi process.
        individual_uwsgi_metrics = "\n".join([uwsgi_worker.get_metrics() for uwsgi_worker in self._uwsgi_workers if uwsgi_worker.is_active() ])

        return "\n".join([global_uwsgi_metrics, individual_uwsgi_metrics])

class uWSGIWorker:

    def __init__(self, data):
        self._id = data.get('id')
        self._pid = data.get('pid')
        self._status = data.get('status')
        self._harakiri_count = data.get('harakiri_count')
        self._exceptions = data.get('exceptions')
        self._running_time = data.get('running_time')
        self._last_spawn = data.get('last_spawn')
        self._tx = data.get('tx')
        self._avg_rt = data.get('avg_rt')
        self._requests = data.get('requests')
        self._respawn_count = data.get('respawn_count')


    def __repr__(self):
        return "pid: %d, status %s, requests %s, harakiri_count, %d" % (
            self.pid, 
            self.status, 
            self.requests, 
            self.harakiri_count
        )


    def get_metrics(self):
        return "\n".join([
            "%s|%s|Total Requests, value=%d" % (APPD_METRIC_TEMPLATE, self.id, self.requests),
            "%s|%s|Harakiri Count, value=%d" % (APPD_METRIC_TEMPLATE, self.id, self.harakiri_count),
            "%s|%s|Total Exceptions, value=%d" % (APPD_METRIC_TEMPLATE, self.id, self.exceptions),
            "%s|%s|Total Running Time (s), value=%d" % (APPD_METRIC_TEMPLATE, self.id, (self.running_time/1000)),
            "%s|%s|Total Transmitted Data (MB), value=%d" % (APPD_METRIC_TEMPLATE, self.id, (self.transmitted_data/(1024*1024))),
            "%s|%s|Respawn Count, value=%d" % (APPD_METRIC_TEMPLATE, self.id, self.respawn_count),
            "%s|%s|Average Response Time (s), value=%d" % (APPD_METRIC_TEMPLATE, self.id, (self.average_response_time/1000)),
        ])


    def is_active(self):
        return self.status != 'cheap'


    @property
    def id(self):
        return self._id


    @property
    def pid(self):
        return self._pid


    @property
    def status(self):
        return self._status


    @property
    def harakiri_count(self):
        return self._harakiri_count


    @property
    def exceptions(self):
        return self._exceptions


    @property
    def running_time(self):
        return self._running_time


    @property
    def last_spawn(self):
        return self._last_spawn


    @property
    def respawn_count(self):
        return self._respawn_count


    @property
    def transmitted_data(self):
        return self._tx


    @property
    def average_response_time(self):
        return self._avg_rt


    @property
    def requests(self):
        return self._requests


if __name__ == '__main__':

    print uWSGIStats(
        uWSGIStatsProcessor().read_from_socket()
    ).get_metrics()            
