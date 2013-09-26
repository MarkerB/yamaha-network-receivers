# Python Imports
from xml.dom import minidom
import httplib

# Local Imports
import globals
from helpers import *

def do_xml(xml, **kwargs):
    """
    Base function to send/receive xml using either GET or POST

    Optional Parameters:
    timeout, ip, port, return_result, print_error
    """
    timeout = float(kwargs.get('timeout', globals.default_timeout))
    ip = kwargs.get('ip', globals.ip_address)
    port = kwargs.get('port', globals.port)
    return_result = kwargs.get('return_result', False)
    print_error = kwargs.get('print_error', True)

    conn = httplib.HTTPConnection('{0}:{1}'.format(ip, port), timeout=float(timeout))
    headers = { "Content-type": "text/xml" }
    try:
        conn.request("POST", "/YamahaRemoteControl/ctrl", "", headers)
        conn.send(xml)
        if return_result:
            response = conn.getresponse()
            rval = response.read()
            conn.close()
            return rval
        else:
            conn.close()
            return True
    except socket.error:
        if print_error:
           eg.PrintError("Unable to communicate with Yamaha Receiver. The connection timed out.")
           return None
        else:
            raise

def send_xml(xml, **kwargs):
    """
    Communicate with the receiver, but do not wait or return the results
    """
    kwargs['return_result'] = False
    do_xml(xml, **kwargs)

def put_xml(xml, **kwargs):
    send_xml('<YAMAHA_AV cmd="PUT">{0}</YAMAHA_AV>'.format(xml), **kwargs)

def zone_put_xml(zone, xml, **kwargs):
    if zone == -1:
        zone = globals.active_zone
    if zone < 2:
        put_xml('<Main_Zone>{0}</Main_Zone>'.format(xml), **kwargs)
    elif zone < -1:
        put_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, chr(-1 * zone)), **kwargs)
    else:
        put_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), **kwargs)

def receive_xml(xml, **kwargs):
    kwargs['return_result'] = True
    return do_xml(xml, **kwargs)

def get_xml(xml, **kwargs):
    return receive_xml('<YAMAHA_AV cmd="GET">{0}</YAMAHA_AV>'.format(xml), **kwargs)

def zone_get_xml(zone, xml, **kwargs):
    if zone == -1:
        zone = globals.active_zone
    if zone < 2:
        return get_xml('<Main_Zone>{0}</Main_Zone>'.format(xml), **kwargs)
    elif zone < -1:
        return get_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, chr(-1 * zone)), **kwargs)
    else:
        return get_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), **kwargs)

def get_basic_status(zone=-1, **kwargs):
    return zone_get_xml(zone, '<Basic_Status>GetParam</Basic_Status>', **kwargs)

def get_tuner_status(**kwargs):
    return get_xml('<Tuner><Play_Info>GetParam</Play_Info></Tuner>', **kwargs)

def get_tuner_presets(**kwargs):
    return get_xml('<Tuner><Play_Control><Preset><Data>GetParam</Data></Preset></Play_Control></Tuner>', **kwargs)

def get_config(**kwargs):
    return get_xml('<System><Config>GetParam</Config></System>', **kwargs)

def get_status_string(param, zone=-1, **kwargs):
    xml = get_basic_status(zone, **kwargs)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_status_param_is_on(param, zone=-1, **kwargs):
    return get_status_string(param, zone, **kwargs) == "On"

def get_status_int(param, zone=-1, **kwargs):
    return int(get_status_string(param, zone, **kwargs))

def get_config_string(param, **kwargs):
    xml = get_config(**kwargs)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_config_param_is_on(param, **kwargs):
    return get_config_string(param, **kwargs) == "On"

def get_config_int(param, **kwargs):
    return int(get_config_string(param, **kwargs))

def get_tuner_string(param, **kwargs):
    xml = get_tuner_status(**kwargs)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_tuner_param_is_on(param, **kwargs):
    return get_tuner_string(param, **kwargs) == "On"

def get_tuner_int(param, **kwargs):
    return int(get_tuner_string(param, **kwargs))
