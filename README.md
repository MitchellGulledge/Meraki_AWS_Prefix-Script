# Meraki_AWS_Prefix-Script

This script executes some shell commands to retrieve the public IPs for Meraki Dashboard.

We utilize the Meraki ASNs and perform a whois lookup to fetch all prefixes associated with the ASNs.

Additionally, there is a function to get all AWS prefixes from their public json file and create a dictionary with a k,v pair of region and list of prefixes.

AWS Prefixes json: https://ip-ranges.amazonaws.com/ip-ranges.json

