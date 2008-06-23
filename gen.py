#!/usr/bin/python
import sys, os.path
from parser.Service import Service
from generator.Generator import Generator

def main():
    service = Service()
    filename = sys.argv[1]
    print "Converting %(filename)s" % locals()
    tree = service.parse(filename)
    # Generator("debug", tree.tree).write("out")
    
    targets = {
        'webpy': 'python-webpy',
        'html' : 'html',
    }
    
    for name, template in targets.iteritems():
        gen = Generator("CodeTemplator", tree.tree)
        gen.setOption("template", sys.path[0] + "/templates/" + template)
        gen.setOption("sourcedir", os.path.dirname(filename))
        gen.setOption("type", name)
        gen.write("out/" + name)

if __name__ == "__main__":
    main()
