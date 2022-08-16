import helpers

def frames_to_tc(totalframes, fps=24, df=False):
    helpers.test_support(fps)

    fps = round(fps)
    totalframes = helpers.remove_df_frames(totalframes, fps) if df else totalframes
    hrs, mins, secs, frames = helpers.frames_to_tuple(totalframes, fps)

    tcints=[hrs,mins,secs,frames]
    tcstrings = [helpers.prezero(tc) for tc in tcints]
    formattedtc = ":".join(tcstrings)

    if df:
        helpers.is_valid_df(mins, secs, True)
        formattedtc = formattedtc[0:8] + ";" + formattedtc[9:]

    return formattedtc


def frames_to_ms(frames, fps=24, hrminsec=False):
    helpers.test_support(fps)

    fps = float(fps)
    if fps.is_integer():
        framems = 1000/fps
    else:
        fps = (round(fps)*1000) / 1001
        framems = 1000/fps
    totalms = frames * framems
    if hrminsec:
        totalsecs = totalms / 1000
        hrs = int(totalsecs / 3600)
        remaining_secs = totalsecs % 3600
        mins = int(remaining_secs / 60)
        secs = round(remaining_secs % 60, 4)
        return [hrs, mins, secs]
    return totalms


def tc_to_frames(tcstr: str, fps: float):
    helpers.test_support(fps)

    if ";" in tcstr:
        df = True
    else:
        df = False

    fps = round(fps)
    clean_tcstr = tcstr.replace(";", ":")
    tcsplit = clean_tcstr.split(":")

    hrs = int(tcsplit[0])
    mins = int(tcsplit[1])
    secs = int(tcsplit[2])
    frames = int(tcsplit[3])
    totalframes = (hrs * 3600 * fps) + (mins * 60 * fps) + (secs * fps) + frames

    if df:
        helpers.is_valid_df(mins, secs, True)
        return helpers.remove_df_frames(totalframes, fps)
    else:
        return totalframes


def ms_to_frames(ms, fps=24, hrminsec=False):
    helpers.test_support(fps)

    fps = float(fps)
    if fps.is_integer():
        framems = 1000/fps
    else:
        fps = (round(fps)*1000) / 1001
        framems = 1000/fps
    if hrminsec:
        ms = (ms[0]*3600 + ms[1]*60 + ms[2]) * 1000
    frames = round(ms/framems)
    return frames