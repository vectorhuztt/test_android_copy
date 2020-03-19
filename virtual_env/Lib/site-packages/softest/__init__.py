"""
Supports the soft assert style of testing, 
where multiple assertions can fail within the same method, 
while collecting and formatting those failures' stack traces
for reporting by a final assert_all call.

Created on Jun 19, 2018
@author: Nick Umble

@usage:	
	import softest

	class ExampleTest(softest.TestCase):

	def test_example(self):
		self.soft_assert(self.assertEqual, 'Worf', 'wharf', 'Klingon is not ship receptacle')
		self.soft_assert(self.assertTrue, True)
		self.soft_assert(self.assertTrue, False)

		self.assert_all()

	def test_example_with_only_one_failure(self):
		self.soft_assert(self.assertTrue, False)
		self.assert_all()

	# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
	class SomeException(Exception):

		def __init__(self, reason:str):
			super().__init__(self)
			self.reason = reason

		def __str__(self):
			return self.reason
			
	# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

	def test_assert_raises(self):
		with self.soft_assert_raises(self.SomeException) as assertion_context:
			print('=)')

		print(assertion_context)


		with self.soft_assert_raises_regex(self.SomeException, 'reason') as another_context:
			raise self.SomeException('reazon')

		print(another_context)
		

		self.assert_all()


	if __name__ == '__main__':
		softest.main()
			

@etymology:
	'softest' stems from 'soft-test',
	joined because twin consonants split like this are terrible to the tongue,
	and especially because "softest" sounds pleasant,
	like warm bath towels on one's face =)
"""

import unittest
from .case import TestCase


def main():
	unittest.main()
