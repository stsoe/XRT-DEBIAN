# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
cmake_minimum_required(VERSION 3.16.0)
project(XRT-UPSTREAM)

set(XRT_UPSTREAM_DEBIAN 1)
set(XRT_UPSTREAM 1)

add_subdirectory(xrt)
add_subdirectory(xdna)
