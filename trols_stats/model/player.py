import json

__all__ = ['Player']


class Player(object):
    """
    .. attribute:: player_id

    .. attribute:: name

    .. attribute:: team

    """
    _player_id = None
    _name = None
    _team = None
    _sex = None

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, value):
        self._player_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        self._team = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value

    def __init__(self, player_id=None, name=None, team=None, sex=None):
        if player_id is not None:
            self._player_id = player_id

        if name is not None:
            self._name = name

        if team is not None:
            self._team = team

        if sex is not None:
            self._sex = sex

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        obj = {
            'id': self.player_id,
            'name': self.name,
            'team': self.team,
            'sex': self.sex
        }

        return obj