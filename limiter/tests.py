from django.test import TestCase
from limiter import models, utils

import sure  # @UnusedImport

def timeout_func():
        return 100

# Create your tests here.
class LimiterModelTests(TestCase):

    @classmethod
    def timeout_func(cls):
        return 100

    def test_timeout_func(self):
        limiter = models.Limiter(code='A',
                                 error_message='B',
                                 limit=100,
                                 timeout_module='limiter.tests',
                                 timeout_func='timeout_func')

        limiter.get_timeout().should.equal(100)

    def test_classmethod_timeout_func(self):
        limiter = models.Limiter(code='A',
                                 error_message='B',
                                 limit=100,
                                 timeout_module='limiter.tests.LimiterModelTests',
                                 timeout_func='timeout_func')

        limiter.get_timeout().should.equal(100)

    def test_refresh_limiters(self):
        utils.Limiter.register('code', 'error_message', 'timeout_module', 'timeout_func', 10)
        len(utils.Limiter.limiters).should.equal(1)

        # same code, nothing change
        utils.Limiter.register('code', 'error_message', 'timeout_module', 'timeout_func', 10)
        len(utils.Limiter.limiters).should.equal(1)

        # different code -> limiters refresh
        utils.Limiter.register('code1', 'error_message', 'timeout_module', 'timeout_func', 10)
        len(utils.Limiter.limiters).should.equal(2)
