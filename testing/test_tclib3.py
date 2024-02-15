import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

import testdata
import src as tclib3


class TestLib(unittest.TestCase):
    def test_frames_to_tc(self):
        for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
            converted_frame = tclib3.frames_to_tc(frame, 29.97, True, True)
            self.assertEqual(converted_frame, tc_str)

        for tc_str, frame in testdata.RANDOM_TCS_2997:
            converted_frame = tclib3.frames_to_tc(frame, 29.97, False, False)
            self.assertEqual(converted_frame, tc_str)

        for tc_str, frame in testdata.RANDOM_TCS_2398:
            converted_frame = tclib3.frames_to_tc(frame, 23.976, False, False)
            self.assertEqual(converted_frame, tc_str)

    def test_tc_to_frames(self):
        for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
            converted_frame = tclib3.tc_to_frames(tc_str, 29.97)
            self.assertEqual(converted_frame, frame)

        for tc_str, frame in testdata.RANDOM_TCS_2997:
            converted_frame = tclib3.tc_to_frames(tc_str, 29.97)
            self.assertEqual(converted_frame, frame)

        for tc_str, frame in testdata.RANDOM_TCS_2398:
            converted_frame = tclib3.tc_to_frames(tc_str, 23.976)
            self.assertEqual(converted_frame, frame)

if __name__ == "__main__":
    unittest.main()