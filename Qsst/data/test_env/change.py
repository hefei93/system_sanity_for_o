import os 
import re
import time



def change_folder_name():
    folders = os.listdir(os.getcwd())
    for item in folders:
        if "test_suit_cmcc_devci" in item:
            oldname = os.path.join(os.getcwd(),item)
            newname = oldname.replace("test_suit_cmcc_devci", "test_suit_gp_sanity")
            print os.rename(oldname, newname);
    time.sleep(2)
    folders_new = os.listdir(os.getcwd())
    for item_new in folders_new:        
        if "test_suit_gp_sanity" in item_new:
            files = os.listdir(os.path.join(os.getcwd(),item_new))
            for file in files:
                if "test_suit_cmcc_devci" in file:
                    oldname =os.path.join(os.path.join(os.getcwd(),item_new),file)
                    print oldname
                    newname = oldname.replace("test_suit_cmcc_devci","test_suit_gp_sanity")
                    print newname
                    print os.rename(oldname,newname)

            
def change_content():
    for root, dirs, files in os.walk(os.getcwd()):
        for item in files:
            if "test_suit_gp_sanity_" in item: 
                path = os.path.join(root,item)
                print path
                f =  open(path,'r+')        
                s= f.read()
                f.seek(0,0)
                f.write(s.replace("cmcc_devci_", "gp_sanity_"))
                f.close
 
#change_folder_name()
#time.sleep(5)
change_content()
                            