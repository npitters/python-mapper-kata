class TrackAndFieldDb:
    def __init__(
        self, 
        id: str = None,
        name: str = None
    ):
        self.id = id
        self.name = name

    @staticmethod
    def from_json(json_dict):
        return TrackAndFieldDb(
            id = str(json_dict.get("id")),
            name = json_dict.get("name"),
        )
