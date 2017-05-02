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
from logging_wrapper import log_test_framework
import re


CASE_PLUG_IN_FUNCTION_NAME = 'case_plug_in'
test_suit_config_map = {}
global_suit_config_map = {}
BOOL_STK_WIFI_CHECK = False
BOOL_STK_MOBILE_NETWORK_CHECK = False

class test_suit_system_sanity_settings(TestSuitBase):
    '''
    test_suit_ui_message is a class for setting suit.

    @see: L{TestSuitBase <TestSuitBase>}
    '''
    pass


def enableSIM1(clickType='Enable'):
    text1=text2=get_view_text_by_index(VIEW_BUTTON, 0)
    log_test_framework("current button is ",text1)
    if clickType=='Enable':
        if text1=='OFF':
            click_button_by_id('id/sub_switch_widget')
            sleep(15)
            if search_view_by_id('android:id/button3'):
                click_button_by_id('android:id/button3')
                sleep(5) 
        return True
    elif clickType=='Disable':
        if text1=='ON':
            click_button_by_id('sub_switch_widget')
            sleep(2)
            if search_text('Deactivating the SIM',isScrollable=0):
                click_button_by_id('android:id/button1')
                sleep(20)
                if search_view_by_id('android:id/button3'):
                    click_button_by_id('android:id/button3')
                    sleep(5)
        return True
    else:
        take_screenshot()
        log_test_framework('type error','')
        
        
def enableSIM2(clickType='Enable'):
    text2=get_view_text_by_index(VIEW_BUTTON, 1)
    log_test_framework("current button is ",text2)      
    if clickType=='Enable':
        if text2=='OFF':
            click_button_by_index(1)
            sleep(15)
            if search_view_by_id('android:id/button3'):
                click_button_by_id('android:id/button3')
                sleep(5) 
        return True
    elif clickType=='Disable':
        if text2=='ON':
            click_button_by_index(1)
            sleep(2)
            if search_text('Deactivating the SIM',isScrollable=0):
                click_button_by_id('android:id/button1')
                sleep(20)
                if search_view_by_id('android:id/button3'):
                    click_button_by_id('android:id/button3')
                    sleep(5)
        return True
    else:
        take_screenshot()
        log_test_framework('type error','')
        
def networkReset(setSIM='SIM1'):
    wait_for_fun(lambda:search_view_by_id('reset_network_subscription'),True,5)
    click_textview_by_id('reset_network_subscription')
    sleep(1)
    if setSIM=='SIM1':
        click_in_list_by_index(0)   #click sim1
    elif setSIM=='SIM2':
        click_in_list_by_index(1)   #click sim2
    sleep(2)
    click_textview_by_text('RESET SETTINGS')
    sleep(2)
    if wait_for_fun(lambda:search_view_by_id('execute_reset_network'),True,5):
        click_button_by_id('execute_reset_network')
        sleep(2)
        send_key(KEY_BACK)
        sleep(1)
        return True
    else:
        take_screenshot()
        return False

    
def openNotification():
    x=getDisplayWidth()
    y=getDisplayHeight()
    os.system('adb shell input swipe %s 0 %s %s 1000'%((int(x)/2),(int(x)/2),(int(y)/2)))
    sleep(2)
    
def quickData():
    if not search_text('Airplane mode',isScrollable=0) and search_view_by_id('expand_indicator'):
        click_textview_by_id('expand_indicator')
        sleep(1)
        click_imageview_by_index(5)   #click data switch
        return True
    else:
        take_screenshot()
        return False
  
def switchData(switch='ON'):
    sleep(2)
    text2=get_view_text_by_id(VIEW_BUTTON,'android:id/toggle',isScrollable=0)
    log_test_framework("current button is ",text2)      
    if switch=='ON':
        if text2=='OFF':
            click_textview_by_id('android:id/toggle')
            sleep(2)
            text3=get_view_text_by_id(VIEW_BUTTON,'android:id/toggle',isScrollable=0)
            if text3=='OFF':
                take_screenshot()
                log_test_framework("click data switch still ", text3)
                return False
        return True
    elif switch=='OFF':
        if text2=='ON':
            click_textview_by_id('android:id/toggle')
            sleep(2)
            text4=get_view_text_by_id(VIEW_BUTTON,'android:id/toggle',isScrollable=0)
            if text4=='ON':
                take_screenshot()
                log_test_framework("click data switch still ", text3)
                return False
        return True
    else:
        take_screenshot()
        log_test_framework('type error','')   
    
def setCellularDataLimit(datalimit=1,setLimit="True"):
    search_text("Data usage")
    click_textview_by_text("Data usage")
    if wait_for_fun(lambda:search_text("Cellular data usage"), True, 3):
        txt1=get_view_text_by_id(VIEW_TEXT_VIEW,"android:id/title")
        dataUsage=re.match(r'([\d]+)',txt1).group(1)
        click_textview_by_text("Cellular data usage")
        if wait_for_fun(lambda:search_view_by_id("filter_settings"), True, 3):
            click_imageview_by_id("filter_settings")
            wait_for_fun(lambda:search_text("Data limit"),True,6)
            click_textview_by_text("Data limit")
            sleep(2)
            if not wait_for_fun(lambda:search_view_by_id("size_spinner"),True,5):
                click_textview_by_text("Set data limit")
                sleep(4)
                if search_view_by_id("android:id/button1"):
                    click_textview_by_id("android:id/button1")
                    sleep(3)
                    click_textview_by_text("Data limit")
                    sleep(4)
            click_textview_by_id("size_spinner")
            sleep(5)
            click_textview_by_text("MB")
            sleep(2)
            entertext_edittext_by_id("bytes",str(datalimit+int(dataUsage)))
            click_button_by_id("android:id/button1")
            return True
 
    
    

    
    

    

