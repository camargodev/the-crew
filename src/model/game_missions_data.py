from dataclasses import dataclass, field
from src.model.round_data import RoundData
from src.model.card import Card
from src.game.mission_engine import MissionRule

@dataclass(frozen=True)
class GameMissionsData:
    """
    Represents the data for mission on the gam

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
        missing_missions = set(mission for mission in missions)
        return GameMissionsData(all_missions=missions, missing_missions=missing_missions)

    def are_missions_complete(self) -> bool:
        return len(self.failed_missions) == 0 and len(self.sucessfull_missions) == len(self.all_missions)
    
    def has_any_failed_mission(self) -> bool:
        return len(self.failed_missions) != 0
    
    def add_failed_mission(self, failed_mission: MissionRule):
        self.failed_missions.add(failed_mission)
        self.missing_missions.remove(failed_mission)

    def add_sucessfull_mission(self, sucessfull_mission: MissionRule):
        self.sucessfull_missions.add(sucessfull_mission)
        self.missing_missions.remove(sucessfull_mission)
