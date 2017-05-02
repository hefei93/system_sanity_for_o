#coding=utf-8
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



class test_suit_system_sanity_camera2_case02(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch gallary;
    Step2:tap camera icon into camera
    Step3: take photo  
    Verification: 
    ER2: can save picture;   
    '''
    
    
    def test_case_main(self, case_results):
        
        
        global case_flag , TAG, testresult, success_flag, i, success_time, auto_flag, on_flag, off_flag
        case_flag = True
        testresult = []
        success_time = 0
        fail_time = 0
        iterationNum = 100
        TAG = "Dev-ci cases: Camera "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
                    
        start_activity('org.codeaurora.gallery','com.android.gallery3d.app.GalleryActivity')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            phone.permission_allow()
        case_flag=self.gallary_into_camera()
        case_flag=self.take_photo()
        if search_text("isn't responding", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")            
            take_screenshot()
            case_flag=False
            if search_text("Close app", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
                sleep(2)
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
        elif search_text("Unfortunately", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs crash")
            take_screenshot()
            case_flag=False
            if search_text("OK", searchFlag=TEXT_CONTAINS):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
        elif search_text("stopped", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup has stopped")
            take_screenshot()
            case_flag=False
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
            if search_text("OK", searchFlag=TEXT_CONTAINS):
                click_button_by_text("OK")
                sleep(2)       
        elif search_text("Close app", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup Close app error")
            take_screenshot()        
            case_flag=False    
            click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
            sleep(2)        
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
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case pass')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tpass')
        else:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case fail')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tfail')
            save_fail_log()
 
    def gallary_into_camera(self):
        if wait_for_fun(lambda:search_view_by_id('id/action_camera'),True,5):
            click_textview_by_id('id/action_camera')
            if wait_for_fun(lambda:search_view_by_id('id/shutter_button'),True,6):
                log_test_framework(self.name, 'from gallary into camera pass')
                case_flag=True
            else:
                log_test_framework(self.name,'from gallary into camera fail')
                take_screenshot()
                case_flag=False
        else:
            log_test_framework(self.name, 'can not find action camera from gallary')
            take_screenshot()
            case_flag=False
        return case_flag
            
    def take_photo(self):
        if wait_for_fun(lambda:search_view_by_id('id/shutter_button'),True,5):
            click_textview_by_id('id/shutter_button')
            sleep(2)
            case_flag=True
        else:
            log_test_framework(self.name, 'take photo fail')
            take_screenshot()
            case_flag=False
        return case_flag
        

    
  