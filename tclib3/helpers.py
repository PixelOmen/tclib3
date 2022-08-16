SUPPORTED_FRAMERATES = [23.98, 23.976, 24, 29.97, 30, 59.94, 60]
SUPPORTED_DROPFRAME = [29.97, 59.94]

def test_support(fps: float) -> None:
    if fps not in SUPPORTED_FRAMERATES:
        raise ValueError(f"{fps} - Framerate not supported. Framerates supported = {SUPPORTED_FRAMERATES}")

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

def prezero(num: int) -> str:
    if num < 10:
        strnum = "0" + str(num)
    else:
        strnum = str(num)
    return strnum

def frames_to_tuple(frames: int, fps: float, valid_fps_only: bool=False) -> tuple[int, int, int, int]:
    if valid_fps_only:
        test_support(fps)
    fps = round(fps)
    tcframes = frames % fps
    totalseconds = int(frames / fps)
    tchours = int(totalseconds / 3600)
    remaining_secs = totalseconds % 3600
    tcmins = int(remaining_secs / 60)
    tcsecs = int(remaining_secs % 60)
    tcframes = frames%fps
    return (tchours,tcmins,tcsecs,tcframes)

def remove_df_frames(totalframes: int, fps: float) -> int:
    _, multiplier = test_dropframe(fps)
    hrs, mins, secs, frames = frames_to_tuple(totalframes, fps)
    totalmins = (hrs * 60) + mins
    potentialdrops = totalmins * multiplier
    tenthmin_frames = int(totalmins/10) * multiplier
    frames_to_remove = potentialdrops - tenthmin_frames
    return totalframes - frames_to_remove

def is_valid_df_frame(mins: int, frames: int, fps: float, self_raise: bool=False) -> bool:
    _, multiplier = test_dropframe(fps)
    isvalid = not (frames < multiplier and mins % 10 != 0)
    if not isvalid and self_raise:
        raise ValueError(f"Invalid frame number in DFTC: Mins={mins} Frame={frames}")
    return isvalid