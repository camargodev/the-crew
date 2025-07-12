from dataclasses import dataclass, field
from src.game.mission_rules import MissionRule

@dataclass(frozen=True)
class GameMissionsData:
    """
    Represents the data for mission on the game

    Attributes:
        all_missions (set[MissionRule]): A set with all missions
        missing_missions (set[MissionRule]): A set with missing missions
        sucessfull_missions (set[MissionRule]): A set with sucesfull missions
        failed_missions (set[MissionRule]): A set with failes missions
    """
    all_missions: set[MissionRule]
    missing_missions: set[MissionRule]
    sucessfull_missions: set[MissionRule] = field(default_factory=set)
    failed_missions: set[MissionRule] = field(default_factory=set)

    @classmethod
    def make(cls, missions: set[MissionRule]):
        """
        Static factory method to create a GameMissionsData object

        Args:
            missions (set[MissionRule]): the missions that need to be completed

        Returns:
           GameMissionsData with missions on all_missions and missing_missions
        """
        missing_missions = set(mission for mission in missions)
        return GameMissionsData(all_missions=missions, missing_missions=missing_missions)

    def are_missions_complete(self) -> bool:
        """
        Check if all missions are sucessfully completed

        Returns:
          true if all missions were completed and none is failed
        """
        are_all_missions_completed = len(self.sucessfull_missions) == len(self.all_missions)
        return (not self.has_any_failed_mission()) and are_all_missions_completed

    def has_any_failed_mission(self) -> bool:
        """
        Check if any mission failed

        Returns:
          true if a mission failed
        """
        return len(self.failed_missions) != 0

    def add_failed_mission(self, failed_mission: MissionRule):
        """
        Add a failed mission

        Args:
            mission (MissionRule): the missions that failed
        """
        self.failed_missions.add(failed_mission)
        self.missing_missions.remove(failed_mission)

    def add_sucessfull_mission(self, sucessfull_mission: MissionRule):
        """
        Add a sucessfull mission

        Args:
            mission (MissionRule): the missions that succeeded
        """
        self.sucessfull_missions.add(sucessfull_mission)
        self.missing_missions.remove(sucessfull_mission)
