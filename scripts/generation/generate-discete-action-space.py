import json
from argparse import ArgumentParser, Namespace

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="The path of the input file to be converted", metavar="file_path")
parser.add_argument("-o", "--output", dest="output",
                    help="The output path destination of the new file",  metavar="file_path")

args = vars(parser.parse_args())

# Opening JSON file
f = open(args['input'])

# # returns JSON object as
# # a dictionary
data = json.load(f)

# # Iterating through the json
# # list
# for i in data['emp_details']:
#     print(i)

# # Closing file
# f.close()
