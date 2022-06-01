#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("OP_MS_TEAMS_PYTHON_BOT_APP_ID", "")
    APP_PASSWORD = os.environ.get("OP_MS_TEAMS_PYTHON_BOT_APP_PASSWORD", "")
    CONN_STRING = os.environ.get("OP_MS_TEAMS_PYTHON_BOT_CONN_STRING", "")
