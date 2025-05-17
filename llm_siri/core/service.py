import copy

import mlx_lm
from loguru import logger
from ray import serve
from starlette.requests import Request

from llm_siri.models.message import ChatMessage, Message, Response, Role


@serve.deployment(num_replicas="auto")
class LLMService:
    def __init__(self, model_path: str):
        self.model, self.tokenizer = mlx_lm.load(model_path)
        logger.info(f"model loaded: {model_path}")

    def generate(self, messages: list[Message], think=False):
        messages_for_model = copy.deepcopy(messages)
        if think:
            messages_for_model[-1].content += " /think"
        else:
            messages_for_model[-1].content += " /nothink"

        prompt = self.tokenizer.apply_chat_template(
            [msg.model_dump() for msg in messages_for_model],
            add_generation_prompt=True,
        )
        response = mlx_lm.generate(self.model, self.tokenizer, prompt=prompt)
        response = self.post_process(response)
        logger.debug(f"response: {response}")

        messages.append(Message(role=Role.ASSISTANT.value, content=response.response))
        return ChatMessage(messages=messages, response=response)

    def post_process(self, response: str):
        think, resp = response.split("</think>")
        think = think.split("<think>")[-1].strip()
        resp = resp.strip()
        return Response(think=think, response=resp)

    async def __call__(self, http_request: Request):
        request_json = await http_request.json()
        messages = [Message(**msg) for msg in request_json["messages"]]
        return self.generate(messages, request_json["think"])
