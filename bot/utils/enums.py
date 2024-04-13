from enum import Enum


class RequestStatus(Enum):
    created = 1
    taken_by_volunteer = 2
    partially_fulfilled = 3
    completely_fulfilled = 4
    delivered = 5
    accepted_by_user = 6
    rated_and_ended = 7
