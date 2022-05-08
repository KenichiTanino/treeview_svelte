#!/usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fs import open_fs
# import base64
from urllib.parse import quote

import etc.settings as settings

app = FastAPI()

# CORS
origins = [
    'http://localhost:5000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/ft")
async def get_folder():
    """
    フォルダーツリーAPI:

    ルートディレクトリからの全ツリーをjson形式で返却する

    JSON形式は以下。
```
[
  { id: 0, text: "", type: 'Folder', children: [{id: }] },
]
```

- id: ユニークな数値
- text: ファイル名(or フォルダ名)
- type: ファイルタイプ(以降追加)
  - Folder
  - DocumentBlank
  - Document(未使用)
- children: 子要素
    """
    root_tree, folder_tree_ids = get_tree()
    return root_tree


def get_tree():
    dir = settings.FOLDER_DIR
    folder_tree = []
    # id: path
    folder_tree_ids = {}
    folder_fs = open_fs(dir)
    id = 1
    # ディレクトリを全抽出
    for path in sorted(folder_fs.walk.dirs(path="/")):
        now_tree = dict(id=id, type='Folder', text=path, children=[])
        folder_tree_ids[id] = path;
        id += 1
        for file in folder_fs.walk.files(path=path, max_depth=1):
            # ディレクトリ配下のファイルを子として格納
            now_tree['children'].append(dict(id=id, type='DocumentBlank', text=file))
            folder_tree_ids[id] = file;
            id += 1
        folder_tree.append(now_tree)
    # root_dir file            
    for file in sorted(folder_fs.walk.files(path="/", max_depth=1)):
        folder_tree.append(dict(id=id, type='DocumentBlank', text=file))
        folder_tree_ids[id] = file;
        id += 1

    # root
    root_tree = dict(id=0, type='Folder', text='/', children=folder_tree)

    return [root_tree], folder_tree_ids


@app.get("/ft/{file_id}")
async def get_folder_content(file_id: int):
    """
    フォルダーツリーAPI:
    ファイル内容を返却する。
    ディレクトリだった場合、空の内容を返却する。
    - fileid: tree内のid
    - 
    戻り
    - name: ファイル名(フルパス/URLquote)
    - content: ファイル内容(Base64)
    """
    root_tree, folder_tree_ids = get_tree()

    dir = settings.FOLDER_DIR
    folder_fs = open_fs(dir)
    content = None
    name = ""
    with folder_fs.openbin(folder_tree_ids[file_id]) as file:
        content = file.read()
    # return dict(content=base64.b64encode(content), name=quote(folder_tree_ids[file_id]))
    return dict(content=content, name=quote(folder_tree_ids[file_id]))


from pydantic import BaseModel


class FileContent(BaseModel):
    content: str

    class Config:
        orm_mode = True


class FolderContent(BaseModel):
    id: int
    content: str


@app.put("/ft/{file_id}")
async def put_folder_filepath(file_id: int, fcontent: FileContent)  -> FolderContent:
    """
    フォルダーツリーAPI:

    ファイル内容を修正する。
    200: 成功
    """
    root_tree, folder_tree_ids = get_tree()

    dir = settings.FOLDER_DIR
    folder_fs = open_fs(dir)
    with folder_fs.openbin(folder_tree_ids[file_id], "w") as file:
        file.write(fcontent.content.encode())

    # 読み込み
    content = None
    with folder_fs.openbin(folder_tree_ids[file_id]) as file:
        content = file.read()
    return dict(id=file_id, content = content)


@app.post("/ft/{file_id}")
async def post_folder_filepath():
    """
    フォルダーツリーAPI:

    ファイル内容を新規作成する。
    file_id: フォルダのid
    """
    pass


@app.post("/ft/folder/{fp}")
async def create_folder():
    """
    フォルダーツリーAPI:

    フォルダを新規作成する。
    """
    pass


@app.delete("/ft/{file_id}")
async def delete_folder_file_id(file_id: int):
    """
    フォルダーツリーAPI:

    file idを削除する。
    """
    pass