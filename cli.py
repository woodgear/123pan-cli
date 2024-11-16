#!/bin/env python3

import os
import requests


def fetch_files(auth_token, parent_file_id=0, limit=100, last_file_id=None):
    url = "https://open-api.123pan.com/api/v2/file/list"
    headers = {
        "Authorization": f"{auth_token}",
        "Platform": "open_platform",
        "Content-Type": "application/json",
    }
    params = {"parentFileId": parent_file_id, "limit": limit}
    if last_file_id is not None:
        params["lastFileId"] = last_file_id

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return (None, f"Failed to fetch files: {response.status_code} {response.text}")
    data = response.json()
    data = data.get("data", {})
    last_file_id = data.get("lastFileId", -1)
    file_list = data.get("fileList", [])
    if last_file_id == -1:
        return ((file_list, None), None)
    return ((file_list, last_file_id), None)


def main():
    auth_token = os.getenv("PAN_123_ACCESS_TOKEN")
    flist = {type: "dir", "path": "/", "name": "root", "list": []}
    tasks = [([0], flist)]
    while tasks:
        (cur_task, cur_flist) = tasks.pop()
        all = []
        (fs, last), err = fetch_files(auth_token, parent_file_id=cur_task)
        if err is not None:
            print(err)
            continue
        all.extend(fs)
        while last is not None:
            (fs, last), err = fetch_files(
                auth_token, parent_file_id=cur_task, last_file_id=last
            )
            if err is not None:
                print(err)
                continue
            all.extend(fs)
        for f in all:
            file_type = "file" if f["type"] == 0 else "dir"
            if file_type == "file":
                file = {
                    "type": "file",
                    "path": cur_flist["path"] + "/" + f["filename"],
                    "filename": f["filename"],
                    "etag": f["etag"],
                    "parentFileId": f["parentFileId"],
                    "size": f["size"],
                    "createAt": f["createAt"],
                    "updateAt": f["updateAt"],
                    "fileId": f["fileId"],
                }
                cur_flist["list"].append(file)
                print(
                    f"f: {file["path"]} {file["etag"]} {file["size"]} {file["createAt"]} {file["updateAt"]}"
                )
            if file_type == "dir":
                dir = {
                    "type": "dir",
                    "path": cur_flist["path"] + "/" + f["filename"],
                    "filename": f["filename"],
                    "etag": f["etag"],
                    "parentFileId": f["parentFileId"],
                    "size": f["size"],
                    "createAt": f["createAt"],
                    "updateAt": f["updateAt"],
                    "fileId": f["fileId"],
                    "list":[]
                }
                cur_flist["list"].append(dir)
                print(f"d: {dir["path"]} {dir["createAt"]} {dir["updateAt"]}")
                tasks.append((f["fileId"], dir))


if __name__ == "__main__":
    main()
