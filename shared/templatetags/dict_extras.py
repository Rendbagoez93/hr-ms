from django import template


register = template.Library()


@register.filter(name="get_item")
def get_item(dictionary: dict, key: str):
    """Return dictionary[key], or None if key is missing. Used in templates as {{ dict|get_item:key }}."""
    if not isinstance(dictionary, dict):
        return None
    return dictionary.get(key)


@register.filter(name="split")
def split_string(value: str, delimiter: str = ",") -> list[str]:
    """Split a string on a delimiter. Usage: {{ "a,b,c"|split:"," }}"""
    return value.split(delimiter)
