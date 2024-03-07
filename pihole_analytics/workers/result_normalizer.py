# functions to convert/prettify Type, Status, Timestamps, ect here
#https://docs.pi-hole.net/database/ftl/#query-table
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def normalize(data):
    schema = {
        'type':{
            1:"A",
            2:"AAAA",
            3:"ANY",
            4:"SRV",
            5:"SOA",
            6:"PTR",
            7:"TXT",
            8:"NAPTR",
            9:"MX",
            10:"DS",
            11:"RRSIG",
            12:"DNSKEY",
            13:"NS",
            14:"OTHER",
            15:"SVCB",
            16:"HTTPS",
        },
        'status':{
            0:"Unknown: Unknown status (not yet known)",
            1:"Blocked: Domain contained in gravity database",
            2:"Allowed: Forwarded",
            3:"Allowed: Replied from cache",
            4:"Blocked: Domain matched by a regex blacklist filter",
            5:"Blocked: Domain contained in exact blacklist",
            6:"Blocked: By upstream server (known blocking page IP address)",
            7:"Blocked: By upstream server (0.0.0.0 or ::)",
            8:"Blocked: By upstream server (NXDOMAIN with RA bit unset)",
            9:"Blocked:Domain contained in gravity database.",
            10:"Blocked: Domain matched by a regex blacklist filter.",
            11:"Blocked: Domain contained in exact blacklist",
            12:"Allowed: Retried query",
            13:"Allowed: Retried but ignored query (this may happen during ongoing DNSSEC validation)",
            14:"Allowed: Already forwarded, not forwarding again",
            15:"Blocked: Blocked (database is busy)",
            16:"Blocked: Blocked (special domain)",
            17:"Allowed: Replied from stale cache"
        },
        'reply_type':{
            0:"unknown (no reply so far)",
            1:"NODATA",
            2:"NXDOMAIN",
            3:"CNAME",
            4:"a valid IP record",
            5:"DOMAIN",
            6:"RRNAME",
            7:"SERVFAIL",
            8:"REFUSED",
            9:"OTHER",
            10:"DNSSEC",
            11:"Allowed: Retried query",
            12:"Allowed: Retried but ignored query (this may happen during ongoing DNSSEC validation)",
            13:"BLOB (binary data)"
        },
        'dnssec':{
            0:"unknown",
            1:"SECURE",
            2:"INSECURE",
            3:"BOGUS",
            4:"ABANDONED"
        }
    }

    for column, mapping in schema.items():
        data[column] = data[column].map(mapping)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    
    return data