# SeaGlider-AutoCapFile-check

**Description**

Checks the .cap file generated by the seaglider

r2 version works with both SG66X and SG67X CAP file formats.

**Files**
- *Cap_check_r2.zip* contains the ZIP file with the executable GUI (for Windows).
  - Use *glider_limits.txt* to edit the parameter limits such as currents, AD/s rates and current position to check GPS.
  - Execute *Glider_logcheck_rev2.exe*, open the *pXXXNNNN.cap* with *Browse file* and click on *Analyze*. Click on *Clear* to clear the screen and analyze a new file.
  - Check/uncheck *sim dive* button to anaylze using different limits for each case.

- *Glider_logcheck_rev2.py* is the python script to be executed with python installed. From a terminal type *python Glider_logcheck_rev2.py*. Note that *glider_limits.txt* must be in the same directory.
- *glider_limits.txt* contains the limits used to analyze the .cap file as mentioned before. 


![image](https://user-images.githubusercontent.com/89260258/130265696-31733af2-6b14-4bfe-88f7-5faaa6b67aba.png)
![image (1)](https://user-images.githubusercontent.com/89260258/130265704-d43a02fa-93f3-49b3-a579-b64af92545cf.png)

