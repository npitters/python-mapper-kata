class TrackAndFieldDb:
    def __init__(
        self,
        id: str = None,
        name: str = None,
        grade: str = None,
        classification: str = None,
        eventName: int = None,
    ):
        self.id = id
        self.name = name
        self.grade = grade
        self.classification = classification
        self.eventName = eventName

    @staticmethod
    def from_json(json_dict):
        return TrackAndFieldDb(
            id=str(json_dict.get("id")),
            name=json_dict.get("name"),
            grade=json_dict.get("class"),
            classification=json_dict.get("eventClassification"),
            eventName=json_dict.get("eventId"),
        )
