#!/usr/bin/env python

import subprocess
import optparse
import re
import random


def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Select an interface to alter its MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter the new MAC address.")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[?] Please specify an interface, use --help for more information.")
    elif not options.new_mac:
        parser.error("[?] Please specify a new MAC address or type random for a random MAC address, use --help for more information.")
    else:
        return options


def change_mac(interface, new_mac):
    if new_mac == "random":
        create_random_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        print("[!] Changing MAC Address for " + interface + " to " + create_random_mac)

        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", create_random_mac])
        subprocess.call(["ifconfig", interface, "up"])
    else:
        print("[!] Changing MAC Address for " + interface + " to " + new_mac)

        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[?] Could not read MAC address.")


options = get_argument()
current_mac = get_current_mac(options.interface)
print("Current MAC Address: " + str(current_mac))

change_mac(options.interface, options.new_mac)

new_current_mac = get_current_mac(options.interface)
if not current_mac == new_current_mac:
    print("[!] The MAC Address has been changed to " + new_current_mac)
else:
    print("[!]The Mac address was not changed.")
