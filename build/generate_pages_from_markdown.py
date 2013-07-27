import os
import markdown
from markdown.postprocessors import Postprocessor
from termcolor import colored

def humanize(filename):
  uncapitalized = ['a', 'an', 'and', 'at', 'by', 'from', 'of', 'on', 'or', 'the', 'to', 'with', 'without']
  name = os.path.splitext(filename)[0]
  words = [word[0].upper() + word[1:] if word not in uncapitalized else word for word in name.split('_')]
  title = ' '.join(words)
  title = title[0].upper() + title[1:]
  return title

if __name__ == '__main__':
  markdown_template_file = open('templates/markdown_template.html', 'r')
  markdown_template = markdown_template_file.read()

  processor = markdown.Markdown()
  count = 0


  for root, subFolders, files in os.walk('markdown'):
    for filename in files:
      input_path = os.path.join(root, filename)
      output_dir = root.replace('markdown', 'templates/gen', 1)
      output_path = os.path.splitext(os.path.join(output_dir, filename))[0] + '.html'
      input_file = open(input_path, 'r')
      input_text = input_file.read()

      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      output_file = open(output_path, 'w')

      print colored("Generating %s from %s" % (output_path, input_path), "yellow")
      html_output = processor.convert(input_text)

      output_text = markdown_template.replace('[title]', humanize(filename)).replace('[content]', html_output)
      output_file.write(output_text)

      processor.reset()
      count += 1

  print colored("%s files generated" % count, "green")
