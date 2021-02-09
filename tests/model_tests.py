"""Model tests for call_forward_flask application."""
from .base import BaseTest

from call_forward_flask.models import (
    State,
    Zipcode,
)


class ModelTests(BaseTest):
    """Tests for our call_forward_flask models."""

    def test_zipcode_state_id(self):
        """Test that the state_id property on Zipcode works as expected."""
        bridgeport_zip = '60616'
        il_state_id = State.query.filter_by(name='IL').first().id
        bzip = Zipcode.query.filter_by(zipcode=bridgeport_zip).first()
        bzip_id = bzip.state_id

        self.assertEqual(bzip_id, il_state_id)
