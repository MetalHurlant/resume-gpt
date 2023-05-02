from unittest.mock import patch
from app.db_api import SQLAPI

@patch('sqlite3.connect')
class TestDBApi:
    def test_one(self, connect):
        testy = SQLAPI()
        # assert connect.called
        connect.assert_called_once_with("./fixtures/chatbot.db")
        print(testy)
        assert 1 == 1
