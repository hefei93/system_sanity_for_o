#!/usr/bin/perl
#tcpserver.pl

use IO::Socket::INET;
require "QXDMApi.pl";

my ($socket,$client_socket);
my ($peeraddress,$peerport);

# creating object interface of IO::Socket::INET modules which internally does
# socket creation, binding and listening at the specified port address.
$socket = new IO::Socket::INET (
LocalHost => '127.0.0.1',
LocalPort => $ARGV[0],
Proto => 'tcp',
Listen => 20,
Reuse => 1
) or die "ERROR in Socket Creation : $!\n";

print "SERVER Waiting for client connection on port $ARGV[0]\n";

# waiting for new client connection.
$client_socket = $socket->accept();

# get the host and port number of newly connected client.
$peer_address = $client_socket->peerhost();
$peer_port = $client_socket->peerport();

print "Accepted New Client Connection From : $peer_address, $peer_port \n ";

$data = "Connect server successed.";
print $client_socket "$data\n";

# init QXDM application.
Init();
$data = "Init QXDM successed.";
print $client_socket "$data\n";

sub send_response
{
    $tag = $_[0];
    if ($_[1])
    {
        print $client_socket $tag." true\n";
    } else
    {
        print $client_socket $tag." false\n";
    }
}

$flag = 1;
while($flag) {
    $data = <$client_socket>;
    @args = split(/ /, $data);
    if (@args[0] eq "LoadConfiguation") {
        chomp(@args[1]); # remove string "\n"
        $result = LoadConfiguation(@args[1]);
        send_response(@args[0], $result);
    } elsif (@args[0] eq "QXDMCOMPort") {
        chomp(@args[1]);
        $result = QXDMCOMPort(@args[1]);
        send_response(@args[0],$result);
    } elsif (@args[0] eq "QXDMSaveItemStore") {
        chomp(@args[1]);
        $result = QXDMSaveItemStore(@args[1]);
        send_response(@args[0],$result);
    } elsif (@args[0] eq "QXDMQuitApplication") {
        $result = QXDMQuitApplication();
        send_response(@args[0],$result);
        $flag = 0;
    } elsif (@args[0] eq "ClearViewItems") {
        $result = ClearViewItems();
        send_response(@args[0],$result);
    }
    sleep(1)
}
$socket->close();
