import os
import time
from argparse import ArgumentParser

import dropbox


class DropBoxUpload:
    def __init__(self, token, timeout=900, chunk=8):
        self.token = token
        self.timeout = timeout
        self.chunk = chunk

    def UpLoadFile(self, upload_path, file_path):
        dbx = dropbox.Dropbox(self.token, timeout=self.timeout)
        file_size = os.path.getsize(file_path)
        CHUNK_SIZE = self.chunk * 1024 * 1024
        dest_path = os.path.join(upload_path, os.path.basename(file_path))
        since = time.time()
        with open(file_path, 'rb') as f:
            uploaded_size = 0
            if file_size <= CHUNK_SIZE:
                dbx.files_upload(f.read(), dest_path)
                time_elapsed = time.time() - since
                print('Uploaded {:.2f}%'.format(100).ljust(15) + ' --- {:.0f}m {:.0f}s'.format(time_elapsed // 60,
                                                                                               time_elapsed % 60).rjust(
                    15))
            else:
                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                           offset=f.tell())
                commit = dropbox.files.CommitInfo(path=dest_path)
                while f.tell() <= file_size:
                    if ((file_size - f.tell()) <= CHUNK_SIZE):
                        dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                        time_elapsed = time.time() - since
                        print(
                            'Uploaded {:.2f}%'.format(100).ljust(15) + ' --- {:.0f}m {:.0f}s'.format(time_elapsed // 60,
                                                                                                     time_elapsed % 60).rjust(
                                15))
                        break
                    else:
                        dbx.files_upload_session_append_v2(f.read(CHUNK_SIZE), cursor)
                        cursor.offset = f.tell()
                        uploaded_size += CHUNK_SIZE
                        uploaded_percent = 100 * uploaded_size / file_size
                        time_elapsed = time.time() - since
                        print('Uploaded {:.2f}%'.format(uploaded_percent).ljust(15) + ' --- {:.0f}m {:.0f}s'.format(
                            time_elapsed // 60, time_elapsed % 60).rjust(15), end='\r')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--token", type=str, default="token.dat")
    parser.add_argument("--tgt", type=str, help="dropbox path", required=True)
    parser.add_argument("--src", type=str, help="local file path", required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    with open(args.token) as f:
        token = f.read().strip()

    uploader = DropBoxUpload(token)

    dropbox_path = os.path.join("/", args.tgt)
    local_path = args.src

    if os.path.isfile(local_path):
        uploader.UpLoadFile(os.path.join("/", args.tgt), args.src)
    elif os.path.isdir(local_path):
        local_base_dir = os.path.basename(os.path.normpath(local_path))
        for root, dirs, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                local_relative_path = os.path.relpath(local_file_path, local_path)
                dropbox_file_path = os.path.join(dropbox_path, local_base_dir, os.path.dirname(local_relative_path))
                uploader.UpLoadFile(dropbox_file_path, os.path.basename(local_relative_path))
    else:
        print("Invalid file path")
