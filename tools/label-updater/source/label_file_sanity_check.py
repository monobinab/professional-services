# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# noinspection PyShadowingNames
def validate_fields(line, projectid, resource, resourceid, sub_resource, sub_resource_id,
                                                  zone):

    if resource is not None and resource.strip().lower() in ('project', 'compute engine', 'bigquery',
                                                             'bigtable', 'storage'):

        if resource == "project" and not projectid:
            invalid_record_flag = True

        elif resource == "compute engine" and (not projectid or not resourceid or not zone):
            invalid_record_flag = True

        elif (resource == "storage" or resource == "bigtable" or resource == "bigquery") and \
                (not projectid or not resourceid):
            invalid_record_flag = True

        else:
            invalid_record_flag = False

    return invalid_record_flag


