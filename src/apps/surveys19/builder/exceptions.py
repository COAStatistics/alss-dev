class SignError(Exception):
    def __init__(self, **kwargs):
        self.sign = kwargs.get("sign")
        Exception.__init__(self, "{0} Sign Length Is Not Valid {0}".format(self.sign))


class StringLengthError(Exception):
    def __init__(self, **kwargs):
        self.String = kwargs.get("String")
        Exception.__init__(
            self, "{0} String Length Is Not Valid {0}".format(self.String)
        )


class CreateModelError(Exception):
    def __init__(self, **kwargs):
        self.Name = kwargs.get("Name")
        Exception.__init__(self, "{0} Create Model Is Error {0}".format(self.Name))
