# coding=utf-8
'''
@author: hu_ch
for android N
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line,\
    log_test_framework
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_system_sanity_browser import *
from urlparse import clear_cache
from test_suit_system_sanity_browser import *

class test_suit_system_sanity_browser_case02(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch browser
    Step2:open sina
    Step3:download image or link
    Step4:open download file
    Verification: 
    ER1:can open download file no crash
    
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG  ,p
        case_flag = False
        TAG = 'download file: Browser '
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR],  self.name +' : case Start')
        log_test_framework(TAG, self.name + " -Start")
        recordName=''.join(__name__.split('_')[-2:])
        

        start_activity("com.android.browser", "org.chromium.chrome.browser.ChromeTabbedActivity")
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 15):
            phone.permission_allow()
        if wait_for_fun(lambda:search_view_by_id('terms_accept'), True, 15):            
            click_button_by_id('terms_accept')
            if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                click_button_by_id('next_button')
                if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                    click_button_by_id('next_button')
                    if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                        click_button_by_id('next_button')  
        browser.browser_downloadQQ(True)
        openNotification()
        sleep(4)
        if search_text('Download complete',isScrollable=0):
            log_test_framework(self.name,'download successful')
            click_textview_by_text('Download complete')
            sleep(2)
            if not search_text('has stopped',isScrollable=0,searchFlag=TEXT_CONTAINS):
                log_test_framework("system_sanity_browser_case2:", "download file open pass")
                take_screenshot()
                case_flag=True
            else:
                take_screenshot()
        else:
            take_screenshot()
            case_flag=False
            log_test_framework(self.name, 'download file fail')
            
            
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_HOME)
        sleep(1)
        
        if search_text('has stopped',isScrollable=0,searchFlag=TEXT_CONTAINS):
            log_test_framework("system_sanity_browser_case2:", "Popup has stopped")
            take_screenshot()
            sleep(2)
            send_key(KEY_BACK)
            case_flag=False

        if case_flag:
            qsst_log_case_status(STATUS_SUCCESS, "" , SEVERITY_HIGH)
        else:
            qsst_log_case_status(STATUS_FAILED, "", SEVERITY_HIGH)
        
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], case_flag))
        
    
    
    def test_case_end(self):
        '''
        record the case result
        '''
        '''
        @attention: modify by min.sheng
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
        
                

            
