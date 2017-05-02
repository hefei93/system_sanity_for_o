'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_system_sanity_contact import *

class test_suit_system_sanity_contact_case02(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    Step1: launcher contacts
    Step2: import vcf file
    
    verification:
    can import contacts
    
    '''
    
    def test_case_main(self, case_results):
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False        
        TAG = "Dev-ci cases: Contact "
        log_test_framework(self.name, " -Start")
        
        
        """
        cases contnets you need to add
        """
        
        def execute():  
            p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
            start_activity("com.android.contacts", "com.android.contacts.activities.PeopleActivity")
            if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 8):
                phone.permission_allow()
            if search_text("Next",isScrollable=0):
                send_key(KEY_BACK)
                sleep(3)
            if wait_for_fun(lambda:search_text("ALL"), True, 5) or search_text("ADD ACCOUNT")or search_text("Contacts", searchFlag=TEXT_CONTAINS):
                log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Enter contact successfully")    			                               
                if wait_for_fun(lambda:search_text("IMPORT CONTACTS",),True,5):
                    click_textview_by_text("IMPORT CONTACTS")
                else:
                    click_textview_by_desc("More options")
                    sleep(2)
                    click_textview_by_text("Import/export")
                if wait_for_fun(lambda:search_text("Import from .vcf file"),True,5):
                    click_textview_by_text("Import from .vcf file")
                    sleep(2)
                    if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 8):
                        phone.permission_allow()
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
                
            else:
                take_screenshot()
                log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "case fail")

            return case_flag
        
        case_flag = repeat_cmcc_devci(execute,1)
        
        
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
