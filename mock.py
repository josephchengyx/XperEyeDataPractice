

on_off_times = {'On1':1671833457622655, 'Off1':1671833462622910, 'On2':1671833464623207, 'Off2':1671833469623398,'On3':1671833471623668,
                'taskdone1': 1671833462623222, 'taskdone2': 1671833469623648, 'taskdone3':1671833476624234,
                'eyeDevice1': 1671833456788838, 'EyeDevice2': 1671833456793412, 'EyeDeviceLast':1671833461497601}

sorted_times = sorted(on_off_times.items(), key=lambda x:x[1])
print(sorted_times)