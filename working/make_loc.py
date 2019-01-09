"""
Util script for MTGA localization.
Author: B.F.M.

loc-CAB 파일에서 data_loc_*.mtga 파일을 만들기 위한 작업 자동화
업데이트마다 output_file_name 수정 필요.
"""

def file_as_bytes(file):
    with file:
        return file.read()

if __name__ == "__main__":
    input_file_name = "loc-CAB-en.txt"
    template_file_name = "template_loc-CAB.txt"
    output_file_name = "loc-CAB-801ca563fd5c741f4df88bc57e20d635-13642596834344483412-TextAsset.txt"

    input_file = file_as_bytes(open(input_file_name, 'rb'))
    input_file = input_file.replace(b'\r\n', b'\\r\\n')  # 파일의 개행문자를 텍스트로 변경

    template_file = file_as_bytes(open(template_file_name, 'rb'))
    template_file = template_file.replace(b'[replace_here]', input_file)  # 템플릿 파일과 합침

    print("Make ", output_file_name)
    output_file = open(output_file_name, 'wb')
    output_file.write(template_file)
    output_file.close()
    print("End")
