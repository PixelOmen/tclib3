SUPPORTED_DROPFRAME = [29.97, 59.94]
SUPPORTED_FRAMERATES = [23.98, 23.976, 24, 25, 29.97, 30, 59.94, 60]

def test_support(fps: float) -> None:
    if fps not in SUPPORTED_FRAMERATES:
        raise ValueError(f"{fps} - Framerate not supported. Framerates supported = {SUPPORTED_FRAMERATES}")
    
def frames_to_ms(frames: int, fps: float) -> float:
    """
    Convert frames to milliseconds.
    If hrminsec is True, returns a tuple of (int, int, float), (hours, minutes, seconds)
    """
    test_support(fps)

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
    test_support(fps)

    if isinstance(fps, int) or fps.is_integer():
        framems = 1000/fps
    else:
        fps = (round(fps)*1000) / 1001
        framems = 1000/fps

    return round(ms/framems)

def test_dropframe(fps: float, self_raise: bool=True) -> tuple[bool, int]:
    if fps == 29.97:
        drop_multiplier = 2
    elif fps == 59.94:
        drop_multiplier = 4
    else:
        if self_raise:
            raise ValueError(f"Dropframe not supported with fps: {fps}")
        else:
            return (False, 0)
    return (True, drop_multiplier)

def frames_to_tuple(totalframes: int, fps: float, valid_fps_only: bool=False) -> tuple[int, int, int, int]:
    """
    Convert frames to timecode tuple (hours, minutes, seconds, frames).
    If valid_fps_only is True, it raises a ValueError if the fps is not supported.
    If original frames were dropframe, frames are assumed to have already been adjusted.
    """
    if valid_fps_only:
        test_support(fps)
    fps = round(fps)
    totalseconds = int(totalframes / fps)
    tchours = int(totalseconds / 3600)
    remaining_secs = totalseconds % 3600
    tcmins = int(remaining_secs / 60)
    tcsecs = int(remaining_secs % 60)
    tcframes = totalframes%fps
    return (tchours,tcmins,tcsecs,tcframes)

def adjust_df_frames(totalframes: int, fps: float, df_input: bool=False) -> int:
    """
    Adjust frames for dropframe timecode.
    if df_input is False, it subtracts the dropped frames from the totalframes.
    If df_input is True, it adds the dropped frames back to the totalframes.
    """
    _, multiplier = test_dropframe(fps)

    if df_input:
        round_fps = round(fps)
        frames_in_droppedmin = (round_fps * 60) - multiplier
        prev_min = 0
        dropped_min = 0
        currentframes = totalframes
        while currentframes >= frames_in_droppedmin + multiplier:
            if (prev_min + 1) % 10 == 0:
                currentframes -= frames_in_droppedmin + multiplier
            else:
                currentframes -= frames_in_droppedmin
                dropped_min += 1
            prev_min += 1
        totalframes += dropped_min * multiplier
    else:
        whole_seconds = totalframes // round(fps)
        minutes = whole_seconds // 60
        tenth_min_blocks = minutes // 10
        dropped_frames = int((minutes * multiplier) - (tenth_min_blocks * multiplier))
        totalframes -= dropped_frames

    return totalframes

def is_valid_df_frame(mins: int, secs: int, frames: int, fps: float, self_raise: bool=False) -> bool:
    _, multiplier = test_dropframe(fps)
    isvalid = not (frames < multiplier and secs == 0 and mins % 10 != 0)
    if not isvalid and self_raise:
        raise ValueError(f"Invalid frame number in DFTC: Mins={mins} Frame={frames}")
    return isvalid