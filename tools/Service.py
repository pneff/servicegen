def DumpTree(tree, indent = 0):
    if indent == 0:
        print "\n================================================\n"
        print tree.toStringTree()
        print "\n================================================\n"
    
    space = indent * "   " + " - "
    count = tree.getChildCount()
    print space, "getType : %d" % tree.getType()
    print space, "getText : %s" % tree.getText()
    print space, "Children: %d" % count
    i = 0
    while i < count:
        print space, "child   : %d" % i
        DumpTree(tree.getChild(i), indent+1)
        i+=1
