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
from test_suit_system_sanity_camera import *



class test_suit_system_sanity_camera_case17(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Test Steps:
    step1.Open Camera app
    step2.Press camera shot to take a photo
    step3:Check the speed when thumbnail display
    Verification: 
    ER4: The response can quickly same with reference phone
    '''
    
    
    def test_case_main(self, case_results):
        
        
        global case_flag , TAG, i,recoreName,p ,x,y
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        x=int(getDisplayWidth())
        y=int(getDisplayHeight())
        result=[]
        TAG = "Take snapshot with random feature: Camera "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        if search_text("Close app", searchFlag=TEXT_CONTAINS):
            click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
            sleep(2) 
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)       
        start_activity('org.codeaurora.snapcam','com.android.camera.CameraLauncher')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 10):
            click_button_by_id('permission_allow_button')
        if wait_for_fun(lambda:search_text('OK'), True, 5):            
            click_textview_by_text('OK')
        if wait_for_fun(lambda:search_view_by_id('shutter_button'), True, 5):
            log_test_framework("step1:", "Launch camera pass") 
            takePhoto(1) 
            if wait_for_fun(lambda:search_view_by_id('preview_thumb'), True, 5):
                click_imageview_by_id("preview_thumb")
                if wait_for_fun(lambda:search_view_by_id("photopage_bottom_control_delete"), True, 5):
                    send_key(KEY_BACK)
                    sleep(2)
                    case_flag=True
        if search_text("isn't responding", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR") 
            case_flag = False           
            take_screenshot()
            if search_text("Close app", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close app", searchFlag=TEXT_CONTAINS)
                sleep(2)
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
        elif search_text("Unfortunately", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs crash")
            case_flag = False
            take_screenshot()
            if search_text("OK", searchFlag=TEXT_CONTAINS):
                click_button_by_text("OK")
                sleep(2)
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
        elif search_text("stopped", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup has stopped")
            case_flag = False
            take_screenshot()
            if search_text("Close", searchFlag=TEXT_CONTAINS):
                click_button_by_text("Close")
                sleep(2)            
            if search_text("OK", searchFlag=TEXT_CONTAINS):
                click_button_by_text("OK")
                sleep(2)       
        elif search_text("Close app", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup Close app error")
            case_flag = False
            take_screenshot()            
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
        p.terminate()  
