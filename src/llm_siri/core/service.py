import copy

import mlx_lm
from loguru import logger
from mlx_lm.sample_utils import make_sampler
from ray import serve
from starlette.requests import Request

from llm_siri.models.llm_config import LLMConfig
from llm_siri.models.message import ChatMessage, Message, Response, Role
from llm_siri.utils.logger import get_logger

logger = get_logger()


@serve.deployment(num_replicas="auto")
class LLMService:
    def __init__(self, model_path: str, llm_config: LLMConfig):
        self.llm_config = llm_config
        self.model, self.tokenizer = mlx_lm.load(model_path)
        logger.info(f"model loaded: {model_path}")
        logger.info(f"config: {llm_config}")
        self.sampler = make_sampler(
            temp=llm_config.temp,
            top_p=llm_config.top_p,
            top_k=llm_config.top_k,
            xtc_special_tokens=self.tokenizer.encode("\n") + list(self.tokenizer.eos_token_ids),
        )

    def generate(self, messages: list[Message], think=False) -> ChatMessage:
        messages_for_model = copy.deepcopy(messages)
        if think:
            messages_for_model[-1].content += " /think"
        else:
            messages_for_model[-1].content += " /nothink"

        prompt = self.tokenizer.apply_chat_template(
            [msg.model_dump() for msg in messages_for_model],
            add_generation_prompt=True,
        )
        response = mlx_lm.generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=self.llm_config.max_tokens,
            sampler=self.sampler,
        )
        response = self.post_process(response)
        logger.debug(f"response: {response}")

        messages.append(Message(role=Role.ASSISTANT.value, content=response.response))
        return ChatMessage(messages=messages, response=response)

    def post_process(self, response: str) -> Response:
        think, resp = response.split("</think>")
        think = think.split("<think>")[-1].strip()
        resp = resp.strip()
        return Response(think=think, response=resp)

    async def __call__(self, http_request: Request) -> str:
        request_json = await http_request.json()
        messages = [Message(**msg) for msg in request_json["messages"]]
        chat_message = self.generate(messages, request_json["think"])
        return chat_message.model_dump_json()
