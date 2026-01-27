from django.template import Library

register = Library()

@register.simple_tag

def show_runtime(time):

    return f'{time.hour}h {time.minute}m'