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

class test_suit_system_sanity_music(TestSuitBase):
    '''
    test_suit_ui_message is a class for music suit.

    @see: L{TestSuitBase <TestSuitBase>}
    '''
    pass

    
def click_songtab(tabname=''):
    click(90,150)
    sleep(2)
    click_textview_by_text(tabname)
    sleep(3)
    if wait_for_fun(lambda:search_view_by_id('search'),True,5):
        case_flag=True
    if search_text("has stopped|Unfortunately|isn't responding", searchFlag=TEXT_MATCHES_REGEX):
        take_screenshot()
        click_textview_by_text('OK|Close', searchFlag=TEXT_MATCHES_REGEX)
        return False
    else:
        return True
 
    

    
    

    

