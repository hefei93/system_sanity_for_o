# -*- coding: utf-8 -*-  
'''

@author: hu_ch
@version:

'''
from utility_wrapper import *
import fs_wrapper
from test_suit_base import TestSuitBase
from case_utility import *
import re, datetime, shlex
from qrd_shared.case import *


CASE_PLUG_IN_FUNCTION_NAME = 'case_plug_in'
test_suit_config_map = {}
global_suit_config_map = {}
BOOL_STK_WIFI_CHECK = False
BOOL_STK_MOBILE_NETWORK_CHECK = False

class test_suit_system_sanity_camera(TestSuitBase):
    '''
    test_suit_ui_message is a class for browser suit.

    @see: L{TestSuitBase <TestSuitBase>}
    '''
    pass

   
   
def recording_video(recordtime=5):
    if switchCR('Record'):
        click_textview_by_id('id/shutter_button')
        sleep(recordtime)
        click_textview_by_id('id/shutter_button')
        sleep(2)
        return True
    else:
        return False
  
#take photo  
def takePhoto(count=1):
    if switchCR('Picture'):
        for num in range(count):
            click_textview_by_id('id/shutter_button')
            sleep(8)
        return True
    else:
        return False

#switch to picture or recorde mode
def switchCR(mode='Picture'):
    if wait_for_fun(lambda:search_view_by_id('id/camera_switcher'),True,5):
        click_textview_by_id('id/camera_switcher')
        sleep(2)
        x=getDisplayWidth()
        y=getDisplayHeight()
        if mode=='Picture':
            click(int(x)-100,int(y)-200)
            if wait_for_fun(lambda:search_view_by_id('id/filter_mode_switcher'),True,5) and search_view_by_id('id/scene_mode_switcher'):
                return True
        elif mode=='Record':
            click(int(x)-100,int(y)-300)
            if wait_for_fun(lambda:search_view_by_id('id/filter_mode_switcher'),True,5) and search_view_by_id('id/scene_mode_switcher'):
                return True
        else:
            return False
    else:
        take_screenshot()
        return False
    
def setCountDown(types='10 seconds'):
    if switchCR('Picture'):
        wait_for_fun(lambda:search_view_by_id('menu'),True,5)
        click_button_by_id('menu')
        sleep(2)
        if wait_for_fun(lambda:search_text('Countdown timer',isScrollable=0),True,5):
            click_textview_by_text('Countdown timer')
            sleep(5)
            click_button_by_id('text')
            #click_textview_by_text(types)
            sleep(2)
            return True
    else:
        take_screenshot()
        return False
    
#set picture quality is (Low/Standard/High)
def setPictureQuality(type='Low'):
    if wait_for_fun(lambda:search_view_by_id("menu"),True,5):
        click_textview_by_id("menu")
        if wait_for_fun(lambda:search_text("Picture quality",isScrollable=0),True,5):
            click_textview_by_text("Picture quality")
            if type=='Low':
                click_textview_by_index(28)  
            if type=='Standard':
                click_textview_by_index(29)
            if type=='High':
                click_textview_by_index(30)
    

#get picture file size
def getPictureSize():
    if wait_for_fun(lambda:search_view_by_id('preview_thumb'), True, 5):
        click_imageview_by_id("preview_thumb")
        if wait_for_fun(lambda:search_view_by_id("photopage_bottom_control_delete"), True, 5):
            click_imageview_by_index(1) 
            if wait_for_fun(lambda:search_text("Details",isScrollable=0), True,5):
                click_textview_by_text("Details") 
                sleep(5) 
                tx1=get_view_text_by_index(VIEW_TEXT_VIEW,6)
                if "MB" in tx1:
                    txt2=re.findall(r"\d.\d\d",tx1)
                    txt3=''.join(txt2)
                    print float(txt3)*1000
                    send_key(KEY_BACK)
                    send_key(KEY_BACK)
                    return float(txt3)*1000
                else:
                    txt1=re.findall(r"\d{3,4}",tx1)
                    txt4=''.join(txt1)
                    print float(txt4)
                    send_key(KEY_BACK)
                    send_key(KEY_BACK)
                    return float(txt4)

#get size of Camera folder  
def getCameraCount():
    f=os.popen('adb shell df /sdcard/DCIM/Camera/')
    aviable=f.readlines()[1].split('%')[0].split('  ')[-2].strip()
    print float(aviable)
    return float(aviable)

#random set HDR is enable or disable and take picture
from random import randint
def setHDR():
    if wait_for_fun(lambda:search_view_by_id("scene_mode_switcher"),True,5):
        click_textview_by_id("scene_mode_switcher")
        sleep(2)
        isHDR=randint(1,10)
        if isHDR<randint(6,10):
            click_textview_by_text("Automatic")
            log_test_framework("HDR mode is ", "auto")
        else:
            log_test_framework("HDR mode is ", "HDR")
            click_textview_by_text("HDR")
        sleep(3)
        if wait_for_fun(lambda:search_view_by_id('id/shutter_button'),True,5):
            click_textview_by_id('id/shutter_button')
            sleep(8)
            return True
        
#recorder settings
def setRecord(cmsettings='First'):
    t1=['Flash','Video quality','Video duration','GPS location','White balance','Video High FrameRate','Image Stabilization']
    #set secend option
    t2=[17,17,17,17,17,17,17]
    #set first option
    t3=[16,16,16,16,16,16,16]
    for i in range(len(t1)):
        if wait_for_fun(lambda:search_view_by_id('menu'),True,5):
            click_textview_by_id('menu')
            sleep(1)
            if wait_for_fun(lambda:search_text(t1[i], isScrollable=0),True,5):
                click_textview_by_text(t1[i])
                sleep(3)
                if cmsettings=='First':
                    click_textview_by_index(t3[i])
                    sleep(3)
                elif cmsettings=='Second':
                    click_textview_by_index(t2[i])
                    sleep(3)

                                 


    