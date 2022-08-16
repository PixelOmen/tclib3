SUPPORTED_FRAMERATES = [23.98, 23.976, 24, 29.97, 30, 59.94, 60]

def test_support(fps: float) -> None:
    if fps not in SUPPORTED_FRAMERATES:
        raise ValueError(f"{fps} - Framerate not supported. Framerates supported = {SUPPORTED_FRAMERATES}")

def prezero(num: int) -> str:
    if num < 10:
        strnum = "0" + str(num)
    else:
        strnum = str(num)
    return strnum

def frames_to_tuple(frames: int, fps: float) -> tuple[int, int, int, int]:
    if fps not in SUPPORTED_FRAMERATES:
        raise ValueError(f"{fps} - Framerate not supported. Framerates supported = {SUPPORTED_FRAMERATES}")

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
    fps = round(fps)
    hrs, mins, secs, frames = frames_to_tuple(totalframes, fps)
    totalmins = (hrs * 60) + mins
    potentialdrops = totalmins * 2
    tenthmin_frames = int(totalmins/10) * 2
    frames_to_remove = potentialdrops - tenthmin_frames
    return totalframes - frames_to_remove

def is_tenthmin_df(totalframes: int, fps: float) -> bool:
    _, mins, _, _ = frames_to_tuple(totalframes, fps)
    return (mins % 10) == 0

def is_valid_df(mins: int, frames: int, self_raise: bool=False) -> bool:
    isvalid = not (frames < 2 and mins % 10 != 0)
    if not isvalid and self_raise:
        raise ValueError(f"Invalid frame number in DFTC: Mins={mins} Frame={frames}")
    return isvalid