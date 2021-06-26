import AuthBase

class AuthBaseTest(AuthBase.AuthBase):
    def __init__(self):
        super().__init__()


test = AuthBaseTest()
a = test.getAccessToken()
# a = test.getAccessToken()
# a = test.getAccessToken()
