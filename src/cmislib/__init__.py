#
#      Licensed to the Apache Software Foundation (ASF) under one
#      or more contributor license agreements.  See the NOTICE file
#      distributed with this work for additional information
#      regarding copyright ownership.  The ASF licenses this file
#      to you under the Apache License, Version 2.0 (the
#      "License"); you may not use this file except in compliance
#      with the License.  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing,
#      software distributed under the License is distributed on an
#      "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#      KIND, either express or implied.  See the License for the
#      specific language governing permissions and limitations
#      under the License.
#

"""
Patch httplib2 before the its import to work around a bug into alfresco
https://issues.alfresco.com/jira/browse/MNT-15819
"""
import wrapt
@wrapt.patch_function_wrapper('httplib2', '_parse_www_authenticate')
def wrapper(wrapped, instance, args, kwargs):
    headers = kwargs.get('headers') or args[0]
    headername = kwargs.get('headername') or  args[1]
    if headername == 'www-authenticate' and headers.has_key(headername):
        authenticate = headers[headername].strip()
        if len(authenticate.split(" ")) < 2:
            # A BUG into alfresco generates non RFC compliant
            # 'www-authenticate' header
            # https://issues.alfresco.com/jira/browse/MNT-15819
            # work around this bug and but force Basic auth into the supported
            # authentication
            authenticate = authenticate + ' , Basic realm=""'
            headers[headername] = authenticate
            return wrapped(headers, headername)
    return wrapped(*args, **kwargs)

"""
Define package contents so that they are easy to import.
"""

from cmislib.model import CmisClient
from cmislib.domain import Repository, Folder
from cmislib.cmis_services import Binding, RepositoryServiceIfc

__all__ = ["Binding", "CmisClient", "RepositoryServiceIfc", "Repository", "Folder"]
