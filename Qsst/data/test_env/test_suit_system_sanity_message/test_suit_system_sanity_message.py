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

class test_suit_system_sanity_message(TestSuitBase):
    '''
    test_suit_ui_message is a class for browser suit.

    @see: L{TestSuitBase <TestSuitBase>}
    '''
    pass

    
def deleteAllMessage():
    # delete all notification
    if wait_for_fun(lambda:search_view_by_id("notification_icon"),True,5):
        click_textview_by_id("notification_icon")
        sleep(3)
        click_textview_by_id("subject",clickType=LONG_CLICK)
        deleteMessage()
        send_key(KEY_BACK)
    if wait_for_fun(lambda:search_view_by_id("avatar"),True,5):
        click_textview_by_id("from", clickType=LONG_CLICK)
        sleep(3)
        deleteMessage()
    if wait_for_fun(lambda:search_text("No conversations."), True,6):
        return True


    
def deleteMessage():
    wait_for_fun(lambda:search_view_by_id("selection_menu"),True,5)
    click_textview_by_id("selection_menu")
    if search_text("Select all", isScrollable=0):
        click_textview_by_text("Select all")
    elif search_text("Deselect all", isScrollable=0):
        click_textview_by_text("selected",searchFlag=TEXT_CONTAINS)
        sleep(3)
    else:
        take_screenshot()
    x=int(getDisplayWidth())
    y=int(getDisplayHeight())
    click(x-30,150)
    sleep(3)
    if wait_for_fun(lambda:search_view_by_id("android:id/button1"),True,8):
        click_textview_by_id("android:id/button1")
        sleep(20)
        return True
    

