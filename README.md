# Picoblog (Python Version)
_Picoblog_ is my somewhat opinionated interpretation and usage of [twtxt](https://twtxt.readthedocs.io/en/latest/index.html). It started it's life as a [PHP script](https://0xff.nu/picoblog), but seeing as I mostly forgot how to write and use PHP as well as the fact that I now use Python as part of work, I figured I'll rewrite it.
The rendered file is now static, as I figured I don't necessarily update it often enough for it to be dynamic.

This code is provided as an example, although you're more than welcome to use it as is (your own template provided, of course!).

## Notes
- The code is small, simple and lacks documentation and error handling. If you feel this needs to be amended, open a PR.
- Entries were intended to be shown and grouped by date, hence `_tweets[_parsed_date]: list = []`.
  You can omit this behavior in the code, or in your template.
- I use [`minify-html`](https://github.com/wilsonzlin/minify-html) to make the resulting HTML smaller in size although you can skip this.
- I use a template engine called [Ibis](https://www.dmulholl.com/docs/ibis/). This too you can omit and just concat HTML together if you wish.
- Picoblog is using [mistletoe](https://github.com/miyuchina/mistletoe) to parse Markdown in leue of a limited subset as I didn't want to screw around with writing a parser, and I couldn't find anything smaller.
- Message/entry ID was dropped. I am now using dates (YYYYMMDD) to link to a specific twt (or day, rather).
- Watch mode (`--watch|-w`) is looking for changes every 15 seconds via file changed time.

## Usage
```
usage: main.py [-h] [-t TEMPLATE] [-w] input output

Picoblog builds an html file using a template from a twtxt (https://twtxt.readthedocs.io) feed.

positional arguments:
  input                 Input file (TWTXT format)
  output                Output file (HTML)

options:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Template to use (HTML)
  -w, --watch           Watch input file for changes (15s)
```

## Template
Here's a very (VERY) basic template usage:
```django
<div class="entries">
    {% for date, entries in tweets.items() %}
    <section class="day" id="{{ date }}">
    {% for entry in entries %}
        <article class="entry">{{ entry.1 }}</article>
    {% endfor %}
    </section>
    {% endfor %}
</div>
```

## TODO
- Add handler to parse twtxt mentions (`@<example http://example.org/twtxt.txt>`).