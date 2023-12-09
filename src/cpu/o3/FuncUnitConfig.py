# Copyright (c) 2010, 2017, 2020 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright (c) 2006-2007 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.SimObject import SimObject
from m5.defines import buildEnv
from m5.params import *

from m5.objects.FuncUnit import *

# AES-128
AES128 = 40

# Simon-128/128
SIMON128128 = 20

# Qarma11-128-o1
QARMA11 = 12

# IMPORTANT: Always toggle this variable and this variable only
ENCRYPTION_LATENCY = AES128

# Default FUDesc opLat is 1 (what's used for the ALU)

# === Sequestered Encryption === #

# EECS 573

class EncDec(FUDesc):
    opList = [
        OpDesc(opClass="EncDec", opLat=ENCRYPTION_LATENCY)
        ]
    count = 1

class EncIntAlu(FUDesc):
    opList = [
        OpDesc(opClass="EncIntAlu", opLat=ENCRYPTION_LATENCY*2+3)
        ]
    count = 1

class EncIntMult(FUDesc):
    opList = [
        OpDesc(opClass="EncIntMult", opLat=ENCRYPTION_LATENCY*2+5)
        ]
    count = 1

# Dummy functional unit for approx. PIR-read latencies
# L2 Cache is 20 cycles, so let's use that as a baseline
# If it's too high, we can try 0, even if we're not simulating with caches
# MAX(DecLat - MemLat, 0) + Arr. Size - 1
# We're assuming an avg. extra cycle per element
MEM_LATENCY = 20
MINSPAN = ENCRYPTION_LATENCY - MEM_LATENCY + 100 - 1
BOYERMOORE = ENCRYPTION_LATENCY - MEM_LATENCY + 400 - 1
KNAPSACK = ENCRYPTION_LATENCY - MEM_LATENCY + 251 - 1
FLOODFILL = ENCRYPTION_LATENCY - MEM_LATENCY + 100 - 1
class EncMem(FUDesc):
    opList = [
        OpDesc(opClass="EncMem", opLat=MINSPAN)
        ]
    count = 1

# === Standard gem5 Units === #

class IntALU(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu")
        ]
    count = 6


class IntMultDiv(FUDesc):
    opList = [
        OpDesc(opClass="IntMult", opLat=3),
        OpDesc(opClass="IntDiv", opLat=20, pipelined=False),
    ]

    count = 2


class FP_ALU(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd", opLat=2),
        OpDesc(opClass="FloatCmp", opLat=2),
        OpDesc(opClass="FloatCvt", opLat=2),
    ]
    count = 4


class FP_MultDiv(FUDesc):
    opList = [
        OpDesc(opClass="FloatMult", opLat=4),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatMisc", opLat=3),
        OpDesc(opClass="FloatDiv", opLat=12, pipelined=False),
        OpDesc(opClass="FloatSqrt", opLat=24, pipelined=False),
    ]
    count = 2


class SIMD_Unit(FUDesc):
    opList = [
        OpDesc(opClass="SimdAdd"),
        OpDesc(opClass="SimdAddAcc"),
        OpDesc(opClass="SimdAlu"),
        OpDesc(opClass="SimdCmp"),
        OpDesc(opClass="SimdCvt"),
        OpDesc(opClass="SimdMisc"),
        OpDesc(opClass="SimdMult"),
        OpDesc(opClass="SimdMultAcc"),
        OpDesc(opClass="SimdMatMultAcc"),
        OpDesc(opClass="SimdShift"),
        OpDesc(opClass="SimdShiftAcc"),
        OpDesc(opClass="SimdDiv"),
        OpDesc(opClass="SimdSqrt"),
        OpDesc(opClass="SimdFloatAdd"),
        OpDesc(opClass="SimdFloatAlu"),
        OpDesc(opClass="SimdFloatCmp"),
        OpDesc(opClass="SimdFloatCvt"),
        OpDesc(opClass="SimdFloatDiv"),
        OpDesc(opClass="SimdFloatMisc"),
        OpDesc(opClass="SimdFloatMult"),
        OpDesc(opClass="SimdFloatMultAcc"),
        OpDesc(opClass="SimdFloatMatMultAcc"),
        OpDesc(opClass="SimdFloatSqrt"),
        OpDesc(opClass="SimdReduceAdd"),
        OpDesc(opClass="SimdReduceAlu"),
        OpDesc(opClass="SimdReduceCmp"),
        OpDesc(opClass="SimdFloatReduceAdd"),
        OpDesc(opClass="SimdFloatReduceCmp"),
    ]
    count = 4


class PredALU(FUDesc):
    opList = [OpDesc(opClass="SimdPredAlu")]
    count = 1

# class EncRdWrPort(FUDesc):  # EECS 573
#     opList = [
#         OpDesc(opClass="EncMem", opLat=ENCRYPTION_LATENCY*2+1)
#         ]
#     count = 1

class ReadPort(FUDesc):
    opList = [OpDesc(opClass="MemRead"), OpDesc(opClass="FloatMemRead")]
    count = 0


class WritePort(FUDesc):
    opList = [OpDesc(opClass="MemWrite"), OpDesc(opClass="FloatMemWrite")]
    count = 0


class RdWrPort(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="FloatMemWrite"),
    ]
    count = 4


class IprPort(FUDesc):
    opList = [OpDesc(opClass="IprAccess", opLat=3, pipelined=False)]
    count = 1