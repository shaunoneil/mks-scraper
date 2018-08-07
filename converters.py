#!/usr/bin/env python

import sys
import os

def keepConverter(converter):
    # disregard if there are no outputs; many parts that consume resources without outputting any show up otherwise.
    if len(converter['outputs'])>0:
        outputs=",".join(converter['outputs'])
        inputs=",".join(converter['inputs'])

        # Ugly attempt at CSV. Don't put spaces after the commas else Excel gets over-excited.
        print("\"{}\",\"{}\",\"{}\",\"{}\"".format(outputs, inputs, converter['name'], converter['part']))

def processcfg(filepath):
    # open a cfg file for reading
    fp = open(filepath,'r')

    line = fp.readline()    # read line-by-line
    line_previous=line      # I keep track of the previous line so I know what section a { matches
    parser = ['root']       # list used as a stack to keep track of which section I'm in
    depth=0                 # how deep in the stack am I. I could probably just len(parser)?
    part_title=""           # I don't always find one, so this stops it exploding.
    line_number=1           # only used for debugging

    converter={}            # Somewhere to keep what I find
    converter_found=False   # flag whether I should be keeping data I find

    while line:
        stripped = line.strip()

        # split a=b lines into 'a' and 'b'
        tokens = stripped.split(" = ")
        if len(tokens)==2:

            # part title
            if parser[depth]=="PART" and tokens[0]=="title":
                part_title=tokens[1]

            # If we find a ConverterName, start a new new convter dict
            if parser[depth]=="MODULE" and tokens[0]=="ConverterName":
                converter['part']=part_title
                converter['name']=tokens[1]
                converter['depth']=depth  # keep track of the current depth in the stack, so we know when we're leaving it
                converter['inputs']=[]
                converter['outputs']=[]
                converter_found=True

            # If we find ResourceName inside a Converter, keep it
            if converter_found and parser[depth]=="INPUT_RESOURCE" and tokens[0]=="ResourceName":
                converter['inputs'].append(tokens[1])
            if converter_found and parser[depth]=="OUTPUT_RESOURCE" and tokens[0]=="ResourceName":
                converter['outputs'].append(tokens[1])

        # Entering a new block
        if stripped == "{":
            # If the line is {, we're entering a new block, and its name is on the previous line
            parser.append(line_previous.strip())
            depth += 1
        elif stripped[-1:] == "{": # elif is important because this would also match the previous condition.
            # If the line ends with {, we're entering a new block, but I need to split the current line to find the nameself.
            tokens = stripped.split()
            parser.append(tokens[0])
            depth += 1

        # Leaving a block block (decrease indentation)
        if line.strip() == "}":
            # If we're finishing a converter, keep it
            if converter_found and converter['depth']==depth:
                del converter['depth']
                keepConverter(converter)
                converter_found=False
                converter={'depth': 0}
            parser = parser[:-1]
            depth -= 1

#        print("\t{}\t{}\t{}\t{}".format(line_number, depth, parser[depth], line.strip()))

        # step through the file
        line_previous=line
        line_number += 1
        line = fp.readline()



for subdir, dirs, files in os.walk('GameData'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".cfg"):
            processcfg(filepath)
