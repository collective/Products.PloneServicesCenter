## -*- coding: utf-8 -*-

# CMF doesn't allow us to put a permission on *reading* comments
# So let's monkey-patch that...

from AccessControl import getSecurityManager
from Products.CMFDefault.DiscussionTool import DiscussionNotAllowed
import types

def monkey_decorate(obj, name, decorator):
    """
    Replace obj.name (which should be a method) to a version decorated
    with decorator
    """
    old_function = getattr(obj, name)
    new_function = decorator(old_function)
    setattr(obj, name, new_function)

def is_exception(what):
    """
    Check if this is an exception
    """
    return isinstance(what, types.ClassType) and issubclass(what, Exception)

def discussion_security(onfail = DiscussionNotAllowed):
    """
    This is the main discussion_security handler

    onfail will be returned (or raise, if it's an exception) in case
    of not allowed
    """
    def decorator(method):
        """
        This will be used to decorate the old method and perform the needed
        checks
        """    
        def ensure_discussion_security(self, content):
            """
            This is the inner function, should do the check and call the old one
            """
            user = getSecurityManager().getUser()
            if not user.has_permission("Show item replies", content):
                if is_exception(onfail):
                    raise onfail
                else:
                    return onfail
            return method(self, content)
        return ensure_discussion_security
    return decorator

from Products.CMFPlone.DiscussionTool import DiscussionTool
monkey_decorate(DiscussionTool, "isDiscussionAllowedFor",
                discussion_security(False))
monkey_decorate(DiscussionTool, "getDiscussionFor",
                discussion_security(DiscussionNotAllowed))
