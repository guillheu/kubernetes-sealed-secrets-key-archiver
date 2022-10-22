# kubernetes-sealed-secrets-key-archiver
addition to a sealed-secrets app to automatically back up and encrypt all sealed-secrets tls secrets

https://hub.docker.com/r/guillh/kubernetes-sealed-secrets-key-archiver

## Motivation

Sealed secrets require TLS sealing keys to be stored directly in the kubernetes cluster. However, there is no disaster recovery put in place by the sealed-secrets app, so those keys would be lost for good after a catastrophic failure, making all sealed secrets in the cluster unusable and losing potentially unrecoverable data.<br>
The goal of this simple container is to back up those keys and save the on disk as a GPG encrypted archive, where they can hopefully be backed up off-site.

## How it works

The container assumes several resources are available :
 * must be deployed in a Pod in a Kubernetes cluster (and have access to [the standard service account token and namespace file](https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/#directly-accessing-the-rest-api))
 * the file `/gpg/key.pub` must contain the public key with which to encrypt the final backup
 * the environment variable `KEY_OWNER` must be defined and contain the name of the GPG key owner
 * the `/tmp` directory within the container must NOT be mounted onto.

With all those conditions met, the container will output an encrypted backup file of all the sealing keys every 30 days into the `/archive` folder. It is highly recommended to mount a volume onto that location to save those backups to disk.