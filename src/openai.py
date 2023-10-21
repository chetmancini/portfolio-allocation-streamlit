import os
from typing import Optional

import openai

from src.allocation import SecurityAllocation


class OpenAIClient:

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def _lookup_allocation_args(self, symbol: str):
        return {
            "model": "gpt-3.5-turbo-0613",
            "messages": [
                {"role": "user",
                 "content": f"Give me an asset allocation breakdown for {symbol}. "
                            f"Give data as an integer percentage for the funds assets (stocks vs bonds), "
                            f"the market cap, usa vs international, and growth vs value. "
                            f"If it's a blend use 50-50 for growth / value."}
            ],
            "functions": [
                {
                    "name": "get_answer_for_user_query",
                    "description": "Get user answer in series of steps. "
                                   "First the name, "
                                   "then the fund asset allocation percentage of stocks and bonds (if it is a fund), "
                                   "then the market cap weighting, "
                                   "then percent us and international, then if it's growth or value, "
                                   "and finally the economic status breakdown of the portfolio's holdings "
                                   "(developed, emerging, or frontier)",
                    "parameters": SecurityAllocation.model_json_schema()
                }
            ],
            "function_call": {"name": "get_answer_for_user_query"}          
        }


    def lookup_allocation(self, symbol: str):
        response = openai.ChatCompletion.create(**self._lookup_allocation_args(symbol))
        return SecurityAllocation.model_validate_json(response.choices[0]["message"]["function_call"]["arguments"])

    async def lookup_allocation_async(self, symbol: str):
        response = await openai.ChatCompletion.acreate(**self._lookup_allocation_args(symbol))
        return SecurityAllocation.model_validate_json(response.choices[0]["message"]["function_call"]["arguments"])