import os
import markdown
from markdown.postprocessors import Postprocessor

markdown_template_file = open('templates/markdown_template.html', 'r')
markdown_template = markdown_template_file.read()

processor = markdown.Markdown()


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

    print "Generating %s from %s" % (output_path, input_path)
    html_output = processor.convert(input_text)

    output_text = markdown_template.replace('[title]', filename).replace('[content]', html_output)
    output_file.write(output_text)

    processor.reset()
