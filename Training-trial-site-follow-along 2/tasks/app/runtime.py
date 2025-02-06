"""
runtime.py file

DEFAULT entry point file to the ProCaaSo Programmers Framework API. YOU DO NOT NEED TO EDIT THIS FILE. 

Overview:
1. Import necessary libraries
2. Initialize the ProCaaSo-Log Library to be used globally in the App Task
3. Initialize the ProCaaSo Programmers Framework API Library to be imported
   to our App and IO Tasks in two cases:
    a. Local Debug
    b. Sidecar 
"""
# Necessary imports to access the ProCaaSo Programmers Framework API (procaaso_client), ProCaaSo Log Library, 
# and Process Environment (os) 
from procaaso_client.synchronous.application import SyncApplication
from procaaso_client.synchronous.client import SyncHarnessClient
from procaaso_client.core.http_clients import SyncHttpClient
import procaaso_log
import os

"""
Configure the procaaso-log library. This allows us to set debug statements on different levels.
Levels (High to low priority): FATAL, CRITICAL, ERROR, WARNING, INFO, DEBUG

Currently, ProCaaSo's defaulted to only show logs above the DEBUG levels on the Trend UI

Caution -- Excessive logging can consume resources and potentially cause performance issues
or other internal problems. It's wise to be mindful of the volume and verbosity of logs
generated to maintain system health and performance.

"""

# # Logging configuration for development
# logger = procaaso_log.get_logger("app.ens")
# config = procaaso_log.standard_config("app", "procaaso_client", level="DEBUG", env="DEV")

# Logging configuration for deployment
config = procaaso_log.standard_config("app", "procaaso_client")
logger = procaaso_log.get_logger("app.ens")

local_debug = None

# Access environment variables
local_debug = os.environ.get("LOCAL_DEBUG")
if local_debug != None:
    # Init Client
    http_sync = SyncHttpClient("http://localhost:5060")
    sync = SyncHarnessClient(http_sync)
    app = SyncApplication(sync)
else:
    # Init Client
    http_sync = SyncHttpClient(
        "http://paracloud-edge-sidecar.paracloud.svc.cluster.local:5060"
    )
    sync = SyncHarnessClient(http_sync)
    app = SyncApplication(sync)