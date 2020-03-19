"""Soft test case implementation"""

import unittest

from softest import context, support


class TestCase(unittest.TestCase):
	"""
	Supports the soft assert style of testing, 
	where multiple assertions can fail within the same method, 
	while collecting and formatting those failures' stack traces
	for reporting by a final assert_all call.
	
	Such stack traces are enhanced
	to include the call hierarchy
	from within the test class.
	
	@see: soft_assert
	@see: assert_all
	@usage:	
		import softest
	
		class ExampleTest(softest.TestCase):
			def test_example(self):
				self.soft_assert(self.assertEqual, 'Worf', 'wharf', 'Klingon is not ship receptacle')
				self.soft_assert(self.assertTrue, True)
				self.soft_assert(self.assertTrue, False)
				
				self.soft_assert_raises(
		
				self.assert_all()
		
		
		if __name__ == '__main__':
			softest.main()
	"""

	def __init__(self, methodName:str = 'runTest'):
		super().__init__(methodName)
		self.__ASSERTION_LOGGER = support.AssertionLogger()

	def __get_module_and_class_names(self) -> str:
		if self.__class__.__module__ == "__main__":
			return '({})'.format(self.__class__.__qualname__)

		return '({}.{})'.format(self.__class__.__module__, self.__class__.__qualname__)

	def __str__(self):
		return '"{}" {}'.format(self._testMethodName, self.__get_module_and_class_names())

	def soft_assert(self, assert_method, *arguments, **keywords):
		"""
		Asserts the specified comparison 
		and stores any raised AssertionErrors stack traces 
		for later reporting.
		
		@param assert_method: the method definition for the desired assert call, ex: self.assert 
		@see: assert_all
		"""
		try:
			assert_method(*arguments, **keywords)
		except AssertionError as ae:
			self.__ASSERTION_LOGGER.process_and_store(ae)

	def soft_assert_raises(self, expected_exception, *arguments, **keywords):
		"""
		If the indicated code does not throw expected_exception,
		stores the raised AssertionError stack traces
		for later reporting.
		 
		@see: unittest.case.assertRaises
		"""
		assertion_context = context.SoftAssertRaisesContext(expected_exception, self, self.__ASSERTION_LOGGER)
		try:
			return assertion_context.handle('assertRaises', arguments, keywords)
		finally:
			# manually break a reference cycle (per unittest)
			assertion_context = None

	def soft_assert_raises_regex(self, expected_exception, expected_regex, *arguments, **keywords):
		"""
		If the indicated code does not raise expected_exception,
		or the raised exception does not match expected regex, 
		stores the raised AssertionError stack traces
		for later reporting.
		
		@see: unittest.case.assertRaisesRegex
		"""
		assertion_context = context.SoftAssertRaisesContext(expected_exception, self,
																											self.__ASSERTION_LOGGER, expected_regex)
		return assertion_context.handle('assertRaisesRegex', arguments, keywords)

	def assert_all(self, method_name:str = None):
		"""
		Prints all collected assertion exceptions,
		then clears the collection,
		and finally fails the method
		if any tests failed
		before the last assert_all call.
		
		@param: method_name: overrides the auto-detection of the caller's displayed function name when specified
		@see: self.fail 
		"""
		if not method_name:
			frames, target_index = support.get_stack_and_first_test_class_frame_index()
			method_name = frames[target_index].name
			full_signature = '"{}" {}'.format(method_name, self.__get_module_and_class_names())
		else:
			full_signature = str(self)

		asserted_exceptions = self.__ASSERTION_LOGGER.get_asserted_exceptions()
		if asserted_exceptions:
			failure_output = ['++++ soft assert failure details follow below ++++\n' +
													'\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n']
			lesser_separator = 	'\n+----------------------+----------------------+----------------------+\n'
			count = len(asserted_exceptions)

			failure_output.append('The following ')
			failure_output.append(str(count) + ' failures were' if count > 1 else 'failure was')
			failure_output.append(' found in {}:'.format(full_signature))
			failure_output.append(lesser_separator)

			for index, failure in enumerate(asserted_exceptions):
				if count > 1:
					if index > 0:
						failure_output.append(lesser_separator)

					failure_output.append(' Failure {} ("{}" method)'.format(index + 1, method_name))
					failure_output.append(lesser_separator)

				failure_output.append(''.join(failure))
				failure_output.append('\n-+ [{}/{}] +-'.format(index + 1, count))

				if index + 1 < count:
					failure_output.append('\n')

			self.__ASSERTION_LOGGER.clear_asserted_exceptions()
			self.fail(''.join(failure_output))
