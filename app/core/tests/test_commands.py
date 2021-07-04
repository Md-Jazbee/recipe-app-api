from unittest.mock import call, patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count,1)

            
    # check to connections handler raises the operational error it wait aan does raise operational error
    # then it can raise the operational error and try again
    # remove that delay by doing this 
    @patch('time.sleep',return_value=True)
    def test_wait_for_db(self,ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 +[True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count,6) 
