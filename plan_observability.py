import numpy as np
import csv
import matplotlib.pyplot as plt



start_hrs = 18
end_hrs = 6
date = "8.3.2023"
d = int(float(date[0:2]))
n = d - 21          # days to vernal equinox (21.3.), this works for march
metsahovi_correction = -22.5    # min, correction to LST
metsahovi_latitude = 60.2       # degrees
a_min_primary = 40  # degrees, observability limit

LST_start_hrs = ( start_hrs*60 + n*4 +12*60 + metsahovi_correction) /60  # last div converts mins to hrs
LST_end_hrs = ( end_hrs*60 + n*4 +12*60 + metsahovi_correction) /60
if LST_start_hrs > 24:
    LST_start_hrs -= 24
if LST_end_hrs > 24:
    LST_end_hrs  -= 24

def lst_hrs_to_time(lst_hrs):
    LST_time = [int(np.floor(lst_hrs)), int(np.floor((lst_hrs - np.floor(lst_hrs)) * 60))]
    return LST_time

LST_start = lst_hrs_to_time(LST_start_hrs)
LST_end = lst_hrs_to_time(LST_end_hrs)
print(f"LST: [{LST_start[0]}:{LST_start[1]}; {LST_end[0]}:{LST_end[1]}] for observation night ({d-1}-){date}")

with open("observables.csv", newline='') as savefile:
    targets = csv.reader(savefile, delimiter=',')
    plt.figure()
    i = -1
    for target in targets:
        name = target[0]
        bname  = target[1]
        RA_hrs = float(target[2]) + float(target[3]) / 60.0 + float(target[4]) / 3600.0
        dec_degs = float(target[5]) + float(target[6]) * 0.0167  # arcmin->degs
        print(f"{name},\tRA={RA_hrs},  dec={dec_degs}")

        # Moving onto source specific calcs
        RA = RA_hrs
        dec = dec_degs
        lat = metsahovi_latitude    # latitude & a_min_primary could vary per source
        a_min_primary = a_min_primary

        print(f"\nDoes the source {name} rise above {a_min_primary}deg?")
        dec_lat = dec + lat
        print(f"Dec+lat={dec_lat}°, circumpolar {dec_lat > 90}")
        dec_over_lat = dec < lat
        if dec_over_lat:
            print("Culminates South of zenith")
            a_cul = 90 - lat + dec
        else:
            print("Culminates North of zenith")
            a_cul = 90 + lat - dec

        observable = a_cul > a_min_primary
        a_cul_print = '{:.1f}'.format(a_cul)
        print(f"a_cul = {a_cul_print}°, > {a_min_primary}° --> observable: {observable}")
        a_min = a_min_primary
        label = name
        frmt = '-'

        if not observable:
            a_min_secondary = 20
            observable = a_cul > a_min_secondary
            print(f"a_cul = {a_cul_print}°, > {a_min_secondary}° --> observable: {observable}")
            if not observable:
                print("Not observable!")
                continue
            a_min = a_min_secondary
            label = name + f"  (>{a_min}°)"
            frmt = '--'


        # when does it culminate?
        LST_culminate_hrs = RA
        # TODO: fix local time conversion
        #local_solar_time = (LST_culminate_hrs - (-13) * 4 - 12 * 60 - metsahovi_correction) / 60
        print(f"Culmination at LST={RA}") #and local time {local_solar_time+24}(broken??)")

        def lst_rise_set(LST_culminate_hrs, a_m, lat, dec, prints=True):
            deg_conv = np.pi / 180.0
            cos_h = (-1.0) * np.tan(dec * deg_conv) * np.tan(lat * deg_conv) + np.sin(a_m * deg_conv) / (
                        np.cos(dec * deg_conv) * np.cos(lat * deg_conv))
            if np.abs(cos_h) > 1.0:
                print(f"Doesn't set below {a_m}°")
                return 0.0, 0.0
            h = np.arccos(cos_h)
            h_hrs = h / (2*np.pi) * 24
            print(f"h = +/-{h} ° ..= {h_hrs}hrs")
            LST_r = LST_culminate_hrs - h_hrs    # LST_rise_to_a_min
            LST_s= LST_culminate_hrs + h_hrs     # LST_sets_to_a_min
            if LST_r > 24:
                LST_r -= 24
            if LST_s > 24:
                LST_s -= 24
            LST_rise_time = lst_hrs_to_time(LST_r)
            LST_sets_time = lst_hrs_to_time(LST_s)
            if prints:
                print(f"LST of rise [{LST_rise_time[0]}:{LST_rise_time[1]}; {LST_rise_time[0]}:{LST_rise_time[1]}]"
                      + f" = {LST_r}hrs")
                print(f"LST of setting [{LST_sets_time[0]}:{LST_sets_time[1]}; {LST_sets_time[0]}:{LST_sets_time[1]}]"
                      + f" = {LST_s}hrs")

            return LST_r, LST_s

        LST_rise, LST_sets = lst_rise_set(RA, a_min, dec_degs, metsahovi_latitude)
        if LST_rise == LST_sets == 0:
            continue
        print("\n")

        LST   = np.linspace(LST_rise, LST_sets, 10)
        hline = np.linspace(i,        i,        10)
        plt.plot(LST,hline,frmt,label=label,linewidth=6)
        a_max = 65
        if a_cul > a_max:
            a_min = a_max
            LST_rise, LST_sets = lst_rise_set(RA, a_min, dec_degs, metsahovi_latitude, prints=False)
            if LST_rise == LST_sets == 0:
                continue
            print(f"LST_rise above {a_max}° = {LST_rise}")
            print(f"LST_set  above {a_max}° = {LST_sets}")
            print("\n")
            LST = np.linspace(LST_rise, LST_sets, 10)
            plt.plot(LST, hline, 'white', label=f" over obs.limit {a_max}°", linewidth=7)

        i -= 1

plt.autoscale()
plt.grid()
plt.title(f"Observation plan, ({d-1}-){date}, Metsähovi")
plt.xlabel("LST")
plt.xlim((LST_start_hrs,LST_end_hrs))
plt.legend()
plt.show()