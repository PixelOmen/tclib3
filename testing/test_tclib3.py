import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

import testdata
import src as tclib3
from src import helpers


class TestLib(unittest.TestCase):
    def test_adjust_df_frames(self):
        for _, frame in testdata.RANDOM_DF_TCS_2997:
            adjusted_frame = helpers.adjust_df_frames(frame, 29.97, True)
            original_frame = helpers.adjust_df_frames(adjusted_frame, 29.97, False)
            self.assertEqual(frame, original_frame)

    def test_frames_to_tc(self):
        for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
            converted_frame = tclib3.frames_to_tc(frame, 29.97, True)
            self.assertEqual(converted_frame, tc_str)

        for tc_str, frame in testdata.RANDOM_TCS_2997:
            converted_frame = tclib3.frames_to_tc(frame, 29.97, False)
            self.assertEqual(converted_frame, tc_str)

        for tc_str, frame in testdata.RANDOM_TCS_2398:
            converted_frame = tclib3.frames_to_tc(frame, 23.976, False)
            self.assertEqual(converted_frame, tc_str)

    def test_frames_to_tc_to_frames(self):
        for _, frame in testdata.RANDOM_DF_TCS_2997:
            tc = tclib3.frames_to_tc(frame, 29.97, True)
            converted_frames = tclib3.tc_to_frames(tc, 29.97, force_df=True)
            self.assertEqual(converted_frames, frame)

        for _, frame in testdata.RANDOM_TCS_2997:
            tc = tclib3.frames_to_tc(frame, 29.97, False)
            converted_frames = tclib3.tc_to_frames(tc, 29.97)
            self.assertEqual(converted_frames, frame)

        for _, frame in testdata.RANDOM_TCS_2398:
            tc = tclib3.frames_to_tc(frame, 23.976, False)
            converted_frames = tclib3.tc_to_frames(tc, 23.976)
            self.assertEqual(converted_frames, frame)

    def test_tc_to_frames(self):
        for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
            converted_frame = tclib3.tc_to_frames(tc_str, 29.97, force_df=True)
            self.assertEqual(converted_frame, frame)

        for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
            converted_frame = tclib3.tc_to_frames(tc_str, 29.97)
            self.assertEqual(converted_frame, frame)

        for tc_str, frame in testdata.RANDOM_TCS_2997:
            converted_frame = tclib3.tc_to_frames(tc_str, 29.97)
            self.assertEqual(converted_frame, frame)

        for tc_str, frame in testdata.RANDOM_TCS_2398:
            converted_frame = tclib3.tc_to_frames(tc_str, 23.976)
            self.assertEqual(converted_frame, frame)

    def test_tc_to_frames_to_tc(self):
        for tc_str, _ in testdata.RANDOM_DF_TCS_2997:
            frames = tclib3.tc_to_frames(tc_str, 29.97, force_df=True)
            converted_tc = tclib3.frames_to_tc(frames, 29.97, True)
            self.assertEqual(converted_tc, tc_str)

        for tc_str, _ in testdata.RANDOM_DF_TCS_2997:
            frames = tclib3.tc_to_frames(tc_str, 29.97)
            converted_tc = tclib3.frames_to_tc(frames, 29.97, False)
            self.assertNotEqual(converted_tc, tc_str)

        for tc_str, _ in testdata.RANDOM_TCS_2997:
            frames = tclib3.tc_to_frames(tc_str, 29.97)
            converted_tc = tclib3.frames_to_tc(frames, 29.97, False)
            self.assertEqual(converted_tc, tc_str)

        for tc_str, _ in testdata.RANDOM_TCS_2398:
            frames = tclib3.tc_to_frames(tc_str, 23.976)
            converted_tc = tclib3.frames_to_tc(frames, 23.976, False)
            self.assertEqual(converted_tc, tc_str)

    def test_frames_to_ms(self):
        for frames, ms in testdata.RANDOM_MS_2997:
            converted_ms = tclib3.frames_to_ms(frames, 29.97)
            self.assertEqual(converted_ms, ms)

        for frames, ms in testdata.RANDOM_MS_2398:
            converted_ms = tclib3.frames_to_ms(frames, 23.976)
            self.assertEqual(converted_ms, ms)

    def test_ms_to_frames(self):
        for frames, ms in testdata.RANDOM_MS_2997:
            converted_frames = tclib3.ms_to_frames(ms, 29.97)
            self.assertEqual(converted_frames, frames)

        for frames, ms in testdata.RANDOM_MS_2398:
            converted_frames = tclib3.ms_to_frames(ms, 23.976)
            self.assertEqual(converted_frames, frames)

    def test_frames_to_ms_to_frames(self):
        for frames, _ in testdata.RANDOM_MS_2997:
            ms = tclib3.frames_to_ms(frames, 29.97)
            converted_frames = tclib3.ms_to_frames(ms, 29.97)
            self.assertEqual(converted_frames, frames)

        for frames, _ in testdata.RANDOM_MS_2398:
            ms = tclib3.frames_to_ms(frames, 23.976)
            converted_frames = tclib3.ms_to_frames(ms, 23.976)
            self.assertEqual(converted_frames, frames)

    def test_ms_to_frames_to_ms(self):
        for _, ms in testdata.RANDOM_MS_2997:
            frames = tclib3.ms_to_frames(ms, 29.97)
            converted_ms = tclib3.frames_to_ms(frames, 29.97)
            self.assertEqual(converted_ms, ms)

        for _, ms in testdata.RANDOM_MS_2398:
            frames = tclib3.ms_to_frames(ms, 23.976)
            converted_ms = tclib3.frames_to_ms(frames, 23.976)
            self.assertEqual(converted_ms, ms)

if __name__ == "__main__":
    unittest.main()