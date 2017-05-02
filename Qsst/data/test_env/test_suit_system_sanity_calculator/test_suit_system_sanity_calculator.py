# -*- coding: utf-8 -*-  
'''

@author: huitingn
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

class test_suit_system_sanity_calculator(TestSuitBase):
    '''
    test_suit_ui_message is a class for calculator suit.

    @see: L{TestSuitBase <TestSuitBase>}
    '''
    pass


def add():
    if wait_for_fun(lambda:search_view_by_id('op_add'),True,5):
        click_button_by_id('op_add')
        return True
    take_screenshot()
    return False

def jian():
    if wait_for_fun(lambda:search_view_by_id('op_sub'),True,5):
        click_button_by_id('op_sub')
        return True
    take_screenshot()
    return False

def chen():
    if wait_for_fun(lambda:search_view_by_id('op_mul'),True,5):
        click_button_by_id('op_mul')
        return True
    take_screenshot()
    return False

def chu():
    if wait_for_fun(lambda:search_view_by_id('op_div'),True,5):
        click_button_by_id('op_div')
        return True
    take_screenshot()
    return False

dict={'jia':add,'jian':jian,'chen':chen,'chu':chu}
def operator(x,fun,y,expeted='3'):
    if search_view_by_id('clr'):
        click_textview_by_id('clr')
    click_textview_by_text(x)
    sleep(1)
    fun()
    click_textview_by_text(y)
    sleep(1)
    click_textview_by_id('eq')
    sleep(1)
    result=get_view_text_by_id(VIEW_TEXT_VIEW, 'result')
    if result==expeted:
        return True
    take_screenshot()
    return False
    
    


    

    
    
    

    
    

    

