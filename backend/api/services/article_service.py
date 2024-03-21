import re
import emoji


def calculate_reading_time(body: str) -> int:
    """
    Description:
        bodyから改行、#、URLを除去して、文章の読了時間を計算する。
    """

    body = re.sub(r"\n|\#|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", body)
    char_count = len(body)
    return (char_count // 400) + 1


def remove_special_characters(text: str) -> str:
    """
    絵文字を削除する
    """
    return emoji.replace_emoji(string=text)
