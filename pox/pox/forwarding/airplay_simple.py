# Copyright 2012 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.

"""
This is the world's simplest OpenFlow learning switch.
"""

from pox.core import core
from pox.lib.addresses import IPAddr, EthAddr
import pox.openflow.libopenflow_01 as of


log = core.getLogger()


def _handle_PacketIn (event):
  packet = event.parsed

  # If this is a Bonjour packet call _bonjour_out 
  ip = packet.find('ipv4')
  if ip != None:
    if ip.dstip == IPAddr("224.0.0.251"):
      log.info("Calling _bonjour_out for mac foo")
      _bonjour_out(packet,event.ofp.buffer_id)

  
  # If we get a packet FROM some src address on some input port, we
  # know that if we want to send TO that address, we should send it
  # out that port.  Install a rule for this.

  msg = of.ofp_flow_mod()
  msg.match.dl_dst = packet.src
  msg.actions.append(of.ofp_action_output(port = event.port))
  event.connection.send(msg)

  

  # Now since we got a packet at the controller, that must mean
  # that we hadn't installed a rule for the destination address
  # yet -- we don't know where it is.  So, we'll just send the
  # packet out all ports (except the one it came in on!) and
  # hope the destination is out there somewhere. :)
  msg = of.ofp_packet_out()
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
  msg.buffer_id = event.ofp.buffer_id # Resend the incoming packet
  msg.in_port = event.port # Don't flood out the incoming port
  event.connection.send(msg)

def _handle_SwitchConnect (event):
  
  # Insert rule to send Bonjour packets to the Controller in all cases
  # Bonjour uses 22
  log.info("Switch connect %s adding Bonjour rule" % event.dpid)
  


  msg = of.ofp_flow_mod()
  msg.match.dl_type = 0x800
  msg.match.nw_dst = IPAddr("224.0.0.251")
  # Set higher than default priority
  msg.priority = 50000
  msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
  event.connection.send(msg)
  
def _bonjour_out (packet,buffer_id):

  print str(packet.src)
  print pairs_dict
  # if there is a known port for a pairing match and send packet
  for key in pairs_dict.keys():
    log.info("key %s %s" % (key,str(packet.src)))
    if key == str(packet.src):
      bon_dst = pairs_dict[key]
      if bon_dst['port']:
        # Send Packet to dst_mac if known dpid/port for dst 
        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port = bon_dst['port']))
        msg.buffer_id = buffer_id
        log.info("msg %s" % msg) 
        if core.openflow.sendToDPID(bon_dst['dpid'],msg.pack()):
          log.info ("Sent Bonjour packet from %s to %s  dpid %s port %d" % (key,bon_dst['dst_mac'],bon_dst['dpid'],bon_dst['port']))
          
  return          
                    
                    


def _get_pairs_from_DB ():
  
  # This will get data from perm database over JSON 
  # Just put test data for now

  dst = {'dst_mac': '00:00:00:00:00:02',
          'dpid': '1',
          'port': '1'}

  pairs = {}

  src_mac = '98:d6:bb:2b:57:f2'
  pairs[src_mac] = dst

  return pairs
 


def launch ():

  # Initialise a dictionary with mac pairings
  global pairs_dict 
  pairs_dict = _get_pairs_from_DB()

  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  core.openflow.addListenerByName("ConnectionUp", _handle_SwitchConnect)  

  log.info("Learning switch running.")
  
