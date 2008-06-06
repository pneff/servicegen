import web

def best_of(types):
    """
    Returns the best output type of `types' to fullfil the current request.
    """
    
    # Path takes priority
    for type in types:
        if web.ctx.path.endswith('.' + type):
            return type
    
    # Try accept header
    accept = [
        entry.split(';')[0].split('/')[-1] for entry in
            web.ctx.env.get('HTTP_ACCEPT').split(',')]
    for type in accept:
        if type in types:
            return type
    
    # Return first entry (to be changed)
    return types[0]

def write(out_type, value_type, value):
    if out_type == 'xml':
        if value_type == 'LITERAL_XML':
            web.output(value)
        else:
            web.output(escape(value))
