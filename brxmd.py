from markdown_it import MarkdownIt
import argparse
import sys
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.field_list import fieldlist_plugin

md = (
    MarkdownIt("gfm-like")
    .use(dollarmath_plugin)
    .use(anchors_plugin)
    .use(footnote_plugin)
    .use(tasklists_plugin)
    .use(fieldlist_plugin)
)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Brookit's Markdown Extension Bundle")
    parser.add_argument("filename", help="Filename to .md file")
    parser.add_argument("--output", help="Output HTML file")
    args = parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as fobj:
        data = "  \n".join(fobj.read().split("\n"))
    if args.output:
        output = open(args.output, "w", encoding="utf-8")
    else:
        output = sys.stdout
    print(md.render(data), file=output)