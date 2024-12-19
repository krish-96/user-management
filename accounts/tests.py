from django.test import TestCase
from logger_egine import logger


# Create your tests here.
class TestTest(TestCase):
    log_index = "Test Class"
    logger.info(log_index, "Testing the class")

    def test_initial(self):
        logger.info(self.log_index, "Testing the initial class")
        _name = "Test Name"
        # Todo: Will implement the actual test data
        new_name = _name

        assert _name == new_name
