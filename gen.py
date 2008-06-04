#!/usr/bin/python
import sys
from parser.Service import Service
from generator.Generator import Generator

def main():
    service = Service()
    filename = sys.argv[1]
    print "Converting %(filename)s" % locals()
    tree = service.parse(filename)
    gen = Generator("debug", tree.tree)
    gen.write("out")
    gen = Generator("HtmlDoc", tree.tree)
    gen.write("out")

if __name__ == "__main__":
    main()
