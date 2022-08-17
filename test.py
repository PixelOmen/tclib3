import tclib3


start = "00:57:30;02"
end = "01:45:34;18"

print(tclib3.duration(start, end, 29.97, True))