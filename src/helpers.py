SUPPORTED_DROPFRAME = [29.97, 59.94]
SUPPORTED_FRAMERATES = [23.98, 23.976, 24, 25, 29.97, 30, 59.94, 60]

def test_support(fps: float) -> None:
    if fps not in SUPPORTED_FRAMERATES:
        raise ValueError(f"{fps} - Framerate not supported. Framerates supported = {SUPPORTED_FRAMERATES}")
    
def test_dropframe(fps: float, self_raise: bool=True) -> tuple[bool, int]:
    """
    Test if the framerate is dropframe and return the dropframe multiplier.
    If `self_raise` is True, it raises a ValueError if the fps is not supported.
    Returns a tuple (bool, int) where the bool is True if the framerate is dropframe
    and the int is the dropframe multiplier.
    """
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
    
def is_valid_df_frame(mins: int, secs: int, frames: int, fps: float, self_raise: bool=False) -> bool:
    """ Check if the frame number is valid in dropframe timecode """
    _, multiplier = test_dropframe(fps)
    isvalid = not (frames < multiplier and secs == 0 and mins % 10 != 0)
    if not isvalid and self_raise:
        raise ValueError(f"Invalid frame number in DFTC: Mins={mins} Frame={frames}")
    return isvalid

def adjust_df_frames(totalframes: int, fps: float, input_df_aligned: bool=True) -> int:
    """
    Adjusts the frame count for compatibility between dropframe and non-dropframe calculations.
    
    `input_df_aligned` = True assumes the input frames are already DF aligned and adjusts to the
    equivalent frame count needed so that a conversion to DF timecode using NDF formulas will be
    accurate to the original frame count.

    `input_df_aligned` = False assumes the input frames were derived from a DF timecode using
    a NDF conversion and adjusts to the actual DF frame count.
    """
    _, multiplier = test_dropframe(fps)

    if input_df_aligned:
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