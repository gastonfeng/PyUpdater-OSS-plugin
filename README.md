[![PyPI version](https://badge.fury.io/py/PyUpdater-OSS-Plugin.svg)](https://badge.fury.io/py/PyUpdater-OSS-Plugin)

# PyUpdater OSS plugin

PyUpdater upload plugin for Aliyun OSS

## Installing

    $ pip install PyUpdater-OSS-plugin


## Configuration

System environmental variables

Optional - If set will be used globally. Will be overwritten when you add OSS settings during pyupdater init

| Variable              | Meaning                                 |
| --------------------- |---------------------------------------- |
| PYU_ACCESSKEY           | Your Aliyun api id                      |
| PYU_SECRET_KEY       | You Aliyun api secret                   |
| PYU_SESSION_TOKEN | You Aliyun api session token (optional) |
| PYU_BUCKET       | Bucket name (optional)                  |
