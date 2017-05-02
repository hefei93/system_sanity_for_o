'''
@author: hu_ch

'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from qrd_shared.launcher.Launcher import Launcher
from _ctypes_test import func
from test_suit_system_sanity_message import *

class test_suit_system_sanity_message_case03(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    "Procedure:
    Step1:Launch message
    Step2:delete all messages 
    Verification: 
    ER1:can delete all messages successfully
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        TAG = "Dev-ci cases: Messager "
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR],  self.name +' : case Start')
        log_test_framework(TAG, self.name + " -Start")
        #Preconditions: Requires photo to be most recent picture taken and for the video to be directly across from it
        """
        cases contnets you need to add
        
        """
        #wakeUpDevice()
        #settings.kill_allpid()
        
     
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity("com.android.mms", "com.android.mms.ui.ConversationList")
        sleep(10)
        phone.permission_allow()
        if search_view_by_id("action_compose_new") or search_view_by_id("create"):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Enter Message successfully")
            sleep(1)
            case_flag=deleteAllMessage()                  
        if search_text("Unfortunately",searchFlag=TEXT_CONTAINS):
            if search_text("OK"):
                click_button_by_text("OK")
            take_screenshot()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
            
        elif search_text("isn't responding",searchFlag=TEXT_CONTAINS):
            if search_text("OK"):
                click_button_by_text("OK")
            take_screenshot()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")
            
                        
        send_key(KEY_BACK)
        sleep(2)
        send_key(KEY_BACK)
        sleep(2)
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