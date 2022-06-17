from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.


@register.filter()
def censor(value):
    try:
        if not isinstance(value, str):
            raise AttributeError
        value_low = value.lower()
        value_split_low = value_low.split(' ')
        value_split = value.split(' ')
        j = 0
        for i in value_split_low:
            if i == 'просторы':
                i = 'п*******'
                value_split[j] = i
            j += 1
        return f'{" ".join(value_split)}'

    except TypeError:
        print('value - not str')


