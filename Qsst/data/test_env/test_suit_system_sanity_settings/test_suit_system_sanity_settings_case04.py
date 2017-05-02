# coding=utf-8
'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_system_sanity_settings import *
from urlparse import clear_cache





class test_suit_system_sanity_settings_case04(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}

    Procedure:
    Step1:Open Settings ->Data usage -> Enable "Set cellular data limit"
    Step2:Set warning line and limits; (eg: usedM)
    Step3:go to browser Visit website 
    Verification: 
    ER1:can viset website successfully
    '''
    

    def test_case_main(self, case_results):
        
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False

        TAG = "data switch in quick settings: Settings "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity('com.android.settings','com.android.settings.Settings')
        search_text("WLAN")
        click_textview_by_text("WLAN")
        settings.disable_wlan()
        send_key(KEY_BACK)
        setCellularDataLimit(1)
        send_key(KEY_HOME)
        sleep(10)
        browser.browser_downloadQQ()
        if wait_for_fun(lambda:search_text("Cellular data is paused",isScrollable=0),True,10):
            click_button_by_id("android:id/button1")
            case_flag=True
        start_activity('com.android.settings','com.android.settings.Settings')
        setCellularDataLimit(3000)
        send_key(KEY_BACK)
        send_key(KEY_HOME)
        sleep(10)
        if search_text("stopped", searchFlag=TEXT_CONTAINS):
            log_test_framework(self.name, "Popup has stopped")
            case_flag=False
            take_screenshot()
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
        elif search_text("Unfortunately", searchFlag=TEXT_CONTAINS):
            take_screenshot()
            case_flag=False
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
                
        elif search_text("isn't responding", searchFlag=TEXT_CONTAINS):
            take_screenshot()
            case_flag=False
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")
    
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
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : end')
        if can_continue() and case_flag == True:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ': case pass')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tpass')
        else:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case fail')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tfail')
            save_fail_log()

            
  
