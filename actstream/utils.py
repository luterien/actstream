from . models import Follow, Action


def follow(follower, followed):
    """ start following an object """
	Follow.objects.create_new(follower=follower, followed=followed)


def unfollow(follower, followed):
	""" stop following an object """
	Follow.objects.filter(follower=follower, followed=followed).update(is_active=False)


def action(actor, action_type, action, target=None):
	""" save the action """
	Action.objects.create_new(actor, action_type, action, target)

