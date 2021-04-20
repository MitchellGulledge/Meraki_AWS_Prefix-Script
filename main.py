import os 
import requests # pip3 install requests
import json # pip3 install json

# this script executes some shell commands to retrieve the public IPs for Meraki Dashboard
# there are cleaner ways and proper libraries to retrieve this data, but for time and ease of use
# subprocess will be used from the os library

# creating function to retrieve a list of all prefixes from the Meraki Autonomous Systems
def get_meraki_prefixes():

    # creating the two ASNs that are owned by Meraki
    asn_1 = 'AS395831'
    asn_2 = 'AS21581'

    # creating ASN list to iterate through
    asn_list = [asn_1, asn_2]

    # creating master IP list to store IP addresses from Meraki and AWS
    master_ip_list = []

    # iterating through the asn list to execute the respective whois commands for each asn
    for asn in asn_list:

        # crafting whois shell command
        whois = f"whois -h whois.radb.net -- '-i origin {asn}' | grep -Eo \"([0-9.]+)" +"{4}"+ "/[0-9]+\""

        # the os.popen() command opens a pipe from or to the command line. 
        # This means that we can access the stream within Python. 
        # This is useful since you can now get the output as a variable
        whois_output = os.popen(whois)

        # using list comprehension to create a list of all the individual prefixes from the output
        # need to index /n from the output
        sub_asn_list = [ str(x)[0:-1] for x in whois_output]

        # appending sub_asn_list to master_ip_list
        master_ip_list = master_ip_list + sub_asn_list


    return master_ip_list

# creating function to grab all AWS prefixes from published json
def get_aws_prefixes():

    # obtaining json formatted list of all aws prefixes 
    raw_aws_json = requests.get(
        "https://ip-ranges.amazonaws.com/ip-ranges.json"
        ).content

    # converting contents variable from a bytes data type to json format
    formatted_aws_prefixes = json.loads(raw_aws_json.decode('utf8').replace("'", '"'))

    # creating AWS dictionary to hold all region: prefixes so we can map test data to it later
    aws_data_dictionary = {}

    for prefix in formatted_aws_prefixes['prefixes']:

        if prefix['region'] in aws_data_dictionary:

            aws_data_dictionary[prefix['region']].append(prefix['ip_prefix'])

        elif prefix['region'] not in aws_data_dictionary:

            # creating sample dictionary that is easy to later append to
            aws_data = {prefix['region']: [prefix['ip_prefix']]}

            aws_data_dictionary.update(aws_data)

    print(aws_data_dictionary)

get_aws_prefixes()
