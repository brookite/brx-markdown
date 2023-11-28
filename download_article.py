import requests
import argparse
from readability import Document
from markdownify import markdownify as md


def filter_filename(text):
    denied = '*"/\\<>:|?'
    for denied_sym in denied:
        text = text.replace(denied_sym, "")
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download markdown article from URL")
    parser.add_argument("url", help="Article URL")
    args = parser.parse_args()
    r = requests.get(args.url)
    doc = Document(r.text)
    with open(filter_filename(doc.title()) + ".md", "w", encoding="utf-8") as fobj:
        fobj.write(md(doc.summary()))
