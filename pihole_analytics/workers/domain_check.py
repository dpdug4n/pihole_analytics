import logging, os, requests, json
import pandas as pd

# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

def vt_lookup(domain):  
    try:
        # using requests instead of vt-py due to asyncio compatibility issues
        url = f"https://www.virustotal.com/api/v3/domains/{domain}"
        headers = {"X-Apikey": f"{os.getenv('VT_API_KEY')}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_error:
        logger.error(f'Error making request:{http_error}')
    except Exception as unexpected_error:
        logger.error(type(unexpected_error).__name__)
        logger.error(unexpected_error)

def domain_lookup(domain):
    vt_domain = vt_lookup(domain).get('data')
    whois = vt_domain.get('attributes').get('whois').replace('\n','''  
    - ''')
    markdown = f'''
## Domain: [{vt_domain.get('id')}](https://www.virustotal.com/gui/domain/{domain})  
- Addresses|DNS Records: {', '.join([address.get('value') for address in vt_domain.get('attributes').get('last_dns_records')])}
- Verdict:  
    - Malicious: {vt_domain.get('attributes').get('last_analysis_stats').get('malicious')}  
    - Suspicious: {vt_domain.get('attributes').get('last_analysis_stats').get('suspicious')}  
    - Undetected: {vt_domain.get('attributes').get('last_analysis_stats').get('undetected')}  
    - Harmless: {vt_domain.get('attributes').get('last_analysis_stats').get('harmless')}  
- WhoIs:  
    - {whois}
    '''
    return markdown