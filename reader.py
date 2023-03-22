import csv

with open("observables.csv", newline='') as savefile:
    saved_session = csv.reader(savefile, delimiter=',')  # , quotechar='|')
    print(saved_session)
    for row in saved_session:
        print('--'.join(row))
        target = row[0]
        bname  = row[1]
        RA_hrs = float(row[2]) + float(row[3]) / 60.0 + float(row[4]) / 3600.0
        dec_degs = float(row[5]) + float(row[6]) * 0.0167 
        print(f"RA={RA_hrs},  dec={dec_degs}")