#!/usr/bin/python
import sys
from parser.Service import Service
from generator.Generator import Generator

def main():
    service = Service()
    filename = sys.argv[1]
    print "Converting %(filename)s" % locals()
    tree = service.parse(filename)
    # Generator("debug", tree.tree).write("out")
    
    gen = Generator("CodeTemplator", tree.tree)
    gen.setOption("template", sys.path[0] + "/templates/python-webpy")
    gen.setOption("type", 'webpy')
    gen.write("out/webpy")

    gen = Generator("CodeTemplator", tree.tree)
    gen.setOption("template", sys.path[0] + "/templates/html")
    gen.setOption("type", 'html')
    gen.write("out/html")


if __name__ == "__main__":
    main()
