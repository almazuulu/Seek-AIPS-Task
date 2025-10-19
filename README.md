# Seek-AIPS-Task
Coding Challenge

# Requirement
An automated traffic counter sits by a road and counts the number of cars that go past. Every half-hour the counter outputs the number of cars seen and resets the counter to zero.

A program  reads a file, where each line contains a timestamp (in yyyy-mm-ddThh:mm:ss format, i.e. ISO 8601) for the beginning of a half-hour and the number of cars seen that half hour

## Result:

###The program should output:
- The number of cars seen in total
- A sequence of lines where each line contains a date (in yyyy-mm-dd format) and the
number of cars seen on that day (eg. 2016-11-23 289) for all days listed in the input file.
- The top 3 half hours with most cars, in the same format as the input file
- The 1.5 hour period with least cars (i.e. 3 contiguous half hour records)
