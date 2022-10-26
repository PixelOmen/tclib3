from audioop import mul


SUPPORTED_FRAMERATES = [23.98, 23.976, 24, 25, 29.97, 30, 59.94, 60]
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

def frames_to_tuple(totalframes: int, fps: float, dropframe: bool=False, valid_fps_only: bool=False) -> tuple[int, int, int, int]:
    if valid_fps_only:
        test_support(fps)
    if dropframe:
        _, multiplier = test_dropframe(fps)
        fps = round(fps)
        remaining_frames = totalframes
        totalmins = 0
        while True:
            if totalmins % 10 == 0:
                to_subtract = (fps * 60)
            else:
                to_subtract = (fps * 60) - multiplier
            remaining_frames -= to_subtract
            if remaining_frames < 0:
                remaining_frames += to_subtract
                break
            totalmins += 1
        tchours = int(totalmins / 60)
        tcmins = totalmins % 60
        tcsecs = int(remaining_frames / fps)
        tcframes = (remaining_frames % fps) + multiplier
        return (tchours,tcmins,tcsecs,tcframes)
    else:
        fps = round(fps)
        tcframes = totalframes % fps
        totalseconds = int(totalframes / fps)
        tchours = int(totalseconds / 3600)
        remaining_secs = totalseconds % 3600
        tcmins = int(remaining_secs / 60)
        tcsecs = int(remaining_secs % 60)
        tcframes = totalframes%fps
        return (tchours,tcmins,tcsecs,tcframes)

def adjust_df_frames(totalframes: int, fps: float, add: bool=False) -> int:
    _, multiplier = test_dropframe(fps)
    hrs, mins, _, _ = frames_to_tuple(totalframes, fps, dropframe=True)
    totalmins = (hrs * 60) + mins
    potentialdrops = (totalmins) * multiplier
    tenthmin_frames = int(totalmins/10) * multiplier
    frames_to_remove = potentialdrops - tenthmin_frames
    if add:
        return totalframes + frames_to_remove
    else:
        return totalframes - frames_to_remove

def is_valid_df_frame(mins: int, secs: int, frames: int, fps: float, self_raise: bool=False) -> bool:
    _, multiplier = test_dropframe(fps)
    isvalid = not (frames < multiplier and secs == 0 and mins % 10 != 0)
    if not isvalid and self_raise:
        raise ValueError(f"Invalid frame number in DFTC: Mins={mins} Frame={frames}")
    return isvalid