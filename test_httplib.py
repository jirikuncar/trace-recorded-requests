from ddtrace import config, patch, tracer

config.httplib["distributed_tracing"] = True
patch(httplib=True)

import http.client
import urllib3
import pytest

@pytest.mark.parametrize("id_", range(100))
@pytest.mark.parametrize("url", ("www.datadoghq.com", "docs.datadoghq.com"))
def test_httplib(vcr_cassette, ddspan, id_, url):
        conn = http.client.HTTPSConnection(url)
        conn.request("GET", "/")
        with tracer.trace("request"):
            r1 = conn.getresponse()
        assert 200 == r1.status
        assert 'OK' == r1.reason


@pytest.mark.parametrize("id_", range(100))
@pytest.mark.parametrize("url", ("www.datadoghq.com", "docs.datadoghq.com"))
def test_urllib3(vcr_cassette, ddspan, id_, url):
    http = urllib3.PoolManager()
    with tracer.trace("request"):
        r = http.request("GET", url)
    assert 200 == r.status
