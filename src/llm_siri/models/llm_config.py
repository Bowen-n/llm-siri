from pydantic import BaseModel, Field

DEFAULT_TEMP = 0.6
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 20
DEFAULT_MAX_TOKENS = 8192


class LLMConfig(BaseModel):
    # ref: https://arxiv.org/pdf/2505.09388
    temp: float = Field(default=DEFAULT_TEMP)
    top_p: float = Field(default=DEFAULT_TOP_P)
    top_k: int = Field(default=DEFAULT_TOP_K)
    max_tokens: int = Field(default=DEFAULT_MAX_TOKENS)
