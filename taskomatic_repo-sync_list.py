#!/usr/bin/python
#
#  taskomatic_repo-sync_list.py
#
# Generate a list of channels and taskomatic schedule for repository sync jobs.
# The list is sorted alphabetically by channel name
#
# The schedules are listed in crontab format
# Channel names and schedules are associated to an internal channel id number.
# In some lists these ids are returned as numeric values and others come back as text strings.
# In order to match them up between the channel names and schedules I found it necessary to convert
# the ids returned from the taskomatic repo-sync list from text to integer.
#

#
import xmlrpclib, struct
from array import *
#
# Replace the userid and password with your information before running this
#
SATELLITE_URL = "http://localhost/rpc/api"
SATELLITE_LOGIN = "username"
SATELLITE_PASSWORD = "password"

#
# Connect and login to the spacewalk server
#
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key_session = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

#
# Get a list of all channels
#
channels = client.channel.listAllChannels(key_session)

chan_name = {}
chan_sched = {}

#
# Build an array of channel names indexed by internal channel id number
#
for c in channels:
    chan_name[ c['id'] ] =  c['label']
    chan_sched[ c['id'] ] = ''
#
# Get a list of all the Taskomatic repo-sync jobs
#
schedules = client.taskomatic.org.listActiveSchedulesByBunch(key_session, 'repo-sync-bunch')
#
# Build an array of schedules indexed by internal channel id number
#
for s in schedules:
    chan_sched[int(s['data_map']['channel_id'])] =  s['cron_expr']

# Print headers
csched_fmt = '{0:>5s}  {1:<40s} {2:<20s}'
print csched_fmt.format('key', 'Channel Name', 'Update Schedule')
print csched_fmt.format('-----', '---------------------', '---------------')

#
# Sort and print the channel names and associated repo-sync schedule (if any)
#
for key, value in sorted(chan_name.iteritems(), key=lambda (k,v): (v,k)):
    print csched_fmt.format(str(key), value, chan_sched[int(key)])

# Logout from spacewalk

client.auth.logout(key_session)

