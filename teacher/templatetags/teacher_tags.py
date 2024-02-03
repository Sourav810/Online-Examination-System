from exam import models as QMODEL 
from django import template
register=template.Library()

@register.simple_tag(name="counter")
def counter(course_id):
    no=QMODEL.Result.objects.filter(exam_id=course_id).count()
    return no