'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *







class test_suit_system_sanity_filemanager_case5(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch filemanager
    Step2:into internel storage
    Step3:check disk usage
    Verification: 
    ER1:disk usage show total,used and free
    '''
    
    
    def test_case_main(self, case_results):
        
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        TAG = "internal disk usage: Filemanager "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        
        start_activity('com.cyanogenmod.filemanager','com.cyanogenmod.filemanager.activities.NavigationActivity')
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            phone.permission_allow()
        click(94, 158)  #click top left to find internal storage
        if wait_for_fun(lambda:search_text('Internal shared storage'), True, 5):
            click_textview_by_text('Internal shared storage',searchFlag=TEXT_MATCHES)
            sleep(3)
            log_test_framework(self.name,"into internal storage pass")
        else:
            log_test_framework("file manager has no internal storage option", self.name + " ERROR")  
        case_flag=self.check_internal_usage()  
        for i in range(3):
            send_key(KEY_BACK)
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
    def check_internal_usage(self):
        if wait_for_fun(lambda:search_view_by_id('ab_filesystem_info'),True,5):
            click_textview_by_id('ab_filesystem_info')
            if wait_for_fun(lambda:search_view_by_id('filesystem_info_dialog_tab_disk_usage'),True,5):
                click_textview_by_id('filesystem_info_dialog_tab_disk_usage')
                sleep(2)
                if not search_text('Total',searchFlag=TEXT_CONTAINS):
                    log_test_framework(self.name,'disk usage no total')
                    take_screenshot()
                    case_flag=False
                if not search_text('Used',searchFlag=TEXT_CONTAINS):
                    log_test_framework(self.name,'disk usage no used')
                    take_screenshot()
                    case_flag=False
                if not search_text('Free',searchFlag=TEXT_CONTAINS):
                    log_test_framework(self.name,'disk usage no free')
                    take_screenshot()
                    case_flag=False
                else:
                    log_test_framework(self.name,'disk usage pass')
                    case_flag=True
            else:
                log_test_framework(self.name, 'no disk usage')
                take_screenshot()
                case_flag=False
        else:
            log_test_framework(self.name, 'no this option')
            take_screenshot()
            case_flag=False
        return case_flag
    

            
  
