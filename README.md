# JMSUM
JMSUM is a script which extracts summaries given a set of .JTL data from Apache JMeter. It's usefull when you are valuating data from multiple experiments. 

I Wrote this script to summarize data coming out from multiple automated executions of Apache JMeter. The alternative was manually read each JTL test log file and manually copy each value doing my stuff.

This is the very first time I wrote something in Python and I did it in a couple of hours (yes this is an excuse because the code actually sucks even if it works, at least).

TODO:  It could not work really fine when there are errors in HTTP Responses from the server. 

```
[ecleipteon@localhost JMSUM]$ python JMSUM.py -d Random/ -o out_file 
label, samples, average, throughput [r/s], duration [s]
Random/test1.jtl, 3332, 1524, 18.4, 181.364
Random/test2.jtl, 3736, 1344, 20.6, 181.605
Random/test3.jtl, 3393, 1494, 18.7, 181.187
Random/test4.jtl, 3278, 1554, 18.1, 181.207
Random/test5.jtl, 3511, 1441, 19.4, 181.349
Random/test6.jtl, 3480, 1449, 19.2, 180.801
Random/test7.jtl, 3653, 1375, 20.2, 180.924
Random/test8.jtl, 3660, 1372, 20.2, 181.005
Random/test9.jtl, 3232, 1577, 17.8, 182.04
``````
``````
[ecleipteon@localhost JMSUM]$ python JMSUM.py -h
JMSUM.py -d directory_JTLs/ -o oufile.csv [-v for verbose mode] 
``````
