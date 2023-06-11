from django import template

register = template.Library()

@register.filter(name='addclassandholder')
def addclassandholder(value, args):

    arg_list = [arg.strip() for arg in args.split(',')]

    newclass = arg_list[0]
    
    def placecalc(placer):
        if len(placer) == 2:
            placeholder = placer[1]
            return(placeholder)
        else:
            return("")
        
    newplaceholder = placecalc(arg_list)

    return value.as_widget(attrs={'class': newclass, 'placeholder': newplaceholder})