# [recipes.addama.net](http://recipes.addama.net)
Collection of recipes used in my household

## md_convert.py Script

The creation of html files is controlled by `md_convert.py` which should be run any time a recipe is changed or added. 

Run `md_convert.py` from the base directory with `python3 converter/md_convert.py`. You do not have to delete existing html files, but in case they are out of date or incompatible, here are the files generated:
* One `/recipes/*.htm` for every `/markdown/*.md`
* One `/tags/*.htm` for every unique tag
* `index.htm` in the base directory

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

