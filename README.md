# DropboxUploader

This script upload the file/directory to your personal dropbox via [dropbox-sdk-python](https://github.com/dropbox/dropbox-sdk-python).
You sohuld paste your access token in `token.dat` to work.

## Usage

```
usage: main.py [-h] [--token TOKEN] --tgt TGT --src SRC

optional arguments:
  -h, --help     show this help message and exit
  --token TOKEN
  --tgt TGT      dropbox path
  --src SRC      local file path
```

### Upload a single file

`python main.py --src YOUR_FILE_PATH --tgt YOUR_DROPBOX_PATH`

After executing the command, you will see `YOUR_DROPBOX_PATH/YOUR_FILE` in dropbox.

### Recursive upload files in directory

`python main.py --src YOUR_DIRECTORY_PATH --tgt YOUR_DROPBOX_PATH`

After executingthe command, you will see a directory `YOUR_DIRECTORY_NAME` created under `YOUR_DROPBOX_PATH`, and all the files locally exist in `YOUR_DIRECTORY_PATH
