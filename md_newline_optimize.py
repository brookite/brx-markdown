import argparse
import os


def process_markdown(filepath):
    with open(filepath, "r", encoding="utf-8") as fobj:
        data = fobj.read().split("\n")
    for i in range(len(data)):
        if not data[i].endswith("  "):
            data[i] = data[i] + "  "
    result = "\n".join(data)
    with open(filepath, "w", encoding="utf-8") as fobj:
        fobj.write(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert newlines to standard double-whitespace break in Markdown"
    )
    parser.add_argument("filepath", help="Filename or folder with markdown")
    args = parser.parse_args()
    if os.path.isdir(args.filepath):
        for root, dirs, files in os.walk(args.filepath):
            for file in files:
                if os.path.splitext(file)[-1] == ".md":
                    process_markdown(os.path.join(root, file))
    elif os.path.splitext(args.filepath)[-1] == ".md":
        process_markdown(args.filepath)
    else:
        print("Incorrect file. Choose folder with md or file with extension .md")
