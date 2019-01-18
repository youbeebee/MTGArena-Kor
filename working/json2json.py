"""
Util script for MTGA localization.
Author: B.F.M.

"""
import json

def file_as_bytes(file):
    with file:
        return file.read()

if __name__ == "__main__":
    input_file_name = "loc-kr.json"
    target_file_name = "loc-en.json"
    output_file_name = "loc-en_result.json"

    with open(input_file_name, 'rb') as data_file:
        data = json.load(data_file)

    with open(target_file_name, 'rb') as target_file:
        target = json.load(target_file)

    t_token = target['keys']
    for i, d_token in enumerate(data['keys']):
        if d_token['text'] == "WWWWWWWWW":
            continue
        else:
            t_token[i]['text'] = d_token['text']

    print("Make ", output_file_name)
    with open(output_file_name, 'bw') as fp:
        fp.write(json.dumps(target, ensure_ascii=False, indent=2).encode('utf-8'))
    print("End")
