from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode


class ActionType(models.Model):
    """
        Examples of usage : 

        -> add <this> to <that>
        -> invite <this> to <that>
        -> remove <this> from <that>
        -> assign <this> to <that>
        -> comment <this> on <that>
    """
    name = models.CharField(_('Action name/key'), max_length=30, unique=True)
    verb = models.CharField(_('Verb'), max_length=40, null=True, blank=True)
    
    format = models.CharField(_('Format'), max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name
    
    def validate_format(self):
        pass
    
    def get_format(self):
        return self.format
    
    def format_dict(self):
        return {'verb': self.verb}


class ActionManager(models.Manager):

    def new_action(self, actor, action_object, action_key, target_object=None):
        """
            Create a new action
        """

        action = self.model(
            actor_content_type=ContentType.objects.get_for_model(
                action_object.__class__),
            actor_object_id=smart_unicode(action_object.id),
            action_content_type=ContentType.objects.get_for_model(
                action_object.__class__),
            action_object_id=smart_unicode(action_object.id),
            action_type=action_types.get())

        if target_object:
            action.target_content_type = ContentType.objects.get_for_model(
                target_object.__class__)
            action.target_object_id = smart_unicode(target_object.id)

        action.save()
        
        return action


class BaseAction(models.Model):
    """

        User action examples :
    
        -> <ahmet> has <deleted> <discussionTitle>
        -> <ercan> has <commented> <on> <taskTitle>
        -> <erhan> has <created> <projectTitle>
        -> <murat> has <assigned> <userName> to <taskName>
        -> <ayhan> has <changed> <taskTitle>

    """
    action_time = models.DateTimeField(_("action time"), auto_now=True)

    action_type = models.ForeignKey(ActionType, verbose_name=_('action type'))

    # Actor
    actor_content_type = models.ForeignKey(
        ContentType, related_name="actor_object", blank=True, null=True)

    actor_object_id = models.TextField(_('object id'), blank=True, null=True)

    actor_content_object = generic.GenericForeignKey(
        'actor_content_type', 'actor_object_id')

    # Action
    action_content_type = models.ForeignKey(
        ContentType, related_name="action_object", blank=True, null=True)

    action_object_id = models.TextField(_('object id'), blank=True, null=True)

    action_content_object = generic.GenericForeignKey(
        'action_content_type', 'action_object_id')

    # Target 
    target_content_type = models.ForeignKey(
        ContentType, related_name="target_object", blank=True, null=True)

    target_object_id = models.TextField(_('object id'), blank=True, null=True)

    target_content_object = generic.GenericForeignKey('target_content_type',
                                                      'target_object_id')

    objects = ActionManager()

    
    class Meta:
        verbose_name = _("User Action")
        verbose_name_plural = _("User Actions")
        abstract = True

    def __unicode__(self):
        return self.formatted
    
    @property
    def default_format(self):
        if self.target_content_object:
            return "%(actor)s has %(verb)s %(action_object)s on %(target_content_object)s"
        else:
            return "%(actor)s has %(verb)s %(action_object)s"
    
    @property
    def format(self):
        if self.action_type.format:
            return self.action_type.format
        else:
            return self.default_format
    
    @property
    def formatted(self):
        
        formatted = self.format % self.format_dict
        
        return formatted

    @property
    def format_dict(self):
        keys = self.action_type.format_dict()
        
        dx = {
              'action_object': self.action_content_object,
              'target_object': self.target_content_object,
              'user': self.user,
              'date': self.action_time
        }
        
        keys.update(dx)
        
        return keys


class Action(BaseAction):
    pass


class FollowManager(models.Manager):

    def create_new(self, follower, followed):
        """
            New follow object
        """

        follow, created = self.model.objects.get_or_create(
            follower_content_type=ContentType.objects.get_for_model(
                follower.__class__),
            follower_object_id=follower.id,

            followed_content_type=ContentType.objects.get_for_model(
                followed.__class__),
            followed_object_id=followed.id)

        follow.save()

        return follow


    def active(self):
        """
            Filter active follows
        """
        return self.filter(is_active=True)


class Follow(models.Model):
    """
        
        Allows an object to follow another object

    """
    follower_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    follower_object_id = models.TextField(_('object id'), blank=True, null=True)
    follower_content_object = generic.GenericForeignKey('follower_content_object',
                                                        'follower_object_id')

    followed_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    followed_object_id = models.TextField(_('object id'), blank=True, null=True)
    followed_content_object = generic.GenericForeignKey('followed_content_type',
                                                        'followed_object_id')

    is_active = models.BooleanField(default=True)

    objects = FollowManager()

    def __unicode__(self):
        return u"%s following %s" % (self.follower_content_object,
                                     self.followed_content_object)

