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
import logging_wrapper


class test_suit_system_sanity_settings_case01(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch settings
    Step2:set sim1 and sim2 enable and disable
    Verification: 
    ER1:can enable and disable normal
    
    '''
    

    
    def test_case_main(self, case_results):
        
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        result=[]
        TAG = "enable and disable sim1 and sim2 normally: Settings "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity('com.android.settings','com.android.settings.Settings')             
        if wait_for_fun(lambda:search_text('WLAN'), True, 5) or wait_for_fun(lambda:search_text('Bluetooth'), True, 5):
            log_test_framework(self.name, "Launch settings pass")
            if search_text('SIM cards',isScrollable=1):
                click_textview_by_text('SIM cards')
                sleep(1)
                result.append(enableSIM1('Disable'))
                sleep(2)
                result.append(enableSIM1('Enable'))
                sleep(2)
                result.append(enableSIM1('Disable'))
                sleep(2)
                result.append(enableSIM1('Enable'))
                sleep(2)
                result.append(enableSIM2('Disable'))
                sleep(2)
                result.append(enableSIM2('Enable'))
                sleep(2)
                result.append(enableSIM2('Disable'))
                sleep(2)
                result.append(enableSIM2('Enable'))
                sleep(2)
                case_flag=not False in result
        if search_text("stopped", searchFlag=TEXT_CONTAINS):
            log_test_framework(self.name, "Popup has stopped")
            take_screenshot()
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
        elif search_text("Unfortunately",searchFlag=TEXT_CONTAINS):
            take_screenshot()
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
                
        elif search_text("isn't responding",searchFlag=TEXT_CONTAINS):
            take_screenshot()
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
            
  
