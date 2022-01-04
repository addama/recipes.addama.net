# [recipes.addama.net](http://recipes.addama.net)

Collection of recipes used in my household, generated from Markdown files into a usable website.

## md_convert.py Script

The creation of html files is controlled by `converter/md_convert.py` which should be run any time a recipe is changed or added. 

Run `md_convert.py` from the base directory with `python3 converter/md_convert.py`. You do not have to delete existing html files, but in case they are out of date or incompatible, here are the files generated:
* One `/recipes/*.htm` for every `/markdown/*.md`
* One `/tags/*.htm` for every unique tag
* `index.htm` in the base directory

The script will only generate output files if the markdown file modified date is later than the output file modified date. This can be circumvented with the `-f` or `-c` flags (see below).

### Output

The script outputs a line for every html file that it generates, which includes what kind of file is being generated (recipe, tag, index), the input and output files, if applicable, and how many lines were written. Output can be piped to a file in the console as normal, but can also be suppressed with the `-s` flag (see below).

### Command line flags

There are two command line flags available:

* `-f`, `--force`
  * Forces the regeneration of output files even if no change warrants regeneration
* `-c`, `--clear`
  * Clears out all previously generated html files, then forces the regeneration of all files
* `-s`, `--silent`
  * Suppresses console messages

As `-c` forces regeneration, it supercedes `-f`, though there's no harm in running `-f -c` - it's just redundant.

## Markdown Recipe Format

The recipes are written in Markdown format, but only some semantic elements are parsed, which are:

* `#`, `##`, `###`
  * Three levels of headers
  * The first `#` of the document serves as the recipe title and will be used to refer to the document externally
* `-`
  * Unordered bullets
* `1.`
  * Numbered list item
  * You only need to use `1.` for every list item; do not number your list yourself!
* `[[internal link]]`
  * Converted into an internal link, i.e. to another recipe page. The text between the `[[` and `]]` should be as close to the `/recipes/*.htm` filename as you can, **excluding the extension**, although it will replace spaces with underscores and convert to lowercase for you.
* `&tags`
  * Proprietary "tags" meta element
  * Should contain a commaspace-separated list of tags that apply to the recipe, e.g. `&tags tag1, tag2, tag3`
* `&source`
  * Proprietary "source" meta element
  * Used to keep track of the URL, book, etc, that the recipe came from
* `&pre`
  * Proprietary "preformatted text" meta element
  * Turns on and off preformatted text
  
Ensure that there is a space between the markdown element and the content, e.g. `# Title`, not `#Title`

