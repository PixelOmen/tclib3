from .main import *
from .helpers import prezero

def test(fps: float, df: bool=False):
    test_fps = round(fps)
    start_tc = "00:00:00:00"
    tc_split = start_tc.split(":")
    while True:
        hrs = int(tc_split[0])
        mins = int(tc_split[1])
        secs = int(tc_split[2])
        frames = int(tc_split[3])

        try:
            tc_str = ":".join(tc_split)
            if df:
                tc_str = tc_str[:8] + ";" + tc_str[9:]
            test_frames = tc_to_frames(tc_str, fps)
            test_string = frames_to_tc(test_frames, fps, df)
            reverted_frames = tc_to_frames(test_string, fps)
            assert test_frames == reverted_frames, f"Start: {tc_split} - Frames: {test_frames} - TC: {test_string} - Reverted: {reverted_frames}"
        except ValueError as e:
            if not str(e).startswith("Invalid frame"):
                raise ValueError(e)

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
        tc_split = [prezero(hrs), prezero(mins), prezero(secs), prezero(frames)]
        if hrs >= 2 and mins >= 59:
            break