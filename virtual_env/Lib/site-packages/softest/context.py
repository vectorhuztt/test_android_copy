"""
Context manager to support softest.case.TestCase.
"""

import unittest
import traceback


class SoftAssertRaisesContext(unittest.case._AssertRaisesContext):
	"""
	As derived from unittest.case._AssertRaisesContext,
	and equipped with a passed instance of AssertionLogger.
	"""

	def __init__(self, expected, test_case, assertion_logger,
							expected_regex = None):
		super().__init__(expected, test_case, expected_regex)
		self.__ASSERTION_LOGGER = assertion_logger

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, exception_traceback):
		"""
		Exit the runtime context related to this object. 
		The parameters describe the exception 
		that caused the context to be exited.
		If the context was exited without an exception,
		all three arguments will be None.

		If an exception is supplied, 
		and the method wishes to suppress the exception 
		(i.e., prevent it from being propagated), 
		it should return a true value. 
		Otherwise, the exception will be processed normally 
		upon exit from this method.
		"""
		if exception_type is not None:
			traceback.clear_frames(exception_traceback)
		else:
			try:
				exception_name = self.expected.__name__
			except AttributeError:
				exception_name = str(self.expected)

			try:
				if self.obj_name:
					self._raiseFailure("{} did not raise {}".format(self.obj_name,
																												exception_name))
				else:
					self._raiseFailure(
						"Context actions did not raise {}".format(exception_name))

			except AssertionError as ae:
				self.__ASSERTION_LOGGER.process_and_store(ae)
				return True

		if not issubclass(exception_type, self.expected):
			# let unexpected exceptions pass through
			return False

		# store exception, without traceback, for later retrieval
		self.exception = exception_value.with_traceback(None)

		if self.expected_regex is None:
			return True

		if not self.expected_regex.search(str(exception_value)):
			try:
				self._raiseFailure(
					'"{}" does not match the supplied regular expression "{}"'.format(
						self.expected_regex.pattern, str(exception_value)))
			except AssertionError as ae:
				self.__ASSERTION_LOGGER.process_and_store(ae)
				return True

		return True
