class SignError(Exception):
    def __init__(self, **kwargs):
        self.sign = kwargs.get("sign")
        Exception.__init__(self, "Invalid Sign Length: {0}".format(self.sign))


class StringLengthError(Exception):
    def __init__(self, **kwargs):
        self.model_name = kwargs.get("model_name")
        Exception.__init__(
            self, "Invalid String Length: {0}".format(self.model_name)
        )


class CreateModelError(Exception):
    def __init__(self, **kwargs):
        self.model_name = kwargs.get("model_name")
        Exception.__init__(self, "Create Model Error: {0}".format(self.model_name))


class SurveyAlreadyExists(Exception):
    def __init__(self):
        Exception.__init__(self, """
            Survey already exists, if you want to delete it while building, set `delete_exist=True`.
        """)
