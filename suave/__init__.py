from django.template import Context, loader

template_cache = {}
def render_cached(template_name, dictionary=None):
    global template_cache
        
    t = template_cache.get(template_name, None)
    if not t or settings.DEBUG:
        template_cache[template_name] = t = loader.get_template(template_name)

    dictionary = dictionary or {}    
    context_instance = Context(dictionary)
    return t.render(context_instance)