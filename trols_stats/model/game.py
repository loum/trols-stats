import json

import trols_stats

__all__ = ['Game']


class Game(object):
    """
    .. attribute:: game_id

    """
    _game_id = None
    _round = None
    _sex = None
    _date_played = None
    _player = trols_stats.Player()
    _team_mate = trols_stats.Player()
    _opposition = (trols_stats.Player(), trols_stats.Player())
    _score_for = None
    _score_against = None

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    def __init__(self, game_id=None):
        if game_id is not None:
            self._game_id = game_id

    def to_json(self):
        """Return a json representation of the object.

        """
        obj = {
            'id': self.game_id,
        }

        return json.dumps(obj)
