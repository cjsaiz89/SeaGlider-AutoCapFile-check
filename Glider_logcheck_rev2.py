from tkinter import filedialog
from tkinter import * 
from tkinter import ttk
from datetime import datetime



def get_file():
    global file_path, file_selected
    try:
        file_path = filedialog.askopenfilename(title ="Select file to check...")
        file_selected = file_path.split('/')[-1] # get only file name 
        print(file_path)
        print(file_selected)
        sel_file.set(file_selected)
        if file_selected != '':
            status_label.config(background='green', foreground='white')
    except:
        sel_file.set('Error selecting file')
        status_label.config(background='red', foreground='white')

def check_line(line, num):
    # Get current index
    pos = text_box.index('end')
    p1 = pos + '-1 lines'
    p2 = pos + '-1 lines + 3 chars'
    # Define tags
    text_box.tag_config('ok', background='green', foreground='white')
    text_box.tag_config('warning', background='yellow', foreground='black')
    text_box.tag_config('critical', background='red', foreground='white')
    text_box.tag_config('error', background='orange', foreground='white')
    text_box.tag_config('caution', background='magenta', foreground='white')
    text_box.tag_config('retry', background='blue', foreground='white')
    text_box.tag_config('fail', background='cyan', foreground='black')
    text_box.tag_config('timeout', background='black', foreground='white')
    # Strip end of line  
    line = line.rstrip("\n")
    # Check for version
    if ('Version' in line and 'Built' in line):

        if '66.12/DORADO' in line:  
            txt = '--> OK -VERSION: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('ok', p1, p2)
            # text_box.tag_config('ok', background='green', foreground='white')
        else:
            txt = '--> WARNING -VERSION: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('warning',p1,p2)
            # text_box.tag_config('warning', background='orange', foreground='white')
           

    if ',C,' in line:
        if ',B,C,' in line:
            pass
        else:
            txt = '--> CRITICAL VALUE: ' + line  + '\b\b [' + str(num) + ']\n'
            text_box.insert(pos, txt)
            text_box.tag_add('critical',p1,p2)
            # text_box.tag_config('critical', background='red', foreground='white')

    if ('WARNING' in line) or ('Warning' in line):
        if '$PITCH_TIMEOUT' in line:
            pass
        elif ('Potential' in line) or ('Potentially' in line):
            pass
        elif 'SBATHY' in line:
            pass
        elif ('speed' in line):
            if (sim_dive == True):
                pass
        else:
            txt = '--> WARNING -MISC: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('warning',p1,p2)
            # text_box.tag_config('warning', background='orange', foreground='white')

    if '$GPRMC' in line:
        # PC date
        pc_day = datetime.utcnow().day
        pc_month = datetime.utcnow().month
        pc_year = datetime.utcnow().year
        # GPS date time
        gps = line.split(',')
        gps_month = gps[12][2:4]
        gps_day = gps[12][0:2]
        gps_year = gps[12][4:6]
        gps_hour = gps[4][0:2]
        gps_minute = gps[4][2:4]
        gps_second = gps[4][4:6]
        
        lat_dec = lat_deg2dec( float(deg(gps[6])),float(minu(gps[6])),gps[7] )
        lon_dec = lon_deg2dec(float(deg(gps[8])),float(minu(gps[8])), gps[9] )

        if ( ( lat_dec >= lat-e and lat_dec <= lat+e ) and ( lon_dec >= lon-e and lon_dec <= lat+e) and ( pc_day == gps_day and pc_month == gps_month and pc_year == gps_year) ):
            txt = '--> OK GPS: within ' + str(e) + '° of position expected and date correct' + ' [' + str(num) + ']\n'
            text_box.insert(pos, txt)
            text_box.tag_add('ok',p1,p2)
            print('its within:', lat, lon, lat_dec, lon_dec)
        else:
            if ( ( lat_dec >= lat-e and lat_dec <= lat+e ) and ( lon_dec >= lon-e and lon_dec <= lat+e) ) == False:
                gps_error = 'position off'
            elif (( pc_day == gps_day and pc_month == gps_month and pc_year == gps_year)) == False:
                gps_error = 'date off'
            
            txt = '--> WARNING -GPS ('+ gps_error + '):  '+ 'Time: ' + gps_hour + ':' + gps_minute + ':' + gps_second 
            txt = txt + ' Date: ' + gps_month +'/' + gps_day +'/' + gps_year
            txt = txt + ' Lat: ' + deg(gps[6]) + '°' + minu(gps[6]) + "'" + gps[7] 
            txt = txt + ' Lon: ' + deg(gps[8]) + '°' + minu(gps[8]) + "'" + gps[9] + ' [' + str(num) + ']\n'
            text_box.insert(pos, txt)
            text_box.tag_add('warning',p1,p2)
            print('its outside:', lat, lon, lat_dec, lon_dec)


    if 'ERROR' in line or 'error' in line:
        if 'NUM' in line or 'MAXERROR' in line or 'ERRORS=0':
            pass
        else:
            txt = '--> ERROR -MISC: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('error',p1,p2)
    
    if 'FAILED' in line or 'failed' in line:
        if 'bathymetry' in line:
            pass
        else:
            txt = '--> FAIL -MISC: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('fail',p1,p2)

    if 'retries' in line:
            txt = '--> RETRY -MISC: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('retry',p1,p2)

    if 'timeout' in line:
        if 'timeouts' in line or 'lengthened' in line or 'SSENSOR' in line or 'HXPDR' in line:
            pass
        else:
            txt = '--> TIMEOUT -MISC: ' + line + ' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('timeout',p1,p2)


    out_of_range = False # flag

    if 'completed' in line and 'AD/sec' in line:
        line_comma = line.split(',',3)
        last_part = line_comma[-1]
        line_space = last_part.split()
        # print('line space:', line_space)
        ads_index = line_space.index('AD/sec')
        ads = line_space[ads_index-1] # AD/sec
        ads = float(ads)
        system = line_comma[1] # type of motion HVBD, HROLL, HPITCH
        motion = line_space[0]
        time_index = line_space.index('took')
        ttime = line_space[time_index+1] # time it took in seconds
        ttime = float(ttime)
        try:
            amp_index = line_space.index('mA')
            amp = line_space[amp_index-1] # average current
            amp = float(amp)
        except:
            i = 0
            while True:
                if 'mA' in line_space[i]:
                    amp = float(line_space[i][:-2])
                    break
                i = i+1
        
        # print('System:',system,'Action:', motion,'AD/sec:',str(ads), ' current:', str(amp),' time:',str(ttime))
        

        if motion == 'VBD':
            total_items = len(line_space) # num of elements in list
            cc_index = [0,1]
            k=0
            for j in range(0,total_items): # search cc in line_space list
                if line_space[j] == 'cc':
                    cc_index[k] = j-1 # store the index with cc
                    k=k+1
            v0 = float(line_space[cc_index[0]])
            vf = float(line_space[cc_index[1]])

            # print(cc_index[0], cc_index[1]) # print index where cc are
            
            if v0 > vf: # if start volume is larger than end volume
                motion = 'Bleed'
            else:
                motion = 'Pump'
            # print(motion)
            # quit()

        lh = ''
        if ttime > 0.1: 
            if sim_dive.get() == True: # use sim dives limits

                if motion == 'Pump':
                    if ads < MIN_spump: 
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_spump:
                        out_of_range = True
                        lh = 'high AD rate'
                    if amp > MAXI_spump:
                        out_of_range = True
                        lh = 'high current'

                if motion == 'Bleed':
                    if ads < MIN_sbleed:
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_sbleed:
                        out_of_range = True
                        lh = 'high AD rate' 
                    if amp > MAXI_sbleed:
                        out_of_range = True
                        lh = 'high current' 

                if motion == 'Roll':
                    if ads < MIN_sroll:
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_sroll:
                        out_of_range = True
                        lh = 'high AD rate'
                    if amp > MAXI_sroll:
                        out_of_range = True
                        lh = 'high current'  

                if motion == 'Pitch':
                    if ads < MIN_spitch:
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_spitch:  
                        out_of_range = True
                        lh = 'high AD rate'     
                    if amp > MAXI_spitch:  
                        out_of_range = True
                        lh = 'high current'

            if sim_dive.get() == False: # use real dives limits

                if motion == 'Pump':
                    if ads < MIN_pump: 
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_pump:
                        out_of_range = True
                        lh = 'high AD rate'
                    if amp > MAXI_pump:
                        out_of_range = True
                        lh = 'high current'  

                if motion == 'Bleed':
                    if ads < MIN_bleed:
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_bleed:
                        out_of_range = True
                        lh = 'high AD rate'
                    if amp > MAXI_bleed:
                        out_of_range = True
                        lh = 'high current'

                if motion == 'Roll':
                    if ads < MIN_roll:
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_roll:
                        out_of_range = True
                        lh = 'high AD rate'
                    if amp > MAXI_roll:
                        out_of_range = True
                        lh = 'high current'

                if motion == 'Pitch':
                    if ads < MIN_pitch:
                        out_of_range = True
                        lh = 'low AD rate'
                    if ads > MAX_pitch:  
                        out_of_range = True
                        lh = 'high AD rate'
                    if amp > MAXI_pitch:  
                        out_of_range = True
                        lh = 'high current'

        if out_of_range == True:
            txt = '--> CAUTION -' + system + ' (' + lh + '): ' + motion + ' had ' + str(ads) + ' AD/sec in ' + str(ttime) + ' sec w/ I= ' + str(amp) + ' mA' +' [' + str(num) + ']\n' 
            text_box.insert(pos, txt)
            text_box.tag_add('caution',p1,p2)
        

                 

def deg(x):
    lx = len(str(int(float(x))))
    xdeg = str(int(float(x)))
    if ( lx == 3):
        return xdeg[0:1]
    elif ( lx == 4):
        return xdeg[0:2]
    elif ( lx == 5):
        return xdeg[0:3]

def minu(x):
    lx = len(str(int(float(x))))
    xmin = str(float(x))
    if (lx == 3):
        return xmin[1:]
    elif (lx == 4):
        return xmin[2:]
    elif (lx == 5):
        return xmin[3:]   

def lat_deg2dec(lat_deg,lat_min, ns):
    a = 1
    if ns == 'N': a = 1
    if ns == "S": a = -1
    return (lat_deg + lat_min/60)*a

def lon_deg2dec( lon_deg,lon_min, ew):
    a = 1
    if ew == 'E': a = 1
    if ew == "W": a = -1
    return (lon_deg + lon_min/60)*a

# Read simdive and check lines
def check_file():
    global fout
    text_box.insert('0.0', 'Starting check...\n')

    # open and read file
    try:
        f = open( file_path, 'r' )
        print("File to read opened")
    except:
        print("File can't be opened")
    if(f):
        count = 0
        for line in f: 
            # print( line)
            check_line(line, count)
            count = count +1
            
            
    # print(count, 'lines read')
    f.close()
    # Write number of lines read
    txt_end = '--------------------------------------------------'
    txt_end = txt_end + '\n' + str(count) + ' lines read from file'  
    text_box.insert('end', txt_end)

# Read limits set on file
def get_glider_limits(fname):
    global MIN_spump, MAX_spump, MIN_sbleed, MAX_sbleed, MIN_sroll, MAX_sroll, MIN_spitch, MAX_spitch # sim dive limits
    global MIN_pump, MAX_pump, MIN_bleed, MAX_bleed, MIN_roll, MAX_roll, MIN_pitch, MAX_pitch # regular dive limits
    global lat, lon, e # lat, lon and window margin to check gps
    global MAXI_spump, MAXI_sbleed, MAXI_sroll, MAXI_spitch # limit currents for sim dives
    global MAXI_pump, MAXI_bleed, MAXI_roll, MAXI_pitch # limit currents for real dives

    flimits = open(fname, 'r')  
    for line in flimits:
        
        if '#' in line:
            pass
        else:
            line = line.replace('\n','')
            lim = line.split(',')
            val = float(lim[1])

            if 'LAT' in line:
                lat = val
            if 'LON' in line:
                lon = val
            if 'RAD' in line:
                e = val 
            if 'MIN_spump' in line:
                MIN_spump = val
            if 'MAX_spump' in line:
                MAX_spump = val
            if 'MIN_sbleed' in line:
                MIN_sbleed = val
            if 'MAX_sbleed' in line:
                MAX_sbleed = val
            if 'MIN_sroll' in line:
                MIN_sroll = val
            if 'MAX_sroll' in line:
                MAX_sroll = val
            if 'MIN_spitch' in line:
                MIN_spitch = val
            if 'MAX_spitch' in line:
                MAX_spitch = val
            if 'MIN_pump' in line:
                MIN_pump = val
            if 'MAX_pump' in line:
                MAX_pump = val
            if 'MIN_bleed' in line:
                MIN_bleed = val
            if 'MAX_bleed' in line:
                MAX_bleed = val
            if 'MIN_roll' in line:
                MIN_roll = val
            if 'MAX_roll' in line:
                MAX_roll = val
            if 'MIN_pitch' in line:
                MIN_pitch = val
            if 'MAX_pitch' in line:
                MAX_pitch = val
            if 'MAXI_spump' in line:
                MAXI_spump = val
            if 'MAXI_sbleed' in line:
                MAXI_sbleed = val
            if 'MAXI_sroll' in line:
                MAXI_sroll = val
            if 'MAXI_spitch' in line:
                MAXI_spitch = val
            if 'MAXI_pump' in line:
                MAXI_pump = val
            if 'MAXI_bleed' in line:
                MAXI_bleed = val
            if 'MAXI_roll' in line:
                MAXI_roll = val
            if 'MAXI_pitch' in line:
                MAXI_pitch = val   

    flimits.close()
    print( MIN_spump, MAX_spump, MIN_sbleed, MAX_sbleed, MIN_sroll, MAX_sroll, MIN_spitch, MAX_spitch) # sim dive limits
    print( MIN_pump, MAX_pump, MIN_bleed, MAX_bleed, MIN_roll, MAX_roll, MIN_pitch, MAX_pitch ) # regular dive limits
    print(lat,lon,e)
    print(MAXI_spump, MAXI_sbleed, MAXI_sroll, MAXI_spitch) 
    print(MAXI_pump, MAXI_bleed, MAXI_roll, MAXI_pitch)

def clear_text():
    text_box.delete('1.0',END)

def main():
    global status_label, sel_file, text_box
    # global lat, lon, e
    global sim_dive
    
    # Limits file
    get_glider_limits('glider_limits.txt')
    # Make window
    root = Tk()    
    root.title('Log file checker')
    # Sim dive?
    sim_dive = BooleanVar()
    sim_dive.set(True)
    ttk.Checkbutton(root, text = 'Sim dive', variable = sim_dive).grid(row = 0, column = 1, sticky = 'nesw', padx = 2, pady = 1)
    # Description
    Label(root, text = 'Select Seaglider log file to check for errors:').grid(row=1, column=0, sticky='nesw',padx = 2, pady = 1)
    # Browse button
    ttk.Button(root, text = 'Browse file', command=get_file).grid(row = 1, column = 1, sticky='nsew',padx = 2, pady = 1)
    sel_file = StringVar()
    sel_file.set('no file selected')
    # Show file selected 
    status_label = Label(root, textvariable=sel_file,justify = CENTER, font = ('Courier', 10, 'italic'))
    status_label.grid(row=2,column=0, sticky='nwes',padx = 2, pady = 1)
    # Open file and analyze
    ttk.Button(root, text = 'Analyze', command= check_file).grid(row = 2, column = 1, sticky='nsew',padx = 2, pady = 1)
    # Display output
    Label(root, text='Output',justify = CENTER).grid(row = 3, column = 0, sticky='nsew',padx = 2, pady = 1)
    ttk.Button(root, text = 'Clear', command= clear_text).grid(row = 3, column = 1, sticky='nsew',padx = 2, pady = 1)
    text_box = Text(root, width = 120, height = 15, font=('Courier',10), wrap=WORD)
    text_box.grid(row = 4, column = 0, sticky = 'nsw', padx = 2, pady = 1)
    text_scroll = ttk.Scrollbar(root, orient = VERTICAL, command = text_box.yview )
    text_scroll.grid(row = 4, column = 1, sticky = 'nse')
    text_box.config(yscrollcommand = text_scroll.set)
    root.mainloop()

# Bottom code
if __name__ == "__main__":
    main()