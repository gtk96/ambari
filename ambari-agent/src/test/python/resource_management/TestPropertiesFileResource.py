#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""
import os
import time
from unittest import TestCase
from mock.mock import patch, MagicMock
from resource_management.core import Environment, sudo
from resource_management.core.system import System
from resource_management.libraries import PropertiesFile

@patch.object(System, "os_family", new='redhat')
class TestPropertiesFIleResource(TestCase):
  """
  PropertiesFile="resource_management.libraries.providers.properties_file.PropertiesFileProvider"
  Testing PropertiesFile(PropertiesFileProvider) with different 'properties dictionary'
  """


  @patch("resource_management.core.providers.system._ensure_metadata")
  @patch.object(sudo, "create_file")
  @patch.object(os.path, "exists")
  @patch.object(os.path, "isdir")
  @patch.object(time, "asctime")
  def test_action_create_empty_properties_without_dir(self,
                                                      time_asctime_mock,
                                                      os_path_isdir_mock,
                                                      os_path_exists_mock,
                                                      create_file_mock,
                                                      ensure_mock):
    """
    Tests if 'action_create' - creates new non existent file and write proper data
    1) properties={}
    2) dir=None
    """
    os_path_isdir_mock.side_effect = [False, True]
    os_path_exists_mock.return_value = False
    time_asctime_mock.return_value = 'Today is Wednesday'

    
    

    with Environment('/') as env:
      PropertiesFile('/somewhere_in_system/one_file.properties',
                     dir=None,
                     properties={}
      )

    create_file_mock.assert_called_with('/somewhere_in_system/one_file.properties', u'# Generated by Apache Ambari. Today is Wednesday\n    \n    ')
    ensure_mock.assert_called()


  @patch("resource_management.core.providers.system._ensure_metadata")
  @patch.object(sudo, "create_file")
  @patch.object(os.path, "exists")
  @patch.object(os.path, "isdir")
  @patch.object(time, "asctime")
  def test_action_create_empty_properties_with_dir(self,
                                                   time_asctime_mock,
                                                   os_path_isdir_mock,
                                                   os_path_exists_mock,
                                                   create_file_mock,
                                                   ensure_mock):
    """
    Tests if 'action_create' - creates new non existent file and write proper data
    1) properties={}
    2) dir='Some directory that exist '
    """
    os_path_isdir_mock.side_effect = [False, True]
    os_path_exists_mock.return_value = False
    time_asctime_mock.return_value = 'Some other day'

    
    

    with Environment('/') as env:
      PropertiesFile('file.txt',
                     dir="/dir/and/dir",
                     properties={},
      )

    create_file_mock.assert_called_with('/dir/and/dir/file.txt', u'# Generated by Apache Ambari. Some other day\n    \n    ')
    ensure_mock.assert_called()


  @patch("resource_management.core.providers.system._ensure_metadata")
  @patch.object(sudo, "create_file")
  @patch.object(os.path, "exists")
  @patch.object(os.path, "isdir")
  @patch.object(time, "asctime")
  def test_action_create_properties_simple(self,
                                           time_asctime_mock,
                                           os_path_isdir_mock,
                                           os_path_exists_mock,
                                           create_file_mock,
                                           ensure_mock):
    """
    Tests if 'action_create' - creates new non existent file and write proper data
    1) properties={"Some property":"Some value"}
    2) dir=None
    """

    os_path_isdir_mock.side_effect = [False, True]
    os_path_exists_mock.return_value = False
    time_asctime_mock.return_value = 777

    
    

    with Environment('/') as env:
      PropertiesFile('/dir/new_file',
                     properties={'property1': 'value1'},
      )

    create_file_mock.assert_called_with('/dir/new_file', u'# Generated by Apache Ambari. 777\n    \nproperty1=value1\n    ')
    ensure_mock.assert_called()


  @patch("resource_management.core.providers.system._ensure_metadata")
  @patch.object(sudo, "create_file")
  @patch.object(os.path, "exists")
  @patch.object(os.path, "isdir")
  @patch.object(time, "asctime")
  def test_action_create_properties_with_metacharacters(self,
                                                        time_asctime_mock,
                                                        os_path_isdir_mock,
                                                        os_path_exists_mock,
                                                        create_file_mock,
                                                        ensure_mock):
    """
    Tests if 'action_create' - creates new non existent file and write proper data
    1) properties={"":"", "Some property":"Metacharacters: -%{} ${a.a}/"}
    2) dir=None
    """
    os_path_isdir_mock.side_effect = [False, True]
    os_path_exists_mock.return_value = False
    time_asctime_mock.return_value = 777

    
    

    with Environment('/') as env:
      PropertiesFile('/dir/new_file',
                     properties={"": "",
                                 "prop.1": "'.'yyyy-MM-dd-HH",
                                 "prop.3": "%d{ISO8601} %5p %c{1}:%L - %m%n",
                                 "prop.2": "INFO, openjpa",
                                 "prop.4": "${oozie.log.dir}/oozie.log",
                                 "prop.empty": "",
                     },
      )

    create_file_mock.assert_called_with('/dir/new_file', u"# Generated by Apache Ambari. 777\n    \n=\nprop.1='.'yyyy-MM-dd-HH\nprop.2=INFO, openjpa\nprop.3=%d{ISO8601} %5p %c{1}:%L - %m%n\nprop.4=${oozie.log.dir}/oozie.log\nprop.empty=\n    ")
    ensure_mock.assert_called()


  @patch("resource_management.core.providers.system._ensure_metadata")
  @patch.object(sudo, "read_file")
  @patch.object(sudo, "create_file")
  @patch.object(os.path, "exists")
  @patch.object(os.path, "isdir")
  @patch.object(time, "asctime")
  def test_action_create_properties_rewrite_content(self,
                                                    time_asctime_mock,
                                                    os_path_isdir_mock,
                                                    os_path_exists_mock,
                                                    create_file_mock,
                                                    read_file_mock,
                                                    ensure_mock):
    """
    Tests if 'action_create' - rewrite file that exist
    1) properties={"Some property":"Some value"}
    2) dir="Some dir"
    """
    os_path_isdir_mock.side_effect = [False, True]
    os_path_exists_mock.return_value = True
    time_asctime_mock.return_value = 777

    
    read_file_mock.return_value = 'old-content'
    

    with Environment('/') as env:
      PropertiesFile('new_file',
                     dir='/dir1',
                     properties={'property_1': 'value1'},
      )

    read_file_mock.assert_called()
    create_file_mock.assert_called_with('/dir1/new_file', u'# Generated by Apache Ambari. 777\n    \nproperty_1=value1\n    ')
    ensure_mock.assert_called()
