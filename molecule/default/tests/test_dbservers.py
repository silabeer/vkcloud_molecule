# This suppresses about 80% of the deprecation warnings from python 3.7.
import warnings
import testinfra.utils.ansible_runner
import os
import pytest


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('dbservers')

@pytest.fixture()
def AnsibleDefaults():
    with open("defaults/main.yml", 'r') as stream:
        return yaml.load(stream)

def test_service_httpd(host):
    s = host.service("mysqld")
    assert s.is_enabled
    assert s.is_running

def test_service_firewalld(host):
    s = host.service("firewalld")
    assert s.is_enabled
    assert s.is_running

def test_httpd_port(host):
    host.socket("tcp://:::3306").is_listening

@pytest.mark.parametrize('file, content', [
    ("/etc/firewalld/zones/public.xml", "port=\"3306\""),
    ("/root/.my.cnf", "password='MySQL@007'")
    ])

def test_files(host, file, content):
    file = host.file(file)
    assert file.exists
    assert file.contains(content)