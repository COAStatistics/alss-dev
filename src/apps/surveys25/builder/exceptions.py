class SignError(Exception):
    def __init__(self, sign):
        super().__init__("Invalid Sign Length: {0}".format(sign))


class StringLengthError(Exception):
    def __init__(self, model_name):
        super().__init__("Invalid String Length: {0}".format(model_name))


class CreateModelError(Exception):
    def __init__(self, model_name):
        super().__init__("Create Model Error: {0}".format(model_name))


class SurveyAlreadyExists(Exception):
    def __init__(self):
        super().__init__(
            "Survey already exists, if you want to delete it while building, set `delete_exist=True`."
        )
