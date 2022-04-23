from padam.parts.cabinet import Cabinet


cabinet = Cabinet()

obj = cabinet.get_object()

# Show
if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass
if 'show' not in globals():
    def show(*args, **kwargs):
        pass
show_object(obj)
show(obj)
