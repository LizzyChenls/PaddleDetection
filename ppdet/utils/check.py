# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

import paddle
import six
import paddle.version as paddle_version

from .logger import setup_logger
logger = setup_logger(__name__)

__all__ = [
    'check_gpu', 'check_npu', 'check_xpu', 'check_mlu', 'check_gcu', 'check_version',
    'check_config'
]


def check_mlu(use_mlu):
    """
    Log error and exit when set use_mlu=true in paddlepaddle
    cpu/gpu/xpu/npu version.
    """
    err = "Config use_mlu cannot be set as true while you are " \
          "using paddlepaddle cpu/gpu/xpu/npu version ! \nPlease try: \n" \
          "\t1. Install paddlepaddle-mlu to run model on MLU \n" \
          "\t2. Set use_mlu as false in config file to run " \
          "model on CPU/GPU/XPU/NPU"

    try:
        if use_mlu and not paddle.is_compiled_with_mlu():
            logger.error(err)
            sys.exit(1)
    except Exception as e:
        pass


def check_npu(use_npu):
    """
    Log error and exit when set use_npu=true in paddlepaddle
    version without paddle-custom-npu installed.
    """
    err = "Config use_npu cannot be set as true while you are " \
          "using paddlepaddle version without paddle-custom-npu " \
          "installed! \nPlease try: \n" \
          "\t1. Install paddle-custom-npu to run model on NPU \n" \
          "\t2. Set use_npu as false in config file to run " \
          "model on other devices supported."

    try:
        if use_npu and not 'npu' in paddle.device.get_all_custom_device_type():
            logger.error(err)
            sys.exit(1)
    except Exception as e:
        pass


def check_xpu(use_xpu):
    """
    Log error and exit when set use_xpu=true in paddlepaddle
    cpu/gpu/npu version.
    """
    err = "Config use_xpu cannot be set as true while you are " \
          "using paddlepaddle cpu/gpu/npu version ! \nPlease try: \n" \
          "\t1. Install paddlepaddle-xpu to run model on XPU \n" \
          "\t2. Set use_xpu as false in config file to run " \
          "model on CPU/GPU/NPU"

    try:
        if use_xpu and not paddle.is_compiled_with_xpu():
            logger.error(err)
            sys.exit(1)
    except Exception as e:
        pass


def check_gpu(use_gpu):
    """
    Log error and exit when set use_gpu=true in paddlepaddle
    cpu version.
    """
    err = "Config use_gpu cannot be set as true while you are " \
          "using paddlepaddle cpu version ! \nPlease try: \n" \
          "\t1. Install paddlepaddle-gpu to run model on GPU \n" \
          "\t2. Set use_gpu as false in config file to run " \
          "model on CPU"

    try:
        if use_gpu and not paddle.is_compiled_with_cuda():
            logger.error(err)
            sys.exit(1)
    except Exception as e:
        pass

def check_gcu(use_gcu):
    """
    Log error and exit when set use_gcu=true in paddlepaddle
    version without paddle-custom-gcu installed.
    """
    err = "Config use_gcu cannot be set as true while you are " \
          "using paddlepaddle version without paddle-custom-gcu " \
          "installed! \nPlease try: \n" \
          "\t1. Install paddle-custom-gcu to run model on GCU \n" \
          "\t2. Set use_gcu as false in config file to run " \
          "model on other devices supported."

    try:
        if use_gcu and not 'gcu' in paddle.device.get_all_custom_device_type():
            logger.error(err)
            sys.exit(1)
    except Exception as e:
        pass

def check_version(version='2.2'):
    """
    Log error and exit when the installed version of paddlepaddle is
    not satisfied.
    """
    err = "PaddlePaddle version {} or higher is required, " \
          "or a suitable develop version is satisfied as well. \n" \
          "Please make sure the version is good with your code.".format(version)

    version_installed = [
        paddle_version.major, paddle_version.minor, paddle_version.patch,
        paddle_version.rc
    ]

    if version_installed == ['0', '0', '0', '0']:
        return

    version_split = version.split('.')

    length = min(len(version_installed), len(version_split))
    for i in six.moves.range(length):
        if version_installed[i] > version_split[i]:
            return
        if version_installed[i] < version_split[i]:
            raise Exception(err)


def check_config(cfg):
    """
    Check the correctness of the configuration file. Log error and exit
    when Config is not compliant.
    """
    err = "'{}' not specified in config file. Please set it in config file."
    check_list = ['architecture', 'num_classes']
    try:
        for var in check_list:
            if not var in cfg:
                logger.error(err.format(var))
                sys.exit(1)
    except Exception as e:
        pass

    if 'log_iter' not in cfg:
        cfg.log_iter = 20

    return cfg
