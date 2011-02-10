from Products.validation.interfaces import ivalidator

class IndustriesValidator:

    __implements__=(ivalidator,)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if len([ v for v in value if v ]) > 2:
            return 'Please select at most two industries'
        return True

