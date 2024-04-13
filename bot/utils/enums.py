from enum import Enum


class RequestStatus(Enum):
    created = 1
    taken_by_volunteer = 2
    partially_fulfilled = 3
    completely_fulfilled = 4
    delivered = 5
    accepted_by_user = 6
    rated_and_ended = 7


class EvacuationRequestStatus(Enum):
    created = 1
    taken_by_volunteer = 2
    details_arranged = 3
    evacuation_ended = 4
    rated_and_ended = 5


class RequestType(Enum):
    psychological = 'Психологічна'
    legal = 'Правова'
    nutrition = 'Харчування'
    military = 'Військова'
    medical = 'Медична'
    clothing = 'Одяг'
    baby = 'Дитяча'
    houshehold = 'Побутові товари'
    equipments = 'Техніка та інструменти'
