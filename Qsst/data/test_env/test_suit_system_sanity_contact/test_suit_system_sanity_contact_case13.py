'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line ,record_screen
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_system_sanity_contact import *
import time
import threading


class test_suit_system_sanity_contact_case13(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    Step1:launch contact
    Step2:add contact deall
    Step3:share all contact via import/export->share all contact
    verification:
    ER1:can launch share contact
    '''
    
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        TAG = "share contacts: Contact "
        log_test_framework(TAG, self.name + " -Start")
        
        """
        cases contnets you need to add
        """
        settings.check_after_resetphone()
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity("com.android.contacts", "com.android.contacts.activities.PeopleActivity")
        sleep(5)
        phone.permission_allow()        
        #contact.share_visible_contacts()
        if contact.checkHasContact():
            log_test_framework(self.name, 'contact has contacts')
        else:
            contact.add_contact_to_phone("deall","123")
        share_visible_contacts()
        click_textview_by_text("Messaging",searchFlag=TEXT_CONTAINS)
        sleep(3)
        if search_view_by_id("button_once"):        
            click_button_by_id("button_once")
            sleep(6)
        phone.permission_allow()
        sleep(2)
        if wait_for_fun(lambda:search_text("Send message"),True,5):
            case_flag = True
            log_test_framework(self.name, 'case_flag :%s'%case_flag)
        send_key(KEY_BACK)
        sleep(2)
        send_key(KEY_BACK)
        sleep(2)
        if search_text("OK"):
            click_textview_by_text("OK")
            sleep(2)
        send_key(KEY_HOME)
        sleep(3)
                    
        if search_text("Unfortunately",searchFlag=TEXT_CONTAINS):
            if search_text("OK"):
                click_button_by_text("OK")
            take_screenshot()
            case_flag=False
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
            
        elif search_text("isn't responding",searchFlag=TEXT_CONTAINS):
            if search_text("OK"):
                click_button_by_text("OK")
            take_screenshot()
            case_flag=False
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")
            
        
        send_key(KEY_BACK)
        sleep(3)
        send_key(KEY_BACK)
        sleep(3)
        send_key(KEY_HOME)
        sleep(3)
        
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
    
    
