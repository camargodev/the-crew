from dataclasses import dataclass, field
from src.game.mission_rules import MissionRule

@dataclass(frozen=True)
class MissionsOrderData:
    """
    Represents the ordering rules for mission completion

    Attributes:
        must_come_before (dict[MissionRule, set[MissionRule]]): 
            Maps a mission to the set of missions that must come after it.
        fixed_positions (dict[MissionRule, int]):
            Maps a mission to its fixed position (0-based index).
    """
    must_come_before: dict[MissionRule, set[MissionRule]] = field(default_factory=dict)
    fixed_positions: dict[MissionRule, int] = field(default_factory=dict)

    def is_order_respected(self, satisfied: list[MissionRule], new: MissionRule) -> bool:
        """
        Check if the order constraints are respected when satisfying a new mission

        Args:
            satisfied (list[MissionRule]): The list of missions already satisfied, in order.
            new (MissionRule): The mission that was just satisfied.

        Returns:
            bool: True if order constraints are respected for this mission.
        """
        satisfied_set = set(satisfied)

        # Check prerequisites (missions that must come before 'new')
        for prerequisite, blocked in self.must_come_before.items():
            if new in blocked and prerequisite not in satisfied_set:
                return False

        # Check fixed position (if it exists)
        if new in self.fixed_positions:
            # Expected order position is 1-indexed
            # To be mission 1, for example, the satisfied array should be empty
            expected_position = self.fixed_positions[new]
            current_position = len(satisfied) + 1
            if current_position != expected_position:
                return False

        return True

    @classmethod
    def builder(cls):
        """
        Create a new builder instance for MissionsOrderData.

        Returns:
            _MissionsOrderDataBuilder: A builder to incrementally construct MissionsOrderData.
        """
        return _MissionsOrderDataBuilder()

    @classmethod
    def empty(cls):
        """
        Create an empty MissionsOrderData instance with no constraints.

        Returns:
            MissionsOrderData: An instance with no order or position restrictions.
        """
        return MissionsOrderData.builder().build()


class _MissionsOrderDataBuilder:
    def __init__(self):
        self._must_come_before: dict[MissionRule, set[MissionRule]] = {}
        self._fixed_positions: dict[MissionRule, int] = {}

    def add_order_constraint(self, before: MissionRule, after: MissionRule):
        """
        Add a constraint that `before` must be satisfied before `after`.
        """
        self._must_come_before.setdefault(before, set()).add(after)
        return self

    def set_fixed_position(self, mission: MissionRule, position: int):
        """
        Fix the mission to a specific position in the list (0-based index).
        """
        self._fixed_positions[mission] = position
        return self

    def build(self) -> MissionsOrderData:
        """
        Returns the built MissionsOrderData.
        """
        return MissionsOrderData(
            must_come_before=self._must_come_before,
            fixed_positions=self._fixed_positions
        )
