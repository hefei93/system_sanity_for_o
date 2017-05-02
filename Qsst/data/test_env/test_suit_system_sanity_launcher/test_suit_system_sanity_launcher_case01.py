'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from qrd_shared.mms.Mms import *
from idlelib.idle_test.test_searchengine import SearchTest


class test_suit_system_sanity_launcher_case01(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:press home
    Step2:press menu
    Step3:set wallpaper is picture 2
    Verification: 
    can set wallpaper successfully
    
    '''
    
    
    def test_case_main(self, case_results):
        
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        TAG = "Dev-ci cases: Settings "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
       
        send_key(KEY_HOME)
        sleep(1)
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        send_key(KEY_MENU)
        sleep(5)
        wait_for_fun(lambda:search_text("WALLPAPERS"),True,5)
        click_textview_by_text("WALLPAPERS")
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            click_button_by_id('permission_allow_button',isScrollable=0)
            sleep(5)
            send_key(KEY_BACK)
            wait_for_fun(lambda:search_text("WALLPAPERS"),True,5)
            click_textview_by_text("WALLPAPERS")
        if wait_for_fun(lambda:search_text("Set wallpaper",isScrollable=0),True,10):
            sleep(2)
            x=getDisplayWidth()
            y=getDisplayHeight()
            #click(int(x)*3/4, int(y)-100)
            click_imageview_by_index(2)
            sleep(5)
            click_textview_by_text("Set wallpaper")
            sleep(2)
            case_flag=True
        if search_text('has stopped',searchFlag=TEXT_CONTAINS,isScrollable=0):
            log_test_framework("gp_sanity_settings_case01:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2) 
            case_flag=False
        elif search_text("not responding",searchFlag=TEXT_CONTAINS,isScrollable=0):
            take_screenshot()
            sleep(5)
            click_textview_by_text("OK")
            case_flag=False
            log_test_framework("gp_sanity_settings_case01:", "ANR")
        
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_HOME)
        sleep(1)        

        if case_flag:
            qsst_log_case_status(STATUS_SUCCESS, "" , SEVERITY_HIGH)
        else:
            qsst_log_case_status(STATUS_FAILED, "", SEVERITY_HIGH)
        
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], case_flag))
        
        
    def test_case_end(self):
        '''
        record the case result

        '''
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : end')
        if can_continue() and case_flag == True:
            # shutdown()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ': case pass')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tpass')
        else:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case fail')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tfail')
            save_fail_log()
        p.terminate() 
