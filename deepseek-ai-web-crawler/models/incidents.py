from pydantic import BaseModel


class Incident(BaseModel):
    """
    Represents the data structure of a Venue.
    """

    zone_type: str
    latitude: float
    longitude: float
    radius: float
    title: str
    description: str
    timestamp: str
