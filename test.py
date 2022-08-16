import tclib3


def test_listinfo(frames=86376):
	for _ in range(73):
		startingtc = tclib3.frames_to_tc(frames)
		print(f"StartTC: {startingtc}")
		ms = tclib3.frames_to_ms(frames, hrminsec=True)
		print(f"MS: {ms}")
		convframes = tclib3.ms_to_frames(ms, hrminsec=True)
		print(f"frames: {convframes}")
		convtc = tclib3.frames_to_tc(convframes)
		print(f"ConvertedTC: {convtc}")
		print(startingtc == convtc)
		if startingtc != convtc:
			raise ValueError
		print('\n')
		frames += 1


print(tclib3.tc_to_frames("00:01:00;04", 59.94))