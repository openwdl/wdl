# usr/bin/python

######################################################################################
# This script creates interval subset lists from a master list for scattering N-ways #
# 																					 #
# Usage: 																			 #
# python create_scatter_intervals.py \												 #
# 	master.interval_list 50 4 wgs_intervals "WGS intervals scattered 50-ways"		 #
######################################################################################

import os
import sys

# CLI arguments
master_list_file = sys.argv[1]
desired_N = int(sys.argv[2])
wiggle_factor = int(sys.argv[3])
dir_name = sys.argv[4]
comment = "@CO\t"+sys.argv[5]+"\n"

# Read in the master list file contents: 
with open(master_list_file, "r") as master_list:
	
	header_lines = []
	intervals_list = []
	longest_interval = 0

	for line in master_list:
		# store the header lines (starting with @) to serve as output stub
		if line.startswith("@"):
			header_lines.append(line)
		else:
			line_split = line.split("\t")
			length = int(line_split[2])-int(line_split[1])
			intervals_list.append((line, length))
			
			# keep track of what is the longest interval
			if length > longest_interval:
				longest_interval = length

print "Number of intervals: "+str(len(intervals_list))
print "Longest interval was: "+str(longest_interval)

# Determine what is the total territory covered by intervals
total_length = 0
for interval in intervals_list:
	total_length = total_length + interval[1]
	
print "Total length of covered territory: "+str(total_length)

# Determine what should be the theoretical maximum territory per subset 
# based on the desired N
max_length_per_subset = total_length / desired_N

print "Theoretical max subset length: "+str(max_length_per_subset)

# Distribute intervals to separate files

interval_count = 0
batch_count = 0
current_batch = []
current_length = 0
length_so_far = 0
batches_list = []

print "Processing..."

def dump_batch(msg):

	global batch_count
	global current_batch
	global current_length
	global length_so_far
	global interval_count
	global batches_list

	# increment appropriate counters
	batch_count +=1
	length_so_far = length_so_far + current_length
	# report batch stats
	print "\t"+str(batch_count)+". \tBatch of "+str(len(current_batch))+"\t| "+str(current_length)+" \t|"+msg+" \t| "+str(interval_count)+" \t| So far "+str(length_so_far)+" \t| Remains "+str(total_length-length_so_far)
	# store batch
	batches_list.append(current_batch)
	# reset everything
	current_batch = []
	current_length = 0
	
for interval in intervals_list:

	interval_count +=1
	#print interval_count
	
	# Is this new interval above the length limit by itself?
	if interval[1] > max_length_per_subset:
		dump_batch("close-out")
		current_batch.append(interval)
		current_length = current_length + interval[1] 
		dump_batch("godzilla")
		
	# Is this new interval putting us above the length limit when added to the batch?
	elif current_length + interval[1] > max_length_per_subset+max_length_per_subset/wiggle_factor:
		dump_batch("normal")
		current_batch.append(interval)
		current_length = current_length + interval[1] 

	else:
		current_batch.append(interval)
		current_length = current_length + interval[1] 

dump_batch("finalize")

print "Done.\nGrouped intervals into "+str(len(batches_list))+" batches."
		
# Write batches to files and compose a JSON stub
counter = 0
json_stub = ["{", "\t\"workflow.scattered_calling_intervals\": ["]
os.mkdir(dir_name)
for batch in batches_list:
	counter +=1
	path = dir_name+"/temp_"+str(counter)+"_of_"+str(len(batches_list))
	os.mkdir(path)
	with open(path+"/scattered.interval_list", "w") as intervals_file:
		# Write out the header copied from the original
		for line in header_lines:
			intervals_file.write("%s" % line)
		# Add a comment to the header
		intervals_file.write("%s" % comment)
		# Write out the intervals
		for interval in batch:
			intervals_file.write("%s" % interval[0])	
	
	# add the json line				
	json_stub.append("\t\t\"gs://bucket/dir/"+path+"/scattered.interval_list\",")
json_stub.append("\t]")
json_stub.append("}")

print "Wrote "+str(counter)+" interval files to \""+dir_name+"/temp_n_of_N/scattered.interval_list\""			

# Write out the json stub
with open("scattered_intervals.json", "w") as json_file:
	for line in json_stub:
		json_file.write("%s\n" % line)

print "Wrote a JSON stub to \"scattered_intervals.json\""





