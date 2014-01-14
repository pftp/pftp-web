import os
import os.path
import json
import sys
from termcolor import colored

if len(sys.argv) < 2:
  print colored("need language as argument", "red")
  sys.exit(1)

language = sys.argv[1]

PARENT_CONCEPT_DIR = '%s/concepts' % language
def read_concept(concept_name):
  concept_path = PARENT_CONCEPT_DIR + '/' + concept_name
  concept_file = open(concept_path, 'r')
  res = {}
  explanation = ''
  for i, line in enumerate(concept_file.readlines()):
    if i == 0:
      res['display_name'] = line
    else:
      explanation += line
  concept_file.close()
  res['explanation'] = explanation
  return res


""" load the concepts """
concept_names = os.listdir(PARENT_CONCEPT_DIR)
all_concepts = {}
for concept_name in concept_names:
  all_concepts[concept_name] = read_concept(concept_name)

practice_concepts = open('%s/practice_concepts.json' % language, 'w')
practice_concepts.write(json.dumps(all_concepts))
practice_concepts.close()
