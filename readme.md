
# TCLIB3

This library provides functionality for converting between frames, timecode, and milliseconds, supporting both non-dropframe and dropframe timecode formats. It is designed to assist in video editing and processing tasks where precise timing and synchronization are crucial.

## Features

- Convert frames to timecode (`frames_to_tc`)
- Convert timecode to frames (`tc_to_frames`)
- Convert frames to milliseconds (`frames_to_ms`)
- Convert milliseconds to frames (`ms_to_frames`)
- Calculate the duration between two timecodes (`duration`)

## Installation

PIP Wheel Install:

```bash
pip install dist/tclib3-1.0.0-py3-none-any.whl
```

Poetry virtual env:
```bash
cd tclib3
poetry install
```

## Usage

### Converting Frames to Timecode

```python
frames_to_tc(inputframes, fps=24, dropframe=False)
```

- `inputframes`: The number of frames to convert.
- `fps`: Frames per second. Default is 24.
- `dropframe`: Set to `True` if using dropframe timecode. Default is `False`.

### Converting Timecode to Frames

```python
tc_to_frames(tcstr, fps, df_by_delim=True, force_df=False)
```

- `tcstr`: The timecode string to convert.
- `fps`: Frames per second.
- `df_by_delim`: Assume dropframe if the timecode contains a semicolon. Default is `True`.
- `force_df`: Force the timecode to be treated as dropframe. Default is `False`.

### Converting Frames to Milliseconds

```python
frames_to_ms(frames, fps)
```

- `frames`: The number of frames to convert.
- `fps`: Frames per second.

### Converting Milliseconds to Frames

```python
ms_to_frames(ms, fps)
```

- `ms`: The number of milliseconds to convert.
- `fps`: Frames per second.

### Calculating Duration Between Two Timecodes

```python
duration(start_tc, end_tc, fps, dropframe=False)
```

- `start_tc`: The starting timecode.
- `end_tc`: The ending timecode.
- `fps`: Frames per second.
- `dropframe`: Set to `True` if using dropframe timecode for the calculation. Default is `False`.


## License

[MIT](https://choosealicense.com/licenses/mit/)
