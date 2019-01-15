"""
Name   : MTG Korean Card Image Downloader
Author : B.F.M.
Date   : 2018/12/14
"""
import requests
import json
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

def download_image(kor_image_url, file_name):
    """
    이미지 다운로드
    :param kor_image_url: 한국어 gatherer 카드 이미지 URL
    (http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={id}&type=card)
    :param file_name: 저장할 파일 이름(확장자 x), 일반적으로 일본어 MultiverseID
    :return:
    """
    img_data = requests.get(kor_image_url).content
    with open('images/{0}'.format(file_name), 'wb') as handler:
        handler.write(img_data)

def get_jap_id(card):
    """
    :param card: mtgsdk의 Card 객체
    :return id: 일본어 MultiverseID
    """
    card_jap = list(filter(lambda kor: kor['language'] == 'Japanese', card.foreign_names)).pop()
    return card_jap['multiverseid']

def get_kor_url(card):
    """
    :param card: mtgsdk의 Card 객체
    :return url: 한국어 카드 이미지 URL
    """
    card_kor = list(filter(lambda kor: kor['language'] == 'Korean', card.foreign_names)).pop()
    url = card_kor['imageUrl']
    return url

def download_cards_in_set(s):
    cards = Card.where(set=s).all()
    print("Set: {0}, #={1}".format(s, len(cards)))
    for card in cards:
        if card.name in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
            continue #기본대지는 다운로드하지 않음
        print(card.name)
        url = get_kor_url(card)
        multiverseid = get_jap_id(card)
        download_image(url, multiverseid)

def make_token_list(sets):
    token_list = []

    for s in sets:
        cards = Card.where(set=s).all()
        print("Set: {0}, #={1}".format(s, len(cards)))

        for card in cards:
            if card.name in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
                continue #기본대지는 다운로드하지 않음

            try:
                card_kor = list(filter(lambda kor: kor['language'] == 'Korean', card.foreign_names)).pop()
            except IndexError:
                print("  Exception: ", card.name)
                continue

            # 카드 이름 추가
            name_dict = {
                "en": card.name,
                "kr": card_kor['name']
            }
            token_list.append(name_dict)

            # 플레이버 텍스트 추가
            if card.flavor is None:
                pass #do nothing
            else:
                flavor_dict = {
                    "en": card.flavor,
                    "kr": card_kor['flavor']
                }
                token_list.append(flavor_dict)

            # 능력 추가
            if card.original_text is None:
                pass
            else:
                en_txt_list = card.original_text.split('\n')
                kr_txt_list = card_kor['text'].split('\n')

                for i, _ in enumerate(en_txt_list):
                    text_dict = {
                        "en": en_txt_list[i],
                        "kr": kr_txt_list[i]
                    }
                    if text_dict not in token_list:
                        token_list.append(text_dict)
            #break
    #print(token_list)

    return token_list


if __name__ == "__main__":
    print("hello")

    sets = ['dom', 'xln', 'rix', 'm19', 'grn', 'rna']
    #sets = ['dom', 'xln', 'rix', 'm19', 'grn']

    #for s in sets:
    #    download_cards_in_set(s)

    tokens = make_token_list(sets)

    #token_json = json.dumps(tokens)
    with open('result.json', 'bw') as fp:
        token_json = json.dumps(tokens, ensure_ascii=False, indent=2).encode('utf-8')
        fp.write(token_json)
        #이후에 " \(.+\)"로 리마인드 텍스트 제거, "\" —"로 플레이버에 줄바꿈 넣어줘야 <i> 제거, raid, enrage에는 추가
        #{1} 같은 비용 수정, 서사시 수정, 플레인즈워커 -비용 수정, 작은따옴표 수정
