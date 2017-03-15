tic = 0
time = 0
while True:
    time +=1
    time_elapsed = time  - tic
    if (time_elapsed>8):
        print("flash")				# beat found, flash blue LED
        tic = time	# reset tic
    elif (time_elapsed > 5):	# if more than 500ms since last beat
        print("flash")			# beat found, flash blue LED
        tic = time