#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import fire
import ray

from llm_siri.core.service import LLMService
from llm_siri.models.llm_config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMP,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
    LLMConfig,
)
from llm_siri.utils.logger import setup_logger
from llm_siri.utils.misc import norm_path


def start_ray_server(
    model_path: str,
    temp: float = DEFAULT_TEMP,
    top_p: float = DEFAULT_TOP_P,
    top_k: int = DEFAULT_TOP_K,
    max_tokens: int = DEFAULT_MAX_TOKENS,
):
    ray.init(address="local", include_dashboard=False)
    ray.serve.run(
        LLMService.bind(
            model_path=norm_path(model_path),
            llm_config=LLMConfig(temp=temp, top_p=top_p, top_k=top_k, max_tokens=max_tokens),
        ),
        name="llm-siri",
        blocking=True,
    )


def run():
    setup_logger()
    fire.Fire(start_ray_server)


if __name__ == "__main__":
    run()
