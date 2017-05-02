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



class test_suit_system_sanity_settings_case03(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:open quick settings
    Step2:enable/disable data switch
    Verification: 
    ER1:can enable/disable switch normally
    
    '''
    

    def test_case_main(self, case_results):
        
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        result=[]
        TAG = "data switch in quick settings: Settings "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        openNotification()
        quickData()
        result.append(switchData('OFF'))
        sleep(5)
        result.append(switchData('ON'))
        sleep(5)
        result.append(switchData('OFF'))
        sleep(5)
        result.append(switchData('ON'))
        log_test_framework(self.name, str(result))
        case_flag=not False in result
        send_key(KEY_BACK)
        send_key(KEY_BACK)
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
  
