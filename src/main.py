#!/usr/bin/env python3

from kubernetes import client, config, watch
from yaml import safe_dump
from time import sleep
from ast import literal_eval
from os import system, environ, remove
from datetime import datetime

timer = 720 # in hours


def main():

    print("Adding %s's pubkey to gpg..." % (environ.get("KEY_OWNER")))
    system("gpg --import /gpg/key.pub")

    config.load_incluster_config()

    v1 = client.CoreV1Api()
    with open("/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
        namespace = f.readline()

    while True:
        save(v1, namespace)
        print("Done ! See you in a bit !")
        sleep(60*60*24)


    # w = watch.Watch()
    # for event in w.stream(v1.list_namespaced_secret(namespace="sealed-secrets"), timeout_seconds=10):
    #     print("Event: %s %s" % (event['type'], event['object'].metadata.name))

def save(client, namespace):
    print("Fetching secrets...")
    with open("/tmp/tempkeys", 'w') as file:
        safe_dump(client.list_namespaced_secret(namespace=namespace, label_selector="sealedsecrets.bitnami.com/sealed-secrets-key=active").to_dict(), file)
    print("Secrets found. Encrypting secrets...")
    system("gpg --output /archive/sealed-secrets-backup_%s.gpg --encrypt --armor --recipient %s --trust-model always /tmp/tempkeys" % (datetime.now().strftime("%m-%d-%Y_%H-%M-%S"), environ.get("KEY_OWNER")))
    print("deleting temp file...")
    remove("/tmp/tempkeys")


if __name__ == '__main__':
    main()