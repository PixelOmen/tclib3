import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

import testdata
from src import tclib3


def test_adjust_df_frames():
    for _, frame in testdata.RANDOM_DF_TCS_2997:
        adjusted_frame = tclib3.helpers.adjust_df_frames(frame, 29.97, True)
        original_frame = tclib3.helpers.adjust_df_frames(adjusted_frame, 29.97, False)
        assert frame == original_frame

def test_frames_to_tc():
    for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
        converted_frame = tclib3.frames_to_tc(frame, 29.97, True)
        assert converted_frame == tc_str

    for tc_str, frame in testdata.RANDOM_TCS_2997:
        converted_frame = tclib3.frames_to_tc(frame, 29.97, False)
        assert converted_frame == tc_str

    for tc_str, frame in testdata.RANDOM_TCS_2398:
        converted_frame = tclib3.frames_to_tc(frame, 23.976, False)
        assert converted_frame == tc_str

def test_frames_to_tc_to_frames():
    for _, frame in testdata.RANDOM_DF_TCS_2997:
        tc = tclib3.frames_to_tc(frame, 29.97, True)
        converted_frames = tclib3.tc_to_frames(tc, 29.97, force_df=True)
        assert converted_frames == frame

    for _, frame in testdata.RANDOM_TCS_2997:
        tc = tclib3.frames_to_tc(frame, 29.97, False)
        converted_frames = tclib3.tc_to_frames(tc, 29.97)
        assert converted_frames == frame

    for _, frame in testdata.RANDOM_TCS_2398:
        tc = tclib3.frames_to_tc(frame, 23.976, False)
        converted_frames = tclib3.tc_to_frames(tc, 23.976)
        assert converted_frames == frame

    for _, frame in testdata.RANDOM_TCS_2398:
        tc = tclib3.frames_to_tc(frame, 24, False)
        converted_frames = tclib3.tc_to_frames(tc, 24)
        assert converted_frames == frame

def test_tc_to_frames():
    for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
        converted_frame = tclib3.tc_to_frames(tc_str, 29.97, force_df=True)
        assert converted_frame == frame

    for tc_str, frame in testdata.RANDOM_DF_TCS_2997:
        converted_frame = tclib3.tc_to_frames(tc_str, 29.97)
        assert converted_frame == frame

    for tc_str, frame in testdata.RANDOM_TCS_2997:
        converted_frame = tclib3.tc_to_frames(tc_str, 29.97)
        assert converted_frame == frame

    for tc_str, frame in testdata.RANDOM_TCS_2398:
        converted_frame = tclib3.tc_to_frames(tc_str, 23.976)
        assert converted_frame == frame

def test_tc_to_frames_to_tc():
    for tc_str, _ in testdata.RANDOM_DF_TCS_2997:
        frames = tclib3.tc_to_frames(tc_str, 29.97, force_df=True)
        converted_tc = tclib3.frames_to_tc(frames, 29.97, True)
        assert converted_tc == tc_str

    for tc_str, _ in testdata.RANDOM_DF_TCS_2997:
        frames = tclib3.tc_to_frames(tc_str, 29.97)
        converted_tc = tclib3.frames_to_tc(frames, 29.97, False)
        assert not (converted_tc == tc_str)

    for tc_str, _ in testdata.RANDOM_TCS_2997:
        frames = tclib3.tc_to_frames(tc_str, 29.97)
        converted_tc = tclib3.frames_to_tc(frames, 29.97, False)
        assert converted_tc == tc_str

    for tc_str, _ in testdata.RANDOM_TCS_2398:
        frames = tclib3.tc_to_frames(tc_str, 23.976)
        converted_tc = tclib3.frames_to_tc(frames, 23.976, False)
        assert converted_tc == tc_str

def test_frames_to_ms():
    for frames, ms in testdata.RANDOM_MS_2997:
        converted_ms = tclib3.frames_to_ms(frames, 29.97)
        assert converted_ms == ms

    for frames, ms in testdata.RANDOM_MS_2398:
        converted_ms = tclib3.frames_to_ms(frames, 23.976)
        assert converted_ms == ms

    for frames, ms in testdata.RANDOM_MS_24:
        converted_ms = tclib3.frames_to_ms(frames, 24)
        assert converted_ms == ms

def test_ms_to_frames():
    for frames, ms in testdata.RANDOM_MS_2997:
        converted_frames = tclib3.ms_to_frames(ms, 29.97)
        assert converted_frames == frames

    for frames, ms in testdata.RANDOM_MS_2398:
        converted_frames = tclib3.ms_to_frames(ms, 23.976)
        assert converted_frames == frames

    for frames, ms in testdata.RANDOM_MS_24:
        converted_frames = tclib3.ms_to_frames(ms, 24)
        assert converted_frames == frames

def test_frames_to_ms_to_frames():
    for frames, _ in testdata.RANDOM_MS_2997:
        ms = tclib3.frames_to_ms(frames, 29.97)
        converted_frames = tclib3.ms_to_frames(ms, 29.97)
        assert converted_frames == frames

    for frames, _ in testdata.RANDOM_MS_2398:
        ms = tclib3.frames_to_ms(frames, 23.976)
        converted_frames = tclib3.ms_to_frames(ms, 23.976)
        assert converted_frames == frames

    for frames, _ in testdata.RANDOM_MS_24:
        ms = tclib3.frames_to_ms(frames, 24)
        converted_frames = tclib3.ms_to_frames(ms, 24)
        assert converted_frames == frames

def test_ms_to_frames_to_ms():
    for _, ms in testdata.RANDOM_MS_2997:
        frames = tclib3.ms_to_frames(ms, 29.97)
        converted_ms = tclib3.frames_to_ms(frames, 29.97)
        assert converted_ms == ms

    for _, ms in testdata.RANDOM_MS_2398:
        frames = tclib3.ms_to_frames(ms, 23.976)
        converted_ms = tclib3.frames_to_ms(frames, 23.976)
        assert converted_ms == ms

    for _, ms in testdata.RANDOM_MS_24:
        frames = tclib3.ms_to_frames(ms, 24)
        converted_ms = tclib3.frames_to_ms(frames, 24)
        assert converted_ms == ms

def test_duration():
    for start, end, df_dur, ndf_dur in testdata.RANDOM_DUR_2997:
        assert tclib3.duration(start, end, 29.97, True) == df_dur
        assert tclib3.duration(start, end, 29.97, False) == ndf_dur

    for start, end, dur in testdata.RANDOM_DUR_2398:
        assert tclib3.duration(start, end, 23.976) == dur

    with pytest.raises(ValueError):
        tclib3.duration("00:00:00:02", "00:00:00:01", 23.976)