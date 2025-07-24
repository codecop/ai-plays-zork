import subprocess
import time
from pathlib import Path
from ai_interface import AiInterface
from log import Log


class ClaudeCodeAi(AiInterface):
    
    def __init__(self, configuration: str, run_folder: Path, log: Log):
        super().__init__(configuration, run_folder, log)
        self.context_file = "context.md"
        self.output_file = run_folder / "output.txt"
        self.timeout_seconds = 30

    def start(self, game_notes: str, game_intro: str) -> None:
        project_content = self.load_resource("project.md")
        self.write_run_resource("project.md", project_content)
        self.write_run_resource("Zork Gameplay Notes.txt", game_notes)
        initial_context = f"""Wait for first game state"""
        self.write_run_resource("context.md", initial_context)
        
        self.log.ai(
            f"ai: {self.__class__}\n"
            + f"configuration: {self.configuration}\n"
            + f"run_folder: {self.run_folder}"
        )

        print("cd " + str(self.run_folder))
        print("claude --dangerously-skip-permissions \"read project.md and follow the instructions\"")
        # TODO maybe we can do that automatically
        input("Press when Claude has started")

    def get_next_command(self, context: str) -> str:
        if self.output_file.exists():
            self.output_file.unlink()

        self.write_run_resource(self.context_file, context)
        
        try:
            subprocess.run([
                "/Users/ladak/ai/tools/claude-tell.sh",
                self.run_folder,
                "'there is a new context, process it and create another output file with your action, then stop'"
            ],
            cwd=self.run_folder,
            input="",
            text=True,
            timeout=self.timeout_seconds,
            check=True
            )
        except subprocess.SubprocessError as e:
            self.log.ai(f"Claude Code subprocess error: {e}")
            # TODO: fatal stop processing
            return "xxx"
        
        # Wait for output.txt to appear and read it
        command = self._wait_for_output()
        return command.strip() if command else "look"

    def _wait_for_output(self) -> str:
        """Wait for output.txt to appear and return its content."""
        max_wait = self.timeout_seconds
        wait_interval = 0.5
        waited = 0
        
        while waited < max_wait:
            if self.output_file.exists() and self.output_file.stat().st_size > 0:
                command = self.load_run_resource("output.txt").strip()
                return command

            time.sleep(wait_interval)
            waited += wait_interval
        
        self.log.ai("Timeout waiting for Claude Code output")
        return "xxx"  # fallback command

    def close(self) -> None:
        # Clean up any remaining files if needed
        pass