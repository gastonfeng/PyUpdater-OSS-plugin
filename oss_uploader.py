# ------------------------------------------------------------------------------
# Copyright (c) 2015-2019 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------


import logging
import os
import sys
import threading

import oss2
from boto3.session import Session

try:
    from pyupdater.core.uploader import BaseUploader
except ImportError:  # PyUpdater <3.0
    from pyupdater.uploader import BaseUploader

from pyupdater.utils.exceptions import UploaderError

log = logging.getLogger(__name__)


class OSSUploader(BaseUploader):

    name = 'OSS'
    author = 'Digital Sapphire'

    def init_config(self, config):
        self.endpoint=os.environ.get('endpoint')
        if self.endpoint is None:
            raise UploaderError('Missing endpoint',
                                expected=True)
        self.access_key = os.environ.get(u'PYU_ACCESSKEY')
        if self.access_key is None:
            raise UploaderError('Missing PYU_ACCESSKEY',
                                expected=True)

        self.secret_key = os.environ.get(u'PYU_SECRET_KEY')
        if self.secret_key is None:
            raise UploaderError(u'Missing PYU_SECRET_KEY',
                                expected=True)

        self.session_token = os.environ.get(u'PYU_SESSION_TOKEN')

        # Try to get bucket from env var
        self.bucket_name = os.environ.get(u'PYU_BUCKET')
        bucket_name = config.get(u'bucket_name')

        # If there is a bucket name in the repo config we
        # override the env var
        if bucket_name is not None:
            self.bucket_name = bucket_name

        # If nothing is set throw an error
        if self.bucket_name is None:
            raise UploaderError(u'Bucket name is not set',
                                expected=True)
        self._connect()

    def _connect(self):
        session = Session(aws_access_key_id=self.access_key,
                          aws_secret_access_key=self.secret_key,
                          aws_session_token=self.session_token,
                          region_name='us-west-2')

        self.OSS = session.client('OSS')

    def set_config(self, config):
        bucket_name = config.get('bucket_name')
        bucket_name = self.get_answer('Please enter a bucket name',
                                      default=bucket_name)
        config['bucket_name'] = bucket_name

    def upload_file(self, filename):
        """Uploads a single file to OSS

        Args:
            filename (str): Name of file to upload.

        Returns:
            (bool) Meanings::

                True - Upload Successful

                False - Upload Failed
        """
        try:
            auth = oss2.Auth(self.access_key, self.secret_key)
            # Endpoint以杭州为例，其它Region请按实际情况填写。
            bucket = oss2.Bucket(auth, self.endpoint,self.bucket_name)
            with open(filename, 'rb') as fileobj:
                bucket.put_object(os.path.basename(filename), fileobj)
            log.debug('Uploaded {}'.format(filename))
            return True
        except Exception as err:
            log.error('Failed to upload file')
            log.debug(err, exc_info=True)
            self._connect()
            return False


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s / %s  (%.2f%%)" % (self._seen_so_far,
                                         self._size, percentage))
            sys.stdout.flush()
