from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Exit:
    direction: str
    destination_room_name: Optional[str]
    was_taken: bool = False

    def mark_as_taken(self) -> "Exit":
        return Exit(
            direction=self.direction,
            destination_room_name=self.destination_room_name,
            was_taken=True,
        )

    def set_destination(self, destination_room_name: str) -> "Exit":
        return Exit(
            direction=self.direction,
            destination_room_name=destination_room_name,
            was_taken=self.was_taken,
        )
