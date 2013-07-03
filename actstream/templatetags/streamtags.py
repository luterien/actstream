from django import template

register = template.Library()


def get_actions_for_actor():
    """
	Returns a list of actions performed by this particular actor
    """
    pass


def get_actions_for_target():
    """
        Returns a list of actions performed on this particular target
    """
    pass


