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




class test_suit_system_sanity_sensor_case1(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch settings
    Step2:close auto rotation
    Verification: 
    ER1:can close auto rotation
    
    '''
    
    
    def test_case_main(self, case_results):
        
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        TAG = "close auto orientation: Sensor "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity('com.android.settings','com.android.settings.Settings')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            phone.permission_allow()   
           
        case_flag=self.close_auto_rotate() 
        if search_text('has stopped',searchFlag=TEXT_CONTAINS):
            log_test_framework(self.name, "Popup has stopped")
            case_flag=False
            take_screenshot()
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2) 
        elif search_text("Unfortunately",searchFlag=TEXT_CONTAINS):
            take_screenshot()
            case_flag=False
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
                
        elif search_text("isn't responding",searchFlag=TEXT_CONTAINS):
            take_screenshot()
            case_flag=False
            if search_text("OK"):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close"):
                click_button_by_text("Close")
                sleep(2)
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")
            
                       
        for i in range(3):
            send_key(KEY_BACK)
            sleep(1)
        send_key(KEY_HOME)
       
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
            
    def close_auto_rotate(self):
        if search_text('Display',isScrollable=1,searchFlag=TEXT_MATCHES_REGEX):
            click_textview_by_text('Display')
            sleep(2)
            if search_text('rotated',isScrollable=1, searchFlag=TEXT_CONTAINS):
                click_textview_by_text('rotated', searchFlag=TEXT_CONTAINS)
                sleep(2)
                if wait_for_fun(lambda:search_text('Stay in current orientation'),True,5):
                    click_textview_by_text('Stay in current orientation')
                    sleep(2)
                    case_flag=True
                else:
                    take_screenshot()
            else:
                take_screenshot()
                case_flag=False
        else:
            take_screenshot()
            case_flag=False
        return case_flag

