[![PyPI version](https://badge.fury.io/py/PyUpdater-oss-Plugin.svg)](https://badge.fury.io/py/PyUpdater-oss-Plugin)

# PyUpdater oss plugin

PyUpdater upload plugin for Aliyun oss

## Installing

    $ pip install PyUpdater-oss-plugin


## Configuration

System environmental variables

Optional - If set will be used globally. Will be overwritten when you add oss settings during pyupdater init

| Variable              | Meaning                                 |
| --------------------- |---------------------------------------- |
| PYU_ACCESSKEY           | Your Aliyun api id                      |
| PYU_SECRET_KEY       | You Aliyun api secret                   |
| PYU_SESSION_TOKEN | You Aliyun api session token (optional) |
| PYU_BUCKET       | Bucket name (optional)                  |
