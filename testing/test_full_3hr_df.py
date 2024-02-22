import sys
from pathlib import Path

import pytest 
pytestmark = pytest.mark.skip(reason="This test is slow and not does not need to be run every time. Comment this to run.")

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

from src import tclib3

def test_df_every_tc_to_hr3():
    test_fps = round(29.97)
    start_tc = "00:00:00:00"
    tc_split = start_tc.split(":")
    while True:
        hrs = int(tc_split[0])
        mins = int(tc_split[1])
        secs = int(tc_split[2])
        frames = int(tc_split[3])

        try:
            tc_str = ":".join(tc_split)
            tc_str = tc_str[:8] + ";" + tc_str[9:]
            test_frames = tclib3.tc_to_frames(tc_str, 29.97)
            test_string = tclib3.frames_to_tc(test_frames, 29.97, True)
            reverted_frames = tclib3.tc_to_frames(test_string, 29.97)
            assert test_frames == reverted_frames
        except ValueError as e:
            if str(e).startswith("Invalid frame"):
                pass

        frames += 1
        if frames >= test_fps:
            frames = 0
            secs += 1
        if secs >= 60:
            secs = 0
            mins += 1
        if mins >= 60:
            mins = 0
            hrs += 1
        tc_split = [f"{hrs:02}", f"{mins:02}", f"{secs:02}", f"{frames:02}"]
        if hrs >= 3:
            break