from argparse import ArgumentParser
from pathlib import Path
from re import search, compile
from time import sleep

import ibis  # Template Engine
import minify_html  # Minifier
from dateutil.parser import parse
from mistletoe import markdown  # Markdown Renderer


def _load_twtxt_from_file(txt_path: str) -> dict:
    _txt_path = Path(txt_path)
    _tweets = {}  # Day -> Entries
    if _txt_path.exists():
        raw = _txt_path.read_text("utf-8").strip().splitlines()
        pattern = compile(r"^(?P<date>[^\t]+)\t(?P<entry>.+)$")
        for index, line in enumerate(raw):
            result = search(pattern, line)
            if not result:
                print(f"Invalid entry L#{index+1}")
                continue

            _parsed_date = parse(result.group(1)).date().isoformat()
            if not _tweets.get(_parsed_date):
                _tweets[_parsed_date]: list = []
            _tweets[_parsed_date].append([index, markdown(result.group(2))])
    return _tweets


def _render_html(tweets: dict, output_file: str, template_file: str):
    if not Path(template_file).exists():
        exit(f"Template {template_file} doesn't exist!")
    loader = ibis.loaders.FileLoader(".")
    template = loader(template_file)
    fh = Path(output_file)
    return fh.write_text(minify_html.minify(template.render(tweets=tweets), minify_css=True, minify_js=True), "utf-8")


def _watch(output_file, input_file, template_file):
    current_mtime = Path(input_file).stat().st_mtime
    try:
        print(f"Watching {input_file}. CTRL+C to interrupt.")
        while True:
            new_mtime = Path(input_file).stat().st_mtime
            if new_mtime > current_mtime:
                current_mtime = new_mtime
                print(
                    input_file,
                    "updated:",
                    _render_html(_load_twtxt_from_file(input_file), output_file, template_file),
                )
            sleep(15)
    except KeyboardInterrupt:
        exit(0)


arg = ArgumentParser(description="Picoblog builds an html file using a template from a twtxt (https://twtxt.readthedocs.io) feed.")
arg.add_argument("input", help="Input file (TWTXT format)")
arg.add_argument("output", help="Output file (HTML)")
arg.add_argument("-t", "--template", default="template.html", help="Template to use (HTML)")
arg.add_argument("-w", "--watch", action="store_true", help="Watch input file for changes (15s)")
args = arg.parse_args()
print("\033[1;4mPicoblog (Python Version)\033[0m")
if args.watch:
    _watch(input_file=args.input, output_file=args.output, template_file=args.template)
else:
    print("Done", _render_html(tweets=_load_twtxt_from_file(args.input), output_file=args.output, template_file=args.template))
