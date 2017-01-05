#!/usr/bin/python

# JMSUM is a script which extracts summaries given a set of .JLT data from Apache JMeter. 

# Ecleipteon wrote it
# luc.castiglione@studenti.unina.it
# This Code is an open source software and it's released under GNU v3 License
# Use it at your own risk, if you find a bug you can open an issue on github
# Cià

import os,sys,getopt


def parse_file(filename):
	lines = open(filename, "r").read().splitlines()
	lines.pop(0)
	
	res = get_labels(lines);

	labels = res[0]
	samples = res[1]

	duration = get_duration(lines)

	avg = averages(lines, labels)
	tot_avg = total_avg(lines)
	
	tot_samples = 0	

	for sample in samples:
		tot_samples += sample

	return [labels, samples, avg, duration, tot_avg, tot_samples]

def get_labels(lines):
	labels = [] 
	samples = []

	for line in lines:
		mammt = "".join(line)
		values = mammt.split(',')
		
		if values[2] in labels:
			samples[labels.index(values[2])] += 1
		else:
        		labels.append(values[2])
			samples.append(1)
	
	return labels, samples

def total_avg(lines):
	sum = 0
	for line in lines:
		l = "".join(line).split(',')
		sum += long(l[1])

	return (sum/len(lines))
	
def averages(lines, labels):
	grouped_average = []

	for label in labels:
		temp_label = "".join(label)
		elapsed = []
		
		for line in lines:
			temp_line = "".join(line)
			values = temp_line.split(',')
			
			if values[2] == temp_label:
				elapsed.append(values[1])
		
		sum = 0

		for value in elapsed:
			svalue = "".join(value)
			ivalue = int(svalue)
			sum += ivalue

		average = (sum / len(elapsed))
		grouped_average.append(average)

	return grouped_average

def get_duration(lines):
	first_line = "".join(lines[0]).split(',')
	last_line = "".join(lines.pop()).split(',')

	start = float(first_line[0])
	end = float(last_line[0])+float(last_line[1])

	return (end-start)/1000


def partial_stat(filename, bool_save, verbose):
	values = parse_file(filename)
	summary = []
	
	# Calculates summaryzed stats for this file
	total_av = values[4]	
	tots = values[5]
	throughput = round(tots/values[3],1)
	duration = values[3]

	summary.append(filename)
	summary.append(tots)
	summary.append(total_av)
	summary.append(throughput)
	summary.append(duration)
	summary.append(values) # Values contains partial stats for each file, it may be useful, who knows.

	if verbose == 1:
	# Print Partial Stats for the analyzed file 
		print "label, samples, average, throughput [r/s], duration [s]"
		for i in range(0, len(values[0])): 
			print values[0][i] + ", "+ str(values[1][i])+", " +str(values[2][i])+", "+ str(values[1][i]/values[3])+", "+str(values[3])
	

		print "TOTAL" + ", "+ str(tots)+", " +str(total_av)+", "+ str(throughput)

	
	# Write out some stuff, if desired
	if (bool_save == 1):
		out_file = open(filename+"_summary.csv", "w")
		out_file.write("label, samples, average, throughput [r/s],duration [s]\n")

		for i in range(0, len(values[0])): 
			out_file.write(values[0][i] + ", "+ str(values[1][i])+", " +str(values[2][i])+", "+ str(values[1][i]/values[3])+","+duration+"\n")

		print("\nPartial output saved on "+out_file.name)		
		out_file.close()
		
	

	return summary



summaries = []

def main(argv):
	verbose = 0
	directory = 0
	outfile = 0

	try:
		opts, args = getopt.getopt(argv, "hd:o:v")
	except getopt.GetoptError:
		print "JMSUM.py -d directory of your JTL -o oufile.csv [-v for verbose mode] "
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print "JMSUM.py -d directory of your JTL -o oufile.csv [-v for verbose mode] "
			sys.exit()
		elif opt == '-d':
			directory = arg
		elif opt == '-v':
			verbose = 1
		elif opt == '-o':
			outfile = arg

	
	if directory == 0 or outfile == 0 :
		print "JMSUM.py -d directory of your JTL -o oufile [-v for verbose mode] " 
		sys.exit(2)


	for f in sorted(os.listdir(directory)):
   		if f.endswith(".jtl"):
        		summaries.append(partial_stat(directory+"/"+f, 0, verbose))

	# Print Summary on screen 	
	print "label, samples, average, throughput [r/s], duration [s]"
	for summary in summaries:
		print summary[0]+", "+str(summary[1])+", "+str(summary[2])+", "+str(summary[3])+", "+str(summary[4])

	# Write out summary stuff
	out_file = open(outfile+".csv", "w")
	out_file.write("label, samples, average, throughput [r/s], duration [s]\n")
	for summary in summaries:
		out_file.write(summary[0]+", "+str(summary[1])+", "+str(summary[2])+", "+str(summary[3])+", "+str(summary[4])+"\n")



if __name__ == "__main__":
	main(sys.argv[1:])
