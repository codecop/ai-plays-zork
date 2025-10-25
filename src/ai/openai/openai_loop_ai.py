import asyncio
from pathlib import Path
from typing import Optional, Any
from agents import Agent, RunResult, Runner
from with_loop.loop_ai import LoopAi
from util.log import Log


class OpenaiLoopAi(LoopAi):

    def __init__(self, configuration: str, run_folder: Path, log: Log):
        super().__init__(configuration, run_folder, log)

        self.agent: Optional[Agent[Any]] = None
        self.last_response: Optional[RunResult] = None
        self.calls = 0

    def file(self) -> Path:
        return Path(__file__)

    def start(self, game_notes: str, game_intro: str) -> None:
        system_prompt = self.load_resource("system_prompt.md").format(
            game_notes=game_notes, game_intro=game_intro
        )
        self.write_run_resource("system_prompt.md", system_prompt)

        self.agent = Agent(
            model=self.config()["model"],
            name=self.config()["name"],
            instructions=system_prompt,
            # description=self.config()["description"],
            # tools=self.config()["tools"],
        )
        self._log_agent_info()

    def _log_agent_info(self) -> None:
        if self.agent is None:
            raise RuntimeError("Agent not initialized")
        self.log.ai(
            f"ai: {self.__class__}\n"
            + f"configuration: {self.configuration}\n"
            + f"model: {self.agent.model}\n"
            + f"name: {self.agent.name}"
        )

    def get_next_command(self, context: str) -> str:
        prompt = f"Game answers with {context}"

        loop = self._event_loop()
        response = loop.run_until_complete(self._send_prompt_to_server(prompt))

        return self._handle_response(response)

    def _event_loop(self):
        try:
            # For Python 3.10+, use new asyncio policy
            if hasattr(asyncio, "get_running_loop"):
                return asyncio.get_running_loop()

            # Fallback for older Python versions
            return asyncio.get_event_loop()
        except RuntimeError:
            # return asyncio.new_event_loop()
            return asyncio.get_event_loop()

    async def _send_prompt_to_server(self, prompt: str) -> RunResult:
        if self.agent is None:
            raise RuntimeError("Agent not initialized")
        if not self.last_response:
            response = await Runner.run(self.agent, prompt)
            self.last_response = response
        else:
            new_input = self.last_response.to_input_list() + [
                {"role": "user", "content": prompt}
            ]
            response = await Runner.run(self.agent, new_input)
            self.last_response = response

        return response

    def _handle_response(self, response: RunResult) -> str:
        # self.log.ai("Response: " + str(response))
        if not response.final_output or len(response.final_output) == 0:
            self.log.ai("NO RESPONSE")
            return "NO RESPONSE"

        content = response.final_output
        self.calls += 1
        return self._extract_command_from(content)

    def _extract_command_from(self, content: str) -> str:
        if "\n" in content:
            self.log.ai(content)
            content = content.splitlines()[-1]
        return content
