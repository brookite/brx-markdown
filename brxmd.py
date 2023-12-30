import argparse
import sys

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.field_list import fieldlist_plugin


def _wikiimage_inline(state, silent: bool):
    if state.src[state.pos] != "!" or state.src[state.pos + 1] != "[" or state.src[state.pos + 2] != "[":
        return False
    try:
        end = state.src.index("]]", state.pos + 3)
    except ValueError:
        return False

    text = state.src[state.pos + 3 : end]
    if not text.strip():
        return False

    try:
        index = text.index("|")
        link = text[:index]
        res = text[index + 1 :]
        if not res:
            width, height = None, None
        else:
            res = res.split("x")
            if len(res) == 2:
                width, height = res
            else:
                width, height = None, None
    except ValueError:
        link = text
        width, height = None, None

    if not silent:
        token = state.push("wikiimage", "wiki", 0)
        token.content = link
        token.attrSet("width", width)
        token.attrSet("height", height)

    state.pos = end + 2
    return True


def wikiimage_plugin(md):
    md.inline.ruler.before(
        "escape",
        "wikiimage",
        _wikiimage_inline,
    )

    def render_wikiimage(self, tokens, idx, options, env) -> str:
        src = str(tokens[idx].content)

        width = tokens[idx].attrGet("width")
        height = tokens[idx].attrGet("height")
        if str(width).isdigit():
            width = str(width) + "px"
        if str(height).isdigit():
            height = str(height) + "px"

        width = 'width="{}" '.format(width)
        height = 'height="{}"'.format(height)
        args = ''
        if tokens[idx].attrGet("width"):
            args += width
        if tokens[idx].attrGet("height"):
            args += height
        return f'<img class="wikiimage" src="{src}" {args}></img>'

    md.add_render_rule("wikiimage", render_wikiimage)


def _highlights_inline(state, silent: bool):
    if state.src[state.pos] != "=" or state.src[state.pos + 1] != "=":
        return False
    try:
        end = state.src.index("==", state.pos + 2)
    except ValueError:
        return False

    text = state.src[state.pos + 2 : end]
    if not text.strip():
        return False

    if not silent:
        token = state.push("highlight", "highlight", 0)
        token.content = text

    state.pos = end + 2
    return True


def highlights_plugin(md):
    md.inline.ruler.before(
        "escape",
        "highlight",
        _highlights_inline,
    )

    def render_highlight(self, tokens, idx, options, env) -> str:
        label = str(tokens[idx].content)
        return f'<mark>{label}</mark>'

    md.add_render_rule("highlight", render_highlight)



def _wikilinks_inline(state, silent: bool):
    if state.src[state.pos] != "[" or state.src[state.pos + 1] != "[":
        return False
    try:
        end = state.src.index("]]", state.pos + 2)
    except ValueError:
        return False

    text = state.src[state.pos + 2 : end]
    if not text.strip():
        return False

    try:
        index = text.index("|")
        link = text[:index]
        label = text[index + 1 :]
    except ValueError:
        link = text
        label = link

    if not silent:
        token = state.push("wikilink", "wiki", 0)
        token.content = label
        token.attrSet("link", link)

    state.pos = end + 2
    return True


def wikilinks_plugin(md):
    md.inline.ruler.before(
        "escape",
        "wikilink",
        _wikilinks_inline,
    )

    def render_wikilink(self, tokens, idx, options, env) -> str:
        label = str(tokens[idx].content)
        link = str(tokens[idx].attrGet("link"))
        return f'<a class="wikilink" href="{link}">{label}</a>'

    md.add_render_rule("wikilink", render_wikilink)


def brx_markdown(html_support=True, newline_break=True):
    return (
        MarkdownIt("gfm-like", {"html": html_support, "breaks": newline_break})
        .use(dollarmath_plugin)
        .use(anchors_plugin)
        .use(footnote_plugin)
        .use(tasklists_plugin)
        .use(fieldlist_plugin)
        .use(wikilinks_plugin)
        .use(wikiimage_plugin)
        .use(highlights_plugin)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brookit's Markdown Extension Bundle")
    parser.add_argument("filename", help="Filename to .md file")
    parser.add_argument("--output", help="Output HTML file")
    args = parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as fobj:
        data = fobj.read()
    if args.output:
        output = open(args.output, "w", encoding="utf-8")
    else:
        output = sys.stdout
    print(brx_markdown().render(data), file=output)
