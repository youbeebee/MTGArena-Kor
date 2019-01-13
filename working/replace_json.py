"""
Util script for MTGA localization.
Author: B.F.M.

한국어 - 영어 json으로 loc-CAB-*-TextAsset.txt 파일을 만들어 줌
이 파일을 data_loc_*.mtga에 넣음
업데이트마다 템플릿, json 수정 필요.
"""
import json

def file_as_bytes(file):
    with file:
        return file.read()

if __name__ == "__main__":
    template_path = "./template/"
    input_file_name = "en-kr.json"
    template_file_name = template_path+"orig_en.dat"
    loc_template_file_name = template_path+"template_loc-CAB.txt"
    output_file_name = "loc-CAB-801ca563fd5c741f4df88bc57e20d635-13642596834344483412-TextAsset.txt"

    with open(input_file_name, 'rb') as data_file:
        data = json.load(data_file)

    template_file = file_as_bytes(open(template_file_name, 'rb'))

    print("Replacing...")
    for token in data['tokens']:
        en_token = '"'+token['en'].replace('"', '\\"')+'"'
        kr_token = '"'+token['kr'].replace('"', '\\"')+'"'
        template_file = template_file.replace(en_token.encode(), kr_token.encode())
    #template_file = template_file.replace(b'\\"', b'\\\\"')  # 따옴표 변경
    template_file = template_file.replace(b'\r\n', b'\\r\\n')  # 파일의 개행문자를 텍스트로 변경

    print("Merging...")
    loc_template = file_as_bytes(open(loc_template_file_name, 'rb'))
    loc_template = loc_template.replace(b'[replace_here]', template_file)  # 템플릿 파일과 합침

    print("Make ", output_file_name)
    output_file = open(output_file_name, 'wb')
    output_file.write(loc_template)
    output_file.close()
    print("End")
