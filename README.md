# IK1552
This repository consists of tools for use with KTH's IK1552 course.

======================================================================
## iperf3-json-to-xlsx.py

### Purpose
The program outputs a file named: experiments.xlsx
with each input JSON file as a sheet and with all of the data collected on an sheet named: All

### Input
```
iperf3-json-to-xlsx.py --dir directory_name
```
If directory_name is . it proces the current directory.

### Output
    a file named: experiments.xlsx

### Notes
The program assumes that there are a set of files produced by iPerf3 with the --json argument
and that names of the files have the form: CONGESTIONCTRL_RATE_DELAY_LOSS
where CONGESTIONCTRL might be bbr, reno, etc.
      RATE might be 100mbit or simply 100 (both for 100 Mbps)
      DELAY is the delay in ms (as an integer without units)
      LOSS is the loss probability (as an integer) 
