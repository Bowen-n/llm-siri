#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os

from llm_siri.core.service import LLMService
from llm_siri.utils import norm_path

llm_service_app = LLMService.bind(model_path=norm_path(os.getenv("MODEL_PATH")))
