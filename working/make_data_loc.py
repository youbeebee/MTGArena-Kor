"""
Util script for MTGA localization.
Author: B.F.M.

data_loc_*.mtga에서 한국어 부분을 영어 부분에 덮어쓴다.
업데이트시 loc_file_name 수정 필요
"""
import json
import os
import sys
from shutil import copy2

import make_manifest

def main(input_file_name):
    output_file_name = input_file_name
    output_path = "./Downloads/Data/"

    print("Reading...")

    with open(input_file_name, 'rb') as data_file:
        data = json.load(data_file)

    en_data = list(filter(lambda dic: dic['langkey'] == 'EN', data)).pop()
    ko_data = list(filter(lambda dic: dic['langkey'] == 'ko-KR', data)).pop()

    print("Replacing...")
    replace_data(en_data, ko_data)
    #replace_data2(ko_data)

    print("Writing...")
    with open(output_file_name, 'bw') as fp:
        fp.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    # ./Downloads/Data/data_loc_*.mtga로 복사
    copy_outputfile(output_path, output_file_name)

    make_manifest.main(output_file_name)
    print("End")

def copy_outputfile(output_path, output_file_name):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    copy2(output_file_name, output_path)

def replace_data(en_data, ko_data):
    en_token = en_data['keys']
    for i, ko_token in enumerate(ko_data['keys']):
        fill_missed_translation(ko_token)
        if ko_token['text'] == "WWWWWWWWW":
            continue
        else:
            en_token[i]['text'] = ko_token['text']

def replace_data2(data):
    data['langkey'] = "KO"
    for token in data['keys']:
        fill_missed_translation(token)

def fill_missed_translation(token):
    """도빈의 명민함/불타는 나무 부족 기물파괴자"""
    tid = token['id']

    if tid == 280002 and token['text'] == "WWWWWWWWW":
        token['text'] = "당신이 당신의 본단계에 순간마법 주문을 발동할 때마다, 당신은 도빈의 명민함을 소유자의 손으로 되돌릴 수 있다."
    elif tid == 279747 and token['text'] == "WWWWWWWWW":
        token['text'] = "불타는 나무 부족 기물파괴자가 공격할 때마다, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 카드 한 장을 뽑는다."
    else:
        return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        loc_file_name = "data_loc_543fb2443bc2bee017bc11cbe08737ce.mtga"
        print("No arg - default: ", loc_file_name)
    else:
        loc_file_name = sys.argv[1]
        print("arg: ", loc_file_name)

    main(loc_file_name)
