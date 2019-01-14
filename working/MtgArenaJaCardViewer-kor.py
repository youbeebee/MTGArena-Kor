"""
Name   : MTG Korean Card Image Downloader
Author : B.F.M.
Date   : 2018/12/14
"""
import requests
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


if __name__ == "__main__":
    print("hello")

    sets = ['dom', 'xln', 'rix', 'm19', 'grn']

    for s in sets:
        download_cards_in_set(s)
