class TrackAndFieldDb:
    def __init__(
        self,
        id: str = None,
        name: str = None,
        grade: str = None,
        classification: str = None,
        event_name: int = None,
        personal_best: int = None,
    ):
        self.id = id
        self.name = name
        self.grade = grade
        self.classification = classification
        self.event_name = event_name
        self.personal_best = personal_best

    @staticmethod
    def from_json(json_dict):
        return TrackAndFieldDb(
            id=str(json_dict.get("id")),
            name=json_dict.get("name"),
            grade=json_dict.get("class"),
            classification=json_dict.get("eventClassification"),
            event_name=json_dict.get("eventId"),
            personal_best=json_dict.get("eventTypeId"),
        )
