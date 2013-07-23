import os
import markdown

processor = markdown.Markdown()

for root, subFolders, files in os.walk('markdown'):
  for filename in files:
    input_path = os.path.join(root, filename)
    output_dir = root.replace('markdown', 'templates/gen', 1)
    output_path = os.path.splitext(os.path.join(output_dir, filename))[0] + '.html'
    input_file = open(input_path, 'r')

    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    output_file = open(output_path, 'w')

    print "Generating %s from %s" % (output_path, input_path)
    processor.convertFile(input=input_file, output=output_file)

    processor.reset()
