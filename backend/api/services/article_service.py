import re
import time

import emoji
import requests
from bs4 import BeautifulSoup


def calculate_reading_time(body: str) -> int:
    """
    bodyから改行、#、URLを除去して、文章の読了時間を計算する。
    """

    body = re.sub(r"\n|\#|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", body)
    char_count = len(body)
    return (char_count // 400) + 1


def remove_special_characters(text: str) -> str:
    """
    記事のタイトルに含まれる絵文字を削除する
    """
    return emoji.replace_emoji(string=text)


def get_qiita_ogp_image_url(article_url: str):
    """
    Qiitaの記事のOGP画像URLを取得する。取得できない場合はNoneを返す。
    """
    time.sleep(1)
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, "html.parser")
    og_image = soup.find("meta", property="og:image")

    if not og_image:
        return None

    return og_image["content"]
