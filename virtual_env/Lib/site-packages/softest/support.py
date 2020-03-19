import os
import sys
import traceback
from typing import Tuple

UNIT_TEST_CASE_MODULE_FILE_PATH = 'unittest' + os.sep + 'case.py'


def get_stack_and_first_test_class_frame_index() -> Tuple[list, int]:
	"""
	Extracts the stack,
	then searches it 
	for the first frame of the test class.
	
	@return: [0] the extracted stack
		[1] the frame index
	"""
	frames = traceback.extract_stack()
	target_index = -1;
	frame_file_path = ''

	while(not frame_file_path.endswith(UNIT_TEST_CASE_MODULE_FILE_PATH)):
		target_index -= 1;
		frame_file_path = frames[target_index].filename;

	return frames, target_index + 1


class AssertionLogger:
	"""
	Processes and collects AssertionErrors thrown by soft test method calls.
	Serves as the middle ground between softest.TestCase and the context module.
	"""
	__asserted_exceptions = []

	def process_and_store(self, exception:AssertionError):
		"""
		Collects all relevant code traces
		to combine for extra details in the log.
		"""
		formatted_frames = traceback.format_exception(AssertionError, exception, sys.exc_info()[2])
		frames, target_index = get_stack_and_first_test_class_frame_index()

		# skipping the deeper softest calls to keep focused on the test class
		test_class_frames = frames[target_index:-3]
		test_class_frames = traceback.format_list(test_class_frames)

		for frame in test_class_frames:
			formatted_frames.insert(1, frame)

		self.__asserted_exceptions.append(formatted_frames)

	def get_asserted_exceptions(self) -> list:
		"""
		Returns a shallow copy of the collected AssertionErrors.
		"""
		return self.__asserted_exceptions.copy()

	def clear_asserted_exceptions(self):
		self.__asserted_exceptions.clear()
