import numpy as np


mhovi_corr = -22.5  # min
mhovi_lat = 60.2    # dec
LST_start_hrs = ( 18*60 + (-13)*4 +12*60 + mhovi_corr) /60  # last div converts mins to hrs
LST_end_hrs = ( 6*60 + (-13)*4 +12*60 + mhovi_corr) /60
LST_start = [int(np.floor(LST_start_hrs)), int(np.floor((LST_start_hrs - np.floor(LST_start_hrs))*60))]
LST_end = [int(np.floor(LST_end_hrs)), int(np.floor((LST_end_hrs - np.floor(LST_end_hrs))*60))]
print(f"LST: [{LST_start[0]-24}:{LST_start[1]}; {LST_end[0]}:{LST_end[1]}] for observation night (7.-)8.3.2023")

# 4. OJ248 = B0827+243  = OJ 248
# 11. PKS1510-089 = B1510-089 = PKS 1510-089
target = "PKS1510-089 = B1510-089"
RA = [15, 10, 0.0]  # (h, min, sec)
dec = -8.9           # deg
lat = mhovi_lat
a_min = 20

print(f"\nDoes the source {target} rise above {a_min}deg?")
dec_lat = dec + lat
print(f"Dec+lat={dec_lat}, circumpolar {dec_lat > 90}")
dec_over_lat = dec < lat
if dec_over_lat:
    print("Culminates South of zenith")
    a_max = 90 - lat + dec
else:
    print("Culminates North of zenith")
    a_max = 90 + lat - dec

observable = a_max > a_min
print(f"a_max = {a_max}deg, > {a_min}deg --> observable: {observable}")  # where dis %.2f

if not observable:
    print("Not observable!")
    exit

# when does it culminate?
LST_culminate_hrs = RA[0] + RA[1] / 60.0
local_solar_time = (LST_culminate_hrs - (-13) * 4 - 12 * 60 - mhovi_corr) / 60
print(f"Culmination at LST={RA} and local time {local_solar_time}")
deg_conv = np.pi/180.0
cos_h = (-1.0) * np.tan(dec*deg_conv) * np.tan(lat*deg_conv) + np.sin(a_min*deg_conv) / (np.cos(dec*deg_conv) * np.cos(lat*deg_conv))
#print(cos_h)
h = np.arccos(cos_h)
print(f"h = +/-{h} deg")
h_hrs = h / (2*np.pi) * 24
LST_rise_to_a_min = LST_culminate_hrs - h_hrs
LST_sets_to_a_min = LST_culminate_hrs + h_hrs
print(f"LST_rise = {LST_rise_to_a_min}")
print(f"LST_set  = {LST_sets_to_a_min}")

