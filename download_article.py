import requests
import argparse
from readability import Document
from markdownify import markdownify as md


def filter_filename(text):
    denied = '*"/\\<>:|?'
    for denied_sym in denied:
        text = text.replace(denied_sym, "")
    return text


def download_article(url):
    r = requests.get(args.url)
    doc = Document(r.text)
    return doc.title(), md(doc.summary())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download markdown article from URL")
    parser.add_argument("url", help="Article URL")
    args = parser.parse_args()
    title, summary = download_article(args.url)
    with open(filter_filename(title) + ".md", "w", encoding="utf-8") as fobj:
        fobj.write(summary)
