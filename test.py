from audioop import mul
import tclib3


test = "00:43:00;10"
test2 = "00:16:00;29"

# frames = tclib3.tc_to_frames(test, 29.97)

tcstring = tclib3.frames_to_tc(3598, 29.97, True)
print(tcstring)

# 15 = 27001
# 16 = 28799
# 01:29:59;29 = 161837
# 00:43:00;10 = 77332

# fps = 30
# multiplier = 2

# remaining_frames = 77332
# totalmins = 0
# while True:
#     if totalmins % 10 == 0:
#         to_subtract = (fps * 60)
#     else:
#         to_subtract = (fps * 60) - multiplier
#     remaining_frames -= to_subtract
#     if remaining_frames < 0:
#         remaining_frames += to_subtract
#         break
#     totalmins += 1

# hrs = int(totalmins / 60)
# mins = totalmins % 60
# secs = int(remaining_frames / fps)
# frames = (remaining_frames % fps) + multiplier
# print(hrs)
# print(mins)
# print(secs)
# print(frames)