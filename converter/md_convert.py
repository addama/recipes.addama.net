import sys
import glob
import re
from os.path import basename, splitext
from datetime import datetime

run_date = datetime.now()
input_dir = '/markdown/'
output_dir = '/recipes/'
tags_dir = '/tags/'
css_file = '/inc/style.css'
# files = glob.glob(f'.{input_dir}*.md') # 3.6+ string formatting
files = glob.glob('.'+input_dir+'*.md')
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
		'<meta charset="utf-8" />',
		'<meta generatedDate="'+str(run_date)+'" />',
		# '<link rel="preconnect" href="https://fonts.googleapis.com">',
		# '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
		'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=The+Nautigal:wght@700&display=swap" />',
		'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=El+Messiri:wght@700&display=swap" />',
		'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@200&display=swap" />',
		'<link rel="stylesheet" href="'+css_location+css_file+'" />',
		'<title>'+title+'</title>',
		'</head>',
		'<body>',
		'<main>'
	]
	html += content
	html += [
		'</main>',
		'<footer>',
		'<a id="repoLink" href="https://github.com/addama/recipes.addama.net">Github</a> | <span class="generatedDate">Generated '+str(run_date)+'</span>',
		'</footer>',
		'<script type="text/javascript" src="'+css_location+'/inc/change_decoration.js"></script>',
		'</body>',
		'</html>'
	]

	return html

def build_recipe_page(title, tags, steps):
	html = steps
	html += [
		'<div id="tags">',
		'<span id="tagsLabel">Tags</span>'
	]

	for tag in tags:
		html.append('<a href="../tags/'+tag+'.htm" title="Recipes tagged as: '+tag+'">'+tag+'</a>')

	html += [ '</div>' ]

	return build_base_page(title, html)

def build_tag_page(tag, uris):
	html = [
		'<h1>',
		'<span id="decoration">🙞</span>',
		'<span id="tagTitle">Tag: '+tag+'</span>',
		'</h1>',
		'<ul>'
	]

	for uri in uris:
		html.append('<li><a href="..'+output_dir+uri+'">'+titles_by_uri[uri]+'</a></li>')

	html += [ '</ul>' ]

	return build_base_page('Recipes tagged as '+tag, html)

def build_index_page():
	html = [
		'<h1>',
		'<span id="decoration">🙞</span>',
		'<span id="indexTitle">Recipes</span>',
		'</h1>',
		'<h2>Tags</h2>',
		'<div id="indexTagList">'
	]

	for tag in uris_by_tag:
		html.append('<a href="./tags/'+tag+'.htm" title="Recipes tagged as: '+tag+'">'+tag+'</a>')

	html += [
		'</div>',
		'<h2>Recipes</h2>',
		'<div id="indexRecipeList">'
	]

	for uri in titles_by_uri:
		title = titles_by_uri[uri]
		html.append('<a href=".'+output_dir+uri+'" title="'+title+'">'+title+'</a>')

	html += [ '</div>' ]

	return build_base_page('Recipes', html, True)

def process_line(line):
	# Common fractions symbol replacement
	modified = re.sub('(\d)\/(\d)', r'&frac\1\2;', line)
	return modified

def process_file(file):
	filename = splitext(basename(file))[0]+'.htm'
	title = default_title
	is_unordered_list = False
	is_ordered_list = False
	tags = []
	steps = []

	switch = {
		'#':	lambda a: '<h1>'+a[1]+'</h1>',
		'##':	lambda a: '<h2><a id="'+slugify(a[1])+'"></a>'+a[1]+'</h2>',
		'###':	lambda a: '<h3><a id="'+slugify(a[1])+'"></a>'+a[1]+'</h3>',
		'-':	lambda a: '<li>'+process_line(a[1])+'</li>',
		'1.':	lambda a: '<li>'+process_line(a[1])+'</li>',
		'!#':	lambda a: '\n'.join([
			'<h1>',
			'<span id="decoration">🙞</span>',
			'<span id="recipeTitle">'+a[1]+'</span>',
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
				if (split[0] == '&tags' and not len(tags)):
					# Build a uniqued lowercase tags list
					tags = (list(set(split[1].lower().split(', '))))
					tags_by_uri[filename] = tags
					for tag in tags:
						if tag not in uris_by_tag: uris_by_tag[tag] = []
						uris_by_tag[tag].append(filename)
				elif (split[0] == '&source'):
					# Nothing for now, just keeping the URLs in the MD
					pass
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
					steps.append(switch.get(split[0], lambda a: '<p>'+process_line(" ".join(a))+'</p>')(split))
		if (is_ordered_list): steps.append('</ol>')
		if (is_unordered_list): steps.append('</ul>')
	return [ filename, build_recipe_page(title, tags, steps) ]

def write_file(filename, html):
	with open(filename, 'w') as f:
		f.write('\n'.join(html))

# Process the markdown files
for file in files:
	filename, html = process_file(file)
	print(filename, len(html))
	write_file('.'+output_dir+filename, html)

# Build the tag pages
for tag in uris_by_tag:
	html = build_tag_page(tag, uris_by_tag[tag])
	print(tag, len(html))
	write_file('.'+tags_dir+tag+'.htm', html)

# Build the index page
html = build_index_page()
print('index.htm', len(html))
write_file('./index.htm', html)