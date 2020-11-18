def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step
