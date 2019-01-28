"""
Util script for MTGA localization.
Author: B.F.M.

"data_loc_*.mtga" 파일을 통해 downloads.manifest 파일을 수정해준다.
업데이트마다 data_loc파일 이름과 매니페스트 템플릿 파일 내용 수정 필요.
"""
import hashlib
import os
import sys

def get_md5(file_name):
    return hashlib.md5(file_as_bytes(open(file_name, 'rb'))).hexdigest()

def file_as_bytes(file):
    with file:
        return file.read()

def get_size(file_name):
    statinfo = os.stat(file_name)
    return statinfo.st_size

def main(file_name):
    template_path = "./template/"
    output_path = "./Downloads/"
    manifest_template_name = template_path+"template_downloads.manifest"

    print("Make downloads.manifest")
    print("loc: ", file_name)

    file_hash = get_md5(file_name)
    file_size = get_size(file_name)

    print("MD5: ", file_hash)
    print("Size: ", file_size)

    manifest_template = file_as_bytes(open(manifest_template_name, 'rb'))

    content_new = manifest_template.decode() \
                .replace('file_length_here', str(file_size)) \
                .replace('file_hash_here', file_hash) \
                .replace('\r\n', '\n')

    # ./Downloads/downloads.manifest로 복사
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    new_manifest = open(output_path+"downloads.manifest", 'w')
    new_manifest.write(content_new)

    new_manifest.close()
    print("Make manifest end")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_name = "data_loc_0d8e6d4e3a8685b70898170358e3e7e3.mtga"
        print("No arg - default: ", file_name)
    else:
        file_name = sys.argv[1]
        print("arg: ", file_name)

    main(file_name)
