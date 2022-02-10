# from django import template
# from blog.models import *
#
# register = template.Library()
#
#
# @register.simple_tag()
# def get_comments(post_id=1, page_comments=0):
#     return Comment.objects.filter(post_id = post_id).order_by('-date_pub')[page_comments*5:page_comments*5+5]

