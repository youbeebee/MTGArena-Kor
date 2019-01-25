"""
Util script for MTGA localization.
Author: B.F.M.

data_loc_*.mtga에서 한국어 부분을 영어 부분에 덮어쓴다.
"""
import json

def file_as_bytes(file):
    with file:
        return file.read()

if __name__ == "__main__":
    input_file_name = "data_loc_0d8e6d4e3a8685b70898170358e3e7e3.mtga"
    output_file_name = input_file_name

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
    print("End")
