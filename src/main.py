from . import helpers

def frames_to_tc(inputframes: int, fps: float=24, df_output: bool=False) -> str:
    """
    Convert frames to timecode.
    If `df_output` is True, the timecode string will be dropframe.
    If `df_input` is True, the input frames are assumed to be dropframe.
    """
    helpers.test_support(fps)

    if df_output:
        totalframes = helpers.adjust_df_frames(inputframes, fps, True)
    else:
        totalframes = inputframes
    hrs, mins, secs, frames = helpers.frames_to_tuple(totalframes, fps)

    tcints=[hrs,mins,secs,frames]
    tcstrings = [f"{tc:02}" for tc in tcints]
    formattedtc = ":".join(tcstrings)

    if df_output:
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

    clean_tcstr = tcstr.replace(";", ":")
    tcsplit = clean_tcstr.split(":")

    hrs = int(tcsplit[0])
    mins = int(tcsplit[1])
    secs = int(tcsplit[2])
    frames = int(tcsplit[3])

    fps_round = round(fps)
    ndf_frames = (hrs * 3600 * fps_round) + (mins * 60 * fps_round) + (secs * fps_round) + frames

    if df:
        helpers.test_dropframe(fps)
        helpers.is_valid_df_frame(mins, secs, frames, fps, True)
        return helpers.adjust_df_frames(ndf_frames, fps, input_df_aligned=False)
    else:
        return ndf_frames

def frames_to_ms(frames: int, fps: float) -> float:
    """
    Convert frames to milliseconds.
    If hrminsec is True, returns a tuple of (int, int, float), (hours, minutes, seconds)
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
    If hrminsec is True, ms must be a tuple of (hours, minutes, seconds) (int, int, float)
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
    start_frames = tc_to_frames(start_tc, fps)
    end_frames = tc_to_frames(end_tc, fps)
    if end_frames < start_frames:
        raise ValueError("End timecode cannot be less than start timecode: {start_tc} > {end_tc}")
    return frames_to_tc(end_frames-start_frames, fps, dropframe)