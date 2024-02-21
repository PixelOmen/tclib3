from . import helpers

def frames_to_tc(inputframes: int, fps: float=24, dropframe: bool=False) -> str:
    """
    Convert frames to timecode.
    If `dropframe` is True, the inputframes are assumed to be derived from 
    dropframe timecode and the output timecode will also be dropframe.
    """
    helpers.test_support(fps)

    if dropframe:
        totalframes = helpers.adjust_df_frames(inputframes, fps, True)
    else:
        totalframes = inputframes
    hrs, mins, secs, frames = helpers.frames_to_tuple(totalframes, fps)

    tcints=[hrs,mins,secs,frames]
    tcstrings = [f"{tc:02}" for tc in tcints]
    formattedtc = ":".join(tcstrings)

    if dropframe:
        helpers.is_valid_df_frame(mins, secs, frames, fps, True)
        formattedtc = formattedtc[0:8] + ";" + formattedtc[9:]

    return formattedtc

def tc_to_frames(tcstr: str, fps: float, df_by_delim: bool=True, force_df: bool=False) -> int:
    """
    Convert timecode string to frames.

    If `df_by_delim` is True, the timecode string is assumed to be
    dropframe if it contains a semicolon.

    If `force_df` is True, the timecode string is assumed to always be dropframe.
    """
    helpers.test_support(fps)

    if force_df or (df_by_delim and ";" in tcstr):
        df = True
    else:
        df = False

    if df:
        helpers.test_dropframe_support(fps)
    helpers.is_valid_tc_frame(tcstr, fps, df, True)

    hrs, mins, secs, frames = helpers.tc_to_tuple(tcstr)

    fps_round = round(fps)
    ndf_frames = (hrs * 3600 * fps_round) + (mins * 60 * fps_round) + (secs * fps_round) + frames

    if df:
        return helpers.adjust_df_frames(ndf_frames, fps, input_df_aligned=False)
    else:
        return ndf_frames

def frames_to_ms(frames: int, fps: float) -> float:
    """
    Convert frames to milliseconds.
    """
    helpers.test_support(fps)

    if isinstance(fps, int) or fps.is_integer():
        framems = 1000/fps
    else:
        fps = (round(fps)*1000) / 1001
        framems = 1000/fps

    return frames * framems

def ms_to_frames(ms: float, fps: float) -> int:
    """
    Convert milliseconds to frames.
    """
    helpers.test_support(fps)

    if isinstance(fps, int) or fps.is_integer():
        framems = 1000/fps
    else:
        fps = (round(fps)*1000) / 1001
        framems = 1000/fps

    return round(ms/framems)

def duration(start_tc: str, end_tc: str, fps: float, dropframe: bool=False) -> str:
    """Get the duration between two timecodes"""
    start_frames = tc_to_frames(start_tc, fps, df_by_delim=False, force_df=dropframe)
    end_frames = tc_to_frames(end_tc, fps, df_by_delim=False, force_df=dropframe)
    if end_frames < start_frames:
        raise ValueError("End timecode cannot be less than start timecode: {start_tc} > {end_tc}")
    return frames_to_tc(end_frames-start_frames, fps, dropframe)