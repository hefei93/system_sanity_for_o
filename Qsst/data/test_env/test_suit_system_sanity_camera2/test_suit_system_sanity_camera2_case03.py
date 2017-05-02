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



class test_suit_system_sanity_camera2_case03(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch camera;
    Step2:Switch flash light to Auto, and take a picture;
    Step3: switch flash light to On, and take a picture;
    Step4: switch flash light to Off, and take a picture;
    Step5: repeat Step2 to Step5 for 100 time;    
    Verification: 
    ER2: picture have no exception;
    ER3: picture have no exception;
    ER4: picture have no exception;
    ER5: picture have no exception;    
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
                    
        start_activity('org.codeaurora.snapcam','com.android.camera.CameraLauncher')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 10):
            click_button_by_id('permission_allow_button')
        if wait_for_fun(lambda:search_text('OK'), True, 5):            
            click_textview_by_text('OK')
        self.delete_photos()
        self.recording_video()
        case_flag=self.check_video_detail()
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
            case_flag=False
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Popup Close app error")
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
 
    #switch to video mode,default 5 secends          
    def recording_video(self,recordtime=5):
        if wait_for_fun(lambda:search_view_by_id('id/camera_switcher'),True,5):
            click_textview_by_id('id/camera_switcher')
            sleep(2)
            x=getDisplayWidth()
            y=getDisplayHeight()
            click(int(x)-100,int(y)-300)
            sleep(5)
            log_test_framework(self.name, 'switch to video mode pass')
            click_textview_by_id('id/shutter_button')
            sleep(recordtime)
            click_textview_by_id('id/shutter_button')
            sleep(2)
            case_flag=True
        else:
            take_screenshot()
            log_test_framework(self.name, 'can not find switch camera mode')
            case_flag=False
        return case_flag
    
    #delete photos
    def delete_photos(self):
        if search_view_by_id('id/preview_thumb'):
            click_textview_by_id('id/on_screen_indicators')
            while(True):
                sleep(5)
                click(600,1200)
                if search_view_by_id('id/photopage_bottom_control_delete'):
                    click_textview_by_id('id/photopage_bottom_control_delete')
                    sleep(2)
                    click_textview_by_id('android:id/button1')
                    sleep(1)
                if search_view_by_id('id/on_screen_indicators'):
                    log_test_framework(self.name, 'picture has clear')
                    break
        elif search_view_by_id('id/on_screen_indicators'):
            log_test_framework(self.name, 'maybe no picture exists')
        else:
            log_test_framework(self.name,'error')
            take_screenshot()
            
    def check_video_detail(self):
        if wait_for_fun(lambda:search_view_by_id('id/preview_thumb'),True,5):
            click_textview_by_id('id/preview_thumb')
            sleep(1)
            if search_view_by_id('id/photopage_bottom_control_delete'):
                x=getDisplayWidth()
                click(int(x)-100,100)
                if wait_for_fun(lambda:search_text('Details'),True,5):
                    click_textview_by_text('Details')
                    case_flag=True
                else:
                    log_test_framework(self.name, 'can not find detail')
                    take_screenshot()
                    case_flag=False
            else:
                log_test_framework(self.name, 'no more option pop up')
                take_screenshot()
                case_flag=False
        else:
            log_test_framework(self.name,'no picture exist')
            take_screenshot()
            case_flag=False
        return case_flag
        
        