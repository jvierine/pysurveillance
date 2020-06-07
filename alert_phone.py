import nexmo
from pprint import pprint
import os
import time
import numpy as n

import pysurveillance_conf as conf


disable_call=False

def is_armed(h_now):

    # we pass midnight
    if conf.alert_armed_h1 < conf.alert_armed_h0:
        if h_now > conf.alert_armed_h0:
            return(True)
        if h_now < conf.alert_armed_h1:
            return(True)
    else:
        if h_now > conf.alert_armed_h0 and h_now < conf.alert_armed_h0:
            return(True)
    return(False)


def send_alert():
    h_now=n.mod(time.time()/3600.0,24.0)

    if not is_armed(h_now):
        return    
    
    if disable_call:
        return

    if os.path.exists("last_call.bin"):
        last_t0=n.fromfile("last_call.bin",dtype=n.float64)
    else:
        last_t0=0.0

    this_call_t0=n.float64(time.time())
    

    if (this_call_t0 - last_t0)/3600.0 < conf.minimum_spacing_between_calls:
        print("not calling. we've already made a call in the past %1.2f hours"%(conf.minimum_spacing_between_calls))
        return

    # save call time
    this_call_t0.tofile("last_call.bin")

    
    if disable_call:
        print("Not making a call. Calls disabled")
        return

    if os.path.exists("private.key"):
        client = nexmo.Client(
            application_id='a0d56b5f-f02f-4b75-9883-d0d22f018581',
            private_key='private.key')
        ncco = [
            {
                'action': 'talk',
                'voiceName': 'Kendra',
                'text': 'This is an automated phone call. We have detected a person in your security camera.'
            }
        ]
        response = client.create_call({
              'to': [{
                      'type': 'phone',
                      'number': '4798172827'
                    }],
              'from': {
                      'type': 'phone',
                      'number': '4798172827'
                    },
              'ncco': ncco
            })

        pprint(response)

if __name__ == "__main__":
    send_alert()
