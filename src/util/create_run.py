from pathlib import Path
from typing import Tuple
from util.composite_log import CompositeLog
from util.individual_log import IndividualLog
from util.log import Log
from util.nice_log import NiceLog
from util.file_utils import next_folder_name


def create_run(config: str, scope="loop", base_path=".") -> Tuple[Path, Log]:
    """Create the run folder and log writing into it."""

    base_name = f"{scope}_{config}"
    run_folder = next_folder_name(Path(base_path) / "runs", base_name)
    log = CompositeLog(NiceLog(run_folder), IndividualLog(run_folder, ""))

    return run_folder, log
