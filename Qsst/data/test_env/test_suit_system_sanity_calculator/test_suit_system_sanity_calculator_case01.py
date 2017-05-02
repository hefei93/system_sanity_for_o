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
from test_suit_system_sanity_calculator import *



class test_suit_system_sanity_calculator_case01(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    """
    "Procedure:
    Step1:Launch calculator
    Step2:simple calculator(+,-,*,/)
    Verification: 
    ER1:verify 1+2=3,7-6=1,4*3=12,8/4=2
    """
    '''
    
    
    def test_case_main(self, case_results):
        
        global case_flag , TAG, recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])
        case_flag = False
        result=[]
        TAG = "simple calculator: Calculator "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        
        def execute():    
            case_flag=False
            start_activity('com.android.calculator2','com.android.calculator2.Calculator')
            p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
            if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
                phone.permission_allow()                  
            if search_view_by_id('del') or search_view_by_id('clr'):
                log_test_framework(self.name, "Launch calculator pass")
                #click_textview_by_text('6')
                case_flag1=operator('1',lambda:add(),'2','3')
                sleep(1)
                result.append(case_flag1)
                case_flag2=operator('7',lambda:jian(),'6','1')
                sleep(1)
                result.append(case_flag2)
                case_flag3=operator('4',lambda:chen(),'3','12')
                sleep(1)
                result.append(case_flag3)
                case_flag4=operator('8',lambda:chu(),'4','2')
                result.append(case_flag4)
                case_flag=not False in result
            elif search_text('has stopped',searchFlag=TEXT_CONTAINS):
                log_test_framework("gp_sanity_calculator_case1:", "Popup has stopped")
                take_screenshot()
                if search_text("OK"):
                    click_button_by_text("OK")
                    sleep(2)
                if search_text("Close"):
                    click_button_by_text("Close")
                    sleep(2)            
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
                log_test_framework("gp_sanity_calculator_case1:", "Launch calculator fail")                
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
  
