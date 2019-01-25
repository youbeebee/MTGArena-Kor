"""
Util script for MTGA localization.
Author: B.F.M.

data_loc_*.mtga에서 한국어 부분을 영어 부분에 덮어쓴다.
"""
import json
import os
import sys
import make_manifest

from shutil import copy2

def file_as_bytes(file):
    with file:
        return file.read()

def main(input_file_name):
    output_file_name = input_file_name
    output_path = "./Downloads/Data/"

    print("Reading: ", input_file_name)

    with open(input_file_name, 'rb') as data_file:
        data = json.load(data_file)

    en_data = list(filter(lambda kor: kor['langkey'] == 'EN', data)).pop()
    ko_data = list(filter(lambda kor: kor['langkey'] == 'ko-KR', data)).pop()

    print("Replacing...")
    en_token = en_data['keys']
    for i, ko_token in enumerate(ko_data['keys']):
        if ko_token['text'] == "WWWWWWWWW":
            continue
        else:
            en_token[i]['text'] = ko_token['text']

    print("Writing ", output_file_name)
    
    with open(output_file_name, 'bw') as fp:
        fp.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    # ./Downloads/Data/data_loc_*.mtga로 복사
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    copy2(output_file_name, output_path)

    make_manifest.main(input_file_name)
    print("End")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        loc_file_name = "data_loc_0d8e6d4e3a8685b70898170358e3e7e3.mtga"
        print("No arg - default: ", loc_file_name)
    else:
        loc_file_name = sys.argv[1]
        print("arg: ", loc_file_name)

    main(loc_file_name)
