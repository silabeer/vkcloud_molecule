# This suppresses about 80% of the deprecation warnings from python 3.7.
import warnings
import testinfra.utils.ansible_runner
import os
import pytest


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('webservers')

@pytest.fixture()
def AnsibleDefaults():
    with open("defaults/main.yml", 'r') as stream:
        return yaml.load(stream)

def test_service_httpd(host):
    s = host.service("httpd")
    assert s.is_enabled
    assert s.is_running

def test_service_firewalld(host):
    s = host.service("firewalld")
    assert s.is_enabled
    assert s.is_running

def test_httpd_port(host):
    host.socket("tcp://:::80").is_listening

def test_httpd_live(host):
    cmd = "curl localhost/about.html"
    run = host.run(cmd)
    assert run.rc == 0
    assert "About automatization with Ansible and Molecule" in run.stdout

@pytest.mark.parametrize('file, content', [
    ("/etc/firewalld/zones/public.xml", "port=\"80\""),
    ("/var/www/html/index.html", "My App deployed via Ansible")
    ])

def test_files(host, file, content):
    file = host.file(file)
    assert file.exists
    assert file.contains(content)