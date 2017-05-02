use HelperFunctions;
use File::Copy;

# Global variable
my $QXDM;

# Initialize application
sub Initialize
{
   # Assume failure
   my $RC = false;

   # Create QXDM object
   $QXDM = new Win32::OLE 'QXDM.Application';
   if ($QXDM == null)
   {
      print "\nError launching QXDM";

      return $RC;
   }

   # Create QXDM2 interface
   $QXDM2 = $QXDM->GetIQXDM2();
   if ($QXDM2 == null)
   {
      print "\nQXDM does not support required interface";

      return $RC;
   }

   SetQXDM ( $QXDM );
   SetQXDM2 ( $QXDM2 );

   # set QXDM running in invisible mode.
#   $QXDM->{'Visible'}=false;

   # Success
   $RC = true;
   return $RC;
}

# Loading the QXDM configuration
sub LoadConfiguation
{
   $FileName = $_[0];
   print "\nLoading configuration file:\n"
       . "$FileName\n";

   # Load existing configuration
   $QXDM->LoadConfig( $FileName );

   return true;
}

# Obtain and dump out the COM port status
sub DumpCOMPort
{
   # Check COM port status
   my $COMPort = $QXDM->COMPort;
   if ($COMPort == -1)
   {
      print "Error occurred\n";
      return false;
   }
   elsif ($COMPort == 0)
   {
      print "Disconnected state\n";
      return false;
   }
   elsif ($COMPort > 0)
   {
      print "Connected to port: COM" . $COMPort . "\n";
   }
   return true;
}

# Connect COM port
sub QXDMCOMPort
{
   $PortNumber = $_[0];
   if ($PortNumber != -1)
   {
      # Change the COM port
      $QXDM->{COMPort} = $PortNumber;
   }
   # Obtain and dump out the COM port status
   return DumpCOMPort();
}

# Save the curent ISF
sub SaveISF
{
   my ( $FileName ) = @_;
   $QXDM->SaveItemStore( $FileName );
   print "Saved item store to:\n" . $FileName . "\n";   

   $RC = true;
   return $RC;
}

# Save item
sub QXDMSaveItemStore
{

   # Get file name from script folder path
   my $FileName = GenerateFileName( $_[0], ".isf" );
   if ($FileName eq "")
   {
      return false;
   }

   # Save current item store
   SaveISF( $FileName );
   return true;
}

# Quit QXDM application
sub QXDMQuitApplication
{
   $QXDM->QuitApplication();

   print "closed\n";
   return true;
}

# Clear the item view
sub ClearViewItems
{
   # Assume failure
   my $RC = false;

   # Create the view first
   $RC = $QXDM->CreateView( "Item View", "" );
   if ($RC == false)
   {
      print "\nFailed to create \'Item View\'";

      return false;
   }

   # Clear the view
   $RC = $QXDM->ClearViewItems( "Item View" );
   if ($RC == false)
   {
      print "\nCannot clear view \'Item View\'";

      return false;
   }

   print "\n\'Item View\' successfully cleared\n";
   return true;
}

# Main body of script
sub Init
{
   # Launch QXDM
   my $RC = Initialize();
   if ($RC == false)
   {
      return false;
   }

   # Get QXDM version
   my $Version = $QXDM->{AppVersion};
   print "\nQXDM Version: " . $Version . "\n";
   return true;
}

1;