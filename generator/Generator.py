import sys
from generator.Process import Process
from generator.webpy import webpy
from generator.debug import debug

class Generator:
    def __init__(self, template, tree):
        self.template = template
        process = Process(tree)
        module = sys.modules[Generator.__module__]
        self.generator = getattr(module, template)(process)
    
    def write(self, outputdir):
        self.generator.write(outputdir)
