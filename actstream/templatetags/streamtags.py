from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


def get_actions_for_actor(actor, limit=None):
    """
	Returns a list of actions performed by this particular actor
    """
    actions = Action.objects.filter(actor_content_type=ContentType.objects.get_for_model(actor.__class__),
    								actor_object_id=actor.id)

    if limit:
    	actions = actions[:limit]

    return actions


def get_actions_for_target(target, limit=None):
    """
        Returns a list of actions performed on this particular target
    """

    actions = Action.objects.filter(target_content_type=ContentType.objects.get_for_model(target.__class__),
    								target_object_id=target.id)

    if limit:
    	actions = actions[:limit]

    return actions

