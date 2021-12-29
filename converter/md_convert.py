import sys
import glob
from os import getcwd
from os.path import basename, splitext
from datetime import datetime

run_date = datetime.now()
# base_dir = getcwd()
input_dir = '/markdown/'
output_dir = '/recipes/'
tags_dir = '/tags/'
css_file = '/inc/style.css'
print(f'.{input_dir}*.md')
files = glob.glob(f'.{input_dir}*.md')
default_title = 'Recipe'
title_suffix = ' | addama.net'
tags_by_uri = {}
titles_by_uri = {}
uris_by_tag = {}

slugify = lambda a: '_'.join(a.lower().split(' '))

def build_base_page(title, content, isIndex=False):
	css_location = '.' if isIndex else '..'
	html = [
		'<!DOCTYPE html>',
		'<html>',
		'<head>',
		'<meta charset="UTF-8" />',
		f'<meta generatedDate="{run_date}" />',
		f'<link rel="stylesheet" href="{css_location}{css_file}" />',
		f'<title>{title}</title>',
		'</head>',
		'<body>',
		'<main>'
	]
	html += content
	html += [
		'</main>',
		'<footer>',
		f'<span class="generatedDate">Generated: {run_date}</span>',
		'</footer>',
		'</body>',
		'</html>'
	]

	return html

def build_recipe_page(title, tags, steps):
	html = steps
	html += [
		'<div id="tags">',
		'<span class="decoration">Tags</span>',
	]
	# tags
	for tag in tags:
		html.append(f'<a href="../tags/{tag}.htm" title="Recipes tagged as: {tag}">{tag}</a>')

	html += [ '</div>' ]

	return build_base_page(title, html)

def build_tag_page(tag, uris):
	html = [
		'<h1>',
		'<a class="decoration" href="../" title="Back to index">🙞</a>',
		f'<span id="tagTitle">Tag: {tag}</span>',
		'</h1>',
		'<ul>'
	]

	# build files list
	for uri in uris:
		html.append(f'<li><a href="..{output_dir}{uri}">{titles_by_uri[uri]}</a></li>')

	html += [ '</ul>' ]

	return build_base_page(f'Recipes tagged as {tag}', html)

def build_index_page():
	html = [
		'<h1>',
		'<span class="decoration">🙞</span>',
		'<span id="indexTitle">Recipes</span>',
		'</h1>'
		'<h2>Tags</h2>',
		'<div id="indexTagList">'
	]

	for tag in uris_by_tag:
		html.append(f'<a href="./tags/{tag}.htm" title="Recipes tagged as: {tag}">{tag}</a>')

	html += [
		'</div>',
		'<h2>Recipes</h2>',
		'<div id="indexRecipeList">'
	]

	for uri in titles_by_uri:
		title = titles_by_uri[uri]
		html.append(f'<a href=".{output_dir}{uri}" title="{title}">{title}</a>')

	html += [ '</div>' ]

	return build_base_page('Recipes', html, True)


def process_file(file):
	filename = f'{splitext(basename(file))[0]}.htm'
	title = default_title
	is_unordered_list = False
	is_ordered_list = False
	tags = []
	steps = []

	switch = {
		'#': lambda a: f'<h1>{a[1]}</h1>',
		'##': lambda a: f'<h2><a id="{slugify(a[1])}"></a>{a[1]}</h2>',
		'###': lambda a: f'<h3><a id="{slugify(a[1])}"></a>{a[1]}</h3>',
		'&&': lambda a: f'<h1>{a[1]}</h1>',
		'-': lambda a: f'<li>{a[1]}</li>',
		'1.': lambda a: f'<li>{a[1]}</li>',
		'!#': lambda a: '\n'.join([
			'<h1>',
			'<a class="decoration" href="../" title="Back to index">🙞</a>',
			f'<span id="recipeTitle">{a[1]}</span>',
			'</h1>'
		])
	}

	with open(file, 'r') as f:
		for line in f:
			# Separate the markdown from the content
			split = line.rstrip().split(' ', 1)
			# Ignore empty lines
			if (len(split) > 1):
				# Use the first H1 as the document title
				# Modify the command, and pass through to the next if
				if (split[0] == '#' and title == default_title):
					title = split[1]
					titles_by_uri[filename] = title
					split[0] = '!#'

				# Deal with the metadata that doesn't get printed, then
				# with the printables
				if (split[0] == '&&' and not len(tags)):
					# Build a uniqued lowercase tags list
					tags = (list(set(split[1].lower().split(', '))))
					tags_by_uri[filename] = tags
					
					for tag in tags:
						if tag not in uris_by_tag:
							uris_by_tag[tag] = []
						uris_by_tag[tag].append(filename)
				else:
					if (split[0] == '-' and not is_unordered_list): 
						is_unordered_list = True
						steps.append('<ul>')
					elif (split[0] != '-' and is_unordered_list):
						is_unordered_list = False
						steps.append('</ul>')
					elif (split[0] == '1.' and not is_ordered_list):
						is_ordered_list = True
						steps.append('<ol>')
					elif (split[0] != '1.' and is_ordered_list):
						is_ordered_list = False
						steps.append('</ol>')
					steps.append(switch.get(split[0], lambda a: f'<p>{" ".join(a)}</p>')(split))
		if (is_ordered_list): steps.append('</ol>')
		if (is_unordered_list): steps.append('</ul>')
	return [ filename, build_recipe_page(title, tags, steps) ]

# Process the markdown files
for file in files:
	filename, html = process_file(file)
	print(filename, len(html))
	with open(f'.{output_dir}{filename}', 'w') as f:
		f.write('\n'.join(html))

# Build the tag pages
for tag in uris_by_tag:
	html = build_tag_page(tag, uris_by_tag[tag])
	print(tag, len(html))
	with open(f'.{tags_dir}{tag}.htm', 'w') as f:
		f.write('\n'.join(html))

# Build the index page
html = build_index_page()
print(f'./index.htm', len(html))
with open(f'./index.htm', 'w') as f:
	f.write('\n'.join(html))