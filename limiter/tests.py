from django.test import TestCase
from limiter import models, utils

import sure  # @UnusedImport

def timeout_func():
        return 100

# Create your tests here.
class LimitCheckerModelTests(TestCase):

    @classmethod
    def timeout_func(cls):
        return 100

    def test_timeout_func(self):
        LimitChecker = models.Tracker(code='A',
                                 error_message='B %(counter)d %(limit)d',
                                 limit=100,
                                 timeout_module='limiter.tests',
                                 timeout_func='timeout_func')

        LimitChecker.get_timeout().should.equal(100)

    def test_classmethod_timeout_func(self):
        LimitChecker = models.Tracker(code='A',
                                 error_message='B %(counter)d %(limit)d',
                                 limit=100,
                                 timeout_module='limiter.tests.LimitCheckerModelTests',
                                 timeout_func='timeout_func')

        LimitChecker.get_timeout().should.equal(100)

    def test_refresh_LimitCheckers(self):
        utils.LimitChecker.register('code', ' %(counter)d %(limit)d', 'timeout_module', 'timeout_func', 10)
        len(utils.LimitChecker.limiters).should.equal(1)

        # same code, nothing change
        utils.LimitChecker.register('code', ' %(counter)d %(limit)d', 'timeout_module', 'timeout_func', 10)
        len(utils.LimitChecker.limiters).should.equal(1)

        # different code -> LimitCheckers refresh
        utils.LimitChecker.register('code1', ' %(counter)d %(limit)d', 'timeout_module', 'timeout_func', 10)
        len(utils.LimitChecker.limiters).should.equal(2)

    def test_error_message_exception(self):
        try:
            utils.LimitChecker.register('code3', '%(limit)d', 'timeout_module', 'timeout_func', 10)
            assert False
        except Exception:
            pass

        try:
            utils.LimitChecker.register('code4', '%(counter)d', 'timeout_module', 'timeout_func', 10)
            assert False
        except Exception:
            pass

        try:
            utils.LimitChecker.register('code5', 'a', 'timeout_module', 'timeout_func', 10)
            assert False
        except Exception:
            pass
