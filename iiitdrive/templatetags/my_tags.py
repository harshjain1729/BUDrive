from django import template
from django.utils import timezone
from django.db import models
from ..models import Tag

register = template.Library()

@register.filter
def get_social_link(socials, name) :
	if socials.filter(name = name).exists():
		return socials.get(name = name).link
	else:
		return None

@register.filter
def get_trending_tags(trend_hours=5, trend_values=3) :
	time_threshold_t = timezone.now() - timezone.timedelta(hours=trend_hours)
	trend_tags = Tag.objects.filter(posts__created_at__gte = time_threshold_t).values('name').annotate(count = models.Count('posts')).order_by('-count')[:trend_values].values_list('name', flat = True)

	return trend_tags



@register.filter
def is_liked_by_user(post, user):
	return post.likes.filter(user=user).exists()
