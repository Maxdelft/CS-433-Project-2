Read before using the python scripts:

Run python scripts in the following order: 
1. <<singlefolder_evalglaretxt_operation_deletestray.py>> for deleting stray glare sources with <500 pixels (but with luminance more than 3000 cd/m2 thats why it was detected in evalglare) 
[Note: No need to run again since I've alr done it]
2. <<singlefolder_calc_glaremetrics.py>> for re-calculating glare metrics and contrast variables 
[Note: This is where you can add exploratory contrast variables like editing log_gc's exponents, at the end of the output since it's sequentially coded]
3. <<singlefolder_consolidate_glaremetrics.py>> for consolidating all results into a single csv.

Next, open consolidated_results.txt in excel and follow the following steps: 
1. Select first column of cells (or Ctrl-A)
2. Click Data> Text to columns > select delimiter: comma
3. Sort the "index" column alphabetically from smallest to largest (Click to expand data so all rows get sorted together) 
[Note: important that the data is sorted from p1s1, p1s2, p1s3, p1s4 for example]
4. Sort the "participant" column from smallest to largest (Click to expand data so all rows get sorted together)
[Note: important that the data is sorted from 1 to 63 for example]
5. Copy data (use Ctrl-Shift-DownArrow-RightArrow) to the main excel sheet
6. Check that the order of participants is the same (small to largest, scene 1 to 4) 

Notes for data analysis:
1. Consider to remove datapoints with CGI = 0 (no glare sources detected)