#==========================================================================
# REVISION HISTORY: 
#  1.00   <shijunz>   <12/23/2013> Created
#
# TEST NAME: qsst demo
#
# DESCRIPTION:
#  This test case introduces demo for how to use the QSST. Be careful the run steps:
#   Init->Config->StartRun->GetReport->CleanUp.
#
# Example:
   # use QsstUtility;
   # QsstUtility::Init();
   # QsstUtility::Config();
   # QsstUtility::StartRun();
   # QsstUtility::GetReport("c:\\temp\\logs");
   # QsstUtility::CleanUp();
#==========================================================================

use strict;
use storable;
use constant;
use IO::Socket;
use Net::Config;

package QsstUtility;

#==========================================================================
# may should be change your QSST test case directory, 
# it maybe test_env_beiing or test_env_SD
our $TEST_ENV_DIR = "test_env";

# may should be change your QSST test config
our %config_hash = (
    "public.smart_number" => "333",
    "public.phone_platform_type" => "automatch",
    "private.phone.call_repeat_times" => "50",
    "private.phone.call_time" => "20",
    "private.hostlogging.qxdm_configuration" =>"C:\\\\\\\\Qsst\\\\\\\\Bluetooth.dmc",
    "private.hostlogging.log_save_path" =>"C:\\\\\\\\Qsst\\\\\\\\log\\\\\\\\",
    "\\*.\\*" => '0',  # disable all case under test_env
    "test_suit_camera.*"=> "1", # enable all cases under the given test_suit_camera
    "test_suit_camera.test_suit_camera_case1"=> "0", # disable the test_suit_camera_case1
    );
#==========================================================================


my %ser_info = (
    "ser_ip" => "127.0.0.1",
    "ser_port" => "7777",
);
our $QSST_SERVICE_ACTION_START = 986;
our $QSST_SERVICE_ACTION_CONFIG = 989;
our $SOCKET_CLOSED_FLAG = 990;
our $QSST_SERVICE_ACTION_REPORT = 991; 
our $END_FLAG = "END";
our $singleInstance = 0;


sub Init {
    if ( $singleInstance == 0 ){
      $singleInstance = 1;
      system("adb forward tcp:7777 tcp:8974");
    }else{
      die "Only single Instace be created."
    }    
}


sub StartRun {
    my $ser_addr = $ser_info{"ser_ip"};
    my $ser_port = $ser_info{"ser_port"};
    my $end;
    my $socket = IO::Socket::INET->new(
                                         PeerAddr => "$ser_addr",
                                         PeerPort => "$ser_port",
                                         Proto => "tcp",
                                       )
       or die "Can not create socket connect.$@";

    my $send_cmd_run = $QSST_SERVICE_ACTION_START.":".$TEST_ENV_DIR."\n";
    print $send_cmd_run;
    $socket->send($send_cmd_run,0);

    if($socket->recv($end,100,0)){    
        print "get qsst run return value is : ".$end."\n";
        my $send_contents = $SOCKET_CLOSED_FLAG.":".$END_FLAG."\n";
        print $send_contents;
        $socket->send($SOCKET_CLOSED_FLAG.":".$END_FLAG."\n",0);
        $socket->close() or die "Close Socket failed.$@";
    }else{
        die "can not get qsst run result!!!";
    }
    return $end;
}


sub Config{

    my $ser_addr = $ser_info{"ser_ip"};
    my $ser_port = $ser_info{"ser_port"};
    my $key;
    my $end;
    my $value;

    my $socket = IO::Socket::INET->new(
                                         PeerAddr => "$ser_addr",
                                         PeerPort => "$ser_port",
                                         Proto => "tcp",
                                       )
       or die "Can not create socket connect.$@";
    foreach $key (sort keys %config_hash){
        $value =$config_hash{$key};
        my $send_cmd_config = $QSST_SERVICE_ACTION_CONFIG.":".$TEST_ENV_DIR."{".$key.":".$value."}\n";
        print $send_cmd_config;
        $socket->send($send_cmd_config,0);
        
        $socket->recv($end,100,0);
        print $end;
    }
    $socket->send($SOCKET_CLOSED_FLAG.":".$END_FLAG."\n",0);
    $socket->close() or die "Close Socket failed.$@";
}

sub GetReport{    
    my $ser_addr = $ser_info{"ser_ip"};
    my $ser_port = $ser_info{"ser_port"};
    my $key;
    my $end;
    my $value;
    my $last_log_files_path;
    my $socket = IO::Socket::INET->new(
                                         PeerAddr => "$ser_addr",
                                         PeerPort => "$ser_port",
                                         Proto => "tcp",
                                       )
       or die "Can not create socket connect.$@";
       
    
    my $last_log_files_path = _get_last_logs_dir_name();
    
    my $saved_path = "/sdcard/com.android.qrdtest/".$last_log_files_path;
    
    my $send_cmd_get_log = $QSST_SERVICE_ACTION_REPORT.":".$saved_path."\n";
    
    print $send_cmd_get_log;
    $socket->send($send_cmd_get_log,0);
    $socket->recv($end,100,0);
    
    if( $end == 0 ){
        print "creat log ok. begin to upload logs\n";
       
        unless ( -e $_[0]) {
           warn "not found $_[0], so mkdir it... \n";
           mkdir $_[0];
        }
        system("adb pull $saved_path $_[0]\\$last_log_files_path");
        
    }else{
      print "creat log failed";      
    }

    $socket->send($SOCKET_CLOSED_FLAG.":".$END_FLAG."\n",0);
    $socket->close() or die "Close Socket failed.$@";
    print $end;
    return $end;
}

sub _get_last_logs_dir_name{
    my $saved_path = "/sdcard/com.android.qrdtest/";
    my @logFileList = `adb shell ls $saved_path`;
    @logFileList = sort @logFileList; #make sure the last one is right.
    my $last_log_files = pop (@logFileList);
    
    unless ($last_log_files){
       die "failed to get last_log_files \n";
    }
    
    print "last_log_files is $last_log_files \n";
    $last_log_files;
}


sub CleanUp {
    print "clean up be called, The End.\n";
}

#==========================================================================
# 
# QUALCOMM Proprietary
# 
# Copyright (c) 2013, by QUALCOMM Incorporated. All Rights Reserved.
#==========================================================================
1;
