import json

import trols_stats

__all__ = ['Game']


class Game(object):
    """
    .. attribute:: game_id

    """
    _game_id = None
    _round = None
    _date_played = None
    _player = trols_stats.Player()
    _team_mate = trols_stats.Player()
    _opposition = (trols_stats.Player(), trols_stats.Player())
    _score_for = None
    _score_against = None
    _section = None

    def __init__(self, game_id=None):
        if game_id is not None:
            self._game_id = game_id

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, value):
        self._round = value

    def to_json(self):
        """Return a json representation of the object.

        """
        obj = {
            'id': self.game_id,
        }

        return json.dumps(obj)
