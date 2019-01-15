"""
Util script for MTGA localization.
Author: B.F.M.

"""
import json

def file_as_bytes(file):
    with file:
        return file.read()

if __name__ == "__main__":
    input_file_name = "result.json"
    target_file_name = "en-kr.json"
    output_file_name = "output.json"

    with open(input_file_name, 'rb') as data_file:
        data = json.load(data_file)

    with open(target_file_name, 'rb') as target_file:
        target = json.load(target_file)

    for d_token in data['tokens']:
        for t_token in target['tokens']:
            if d_token['en'] == t_token['en']:
                t_token['kr'] = d_token['kr']
                #print(t_token['en'], t_token['kr'])

    print("Make ", output_file_name)
    with open(output_file_name, 'bw') as fp:
        fp.write(json.dumps(target, ensure_ascii=False, indent=2).encode('utf-8'))
    print("End")
