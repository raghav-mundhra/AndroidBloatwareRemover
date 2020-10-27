import tkinter as tk
import os
import subprocess
import json
import pickle
from tkinter import ttk
from tkinter import messagebox as mb

device_id = ''

package_lables_dict = {}
window = tk.Tk() 
window.title('Android Bloatware Remover') 
window.geometry('500x350') 

# Combobox creation 
cbox_devices_connected = ttk.Combobox(window, state="readonly", width = 27) 

lbl_device_name = tk.Label(window, text='')

lbl_1 = tk.Label(window, text = "Select the Device :")

Lb1 = tk.Listbox(window, width=50)

def set_device_id():
    global device_id
    device_id = cbox_devices_connected.get()
    get_device_name()
    add_aapt_file(device_id)
    get_installed_packages()

def get_connected_devices():
    # Getting list of devices connected
    device_list = subprocess.run(r'adb\adb devices', capture_output=True).stdout.decode('utf-8').split('\r\n')[1:]
    device_list = [i.replace('\tdevice', '') for i in device_list]
    device_list = list(filter(None, device_list))
    return device_list

def get_device_name():
    device_details = subprocess.run(r'adb\adb -s ' + device_id + ' shell getprop | grep "model"', capture_output=True)
    device_info = device_details.stdout.decode('utf-8').replace('[', '').replace(']', '').replace('\n', ', ').replace('\r', '')
    info_list = device_info.split(',')
    info_list.remove(' ')
    device_name = dict([i.strip().split(':') for i in info_list])['ro.product.model']
    lbl_device_name['text'] = device_name

def add_aapt_file(device_id):
    try:
        subprocess.run(r'adb\adb -s ' + device_id + ' push aapt-arm-pie /data/local/tmp')
        subprocess.run(r'adb\adb -s ' + device_id + ' shell chmod 0755 /data/local/tmp/aapt-arm-pie')
    except:
        pass

def fetch_app_name_from_device(package_name):
    try:
        apk_path = subprocess.run(r'adb\adb -s ' + device_id + ' shell pm list packages -f '+package_name+' ', capture_output=True)
        apk_path = apk_path.stdout.decode('utf-8').split('='+package_name)[0].replace('package:', '')
        app_name = subprocess.run(r'adb\adb -s ' + device_id + ' shell "/data/local/tmp/aapt-arm-pie dump badging '+ apk_path +' | grep application-label"', capture_output=True)
        app_name = app_name.stdout.decode('utf-8').replace('\n', ', ').replace('\r', '').replace("'", "")
        app_name_list = app_name.split(',')
        try:
            app_name_list.remove(' ')
        except:
            app_name_list.remove('')
        app_name = dict([i.split(':') for i in app_name_list])
        return app_name['application-label']
    except:
        return package_name

def get_lable_for_app(package_name):
    try:
        with open("package_names.pickle", 'rb') as handle:
            packages_with_names = pickle.load(handle)
        if package_name in packages_with_names:
            return packages_with_names[package_name]
        else:
            return fetch_app_name_from_device(package_name)
    except:
        return fetch_app_name_from_device(package_name)

def save_app_lables(package_lables_dict):
    with open("package_names.pickle", 'rb') as handle:
        packages_with_names = pickle.load(handle)
    
    for i, j in package_lables_dict.items():
        if i not in packages_with_names:
            packages_with_names[i] = j
    
    with open('package_names.pickle', 'wb') as handle:
        pickle.dump(packages_with_names, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_installed_packages():
    Lb1.grid(column = 0, row = 8, columnspan=4, padx=10, pady=10, ipadx=5, ipady=5)
    Lb1.delete(0, tk.END)
    Lb1.insert(tk.END, 'Please wait while loading installed apps...')
    global package_lables_dict
    list_of_packages_installed = subprocess.run(r'adb\adb -s ' + device_id + ' shell "pm list packages -f" | sed -e "s/.*=//" | sort', capture_output=True)
    list_of_packages_installed = list_of_packages_installed.stdout.decode('utf-8').replace('\r', '').split('\n')
    try:
        list_of_packages_installed.remove('')
    except:
        pass
    if 'android' in list_of_packages_installed:
        list_of_packages_installed.remove('android')

    package_lables_dict = {}
    for i in list_of_packages_installed:
        package_lables_dict[i] = get_lable_for_app(i)

    save_app_lables(package_lables_dict)

    Lb1.delete(0, tk.END)
    package_lables_dict = {k: v for k, v in sorted(package_lables_dict.items(), key=lambda item: item[1])}
    for i,j in package_lables_dict.items():
        Lb1.insert(tk.END, str(j)+str('  :  ')+str(i))

    tk.Button(window, text='Uninstall', command=get_package_name_from_listbox).grid(column = 0, 
          row = 9, padx = 10, pady = 5)

def get_package_name_from_listbox():
    index_of_selection = Lb1.curselection()
    confirmation_popup(list(package_lables_dict.items())[index_of_selection[0]])
  
def confirmation_popup(package):
    app_lable = package[1]
    package_name = package[0]
    res=mb.askquestion('Uninstall', 'Do you really want to uninstall the app "'+ app_lable + ' (' + package_name + ') ' + '?"')
    if res == 'yes' :
        uninstall_app(package_name, app_lable)
    else :
        mb.showinfo('Return', 'Returning to main application')

def uninstall_app(package_name, app_lable):
    uninstall_app = subprocess.run(r'adb\adb -s ' + device_id + ' shell pm uninstall -k --user 0 '+ package_name + ' ', capture_output=True)
    uninstall_app.stdout.decode('utf-8')
    uninstall_status = uninstall_app.stdout.decode('utf-8').replace('\r', '').replace('\n', '')
    if uninstall_status == 'Success':
        mb.showinfo('App Uninstalled', 'App "' + app_lable + ' (' + package_name + ') ' + '" uninstalled!')
        get_installed_packages()
    else:
        mb.showinfo('Error!', 'Error uninstalling package!')

if __name__ == '__main__': 

    # Adding combobox drop down list
    device_list = get_connected_devices()
    if len(device_list) == 0:
        lbl_selected_device = tk.Label(text = 'No device connected. Please restart the applications after connecting a device!') 
        lbl_selected_device.grid(column=0, row=6, padx=20)
        window.mainloop() 
        exit()

    lbl_1.grid(column = 0, row = 5)
    cbox_devices_connected['values'] = (device_list)
    
    cbox_devices_connected.grid(column = 1, row = 5) 
    cbox_devices_connected.current(0)

    tk.Button(window, text='Select', command=set_device_id).grid(column = 3, 
            row = 5, padx = 10, pady = 5)

    lbl_selected_device = tk.Label(text = 'Selected Device: ') 
    lbl_selected_device.grid(column=0, row=6, padx=20)

    lbl_device_name.grid(column = 1, row=6)

    window.mainloop() 