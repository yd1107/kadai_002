from django.template import Library

register = Library()

@register.filter
def weekday(val):
    week = ["日", "月", "火", "水", "木", "金", "土"]

    if val >= len(week):
        return ""
    else:
        return week[val]