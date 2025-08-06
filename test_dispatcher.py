import unittest
from unittest.mock import MagicMock, patch

from dispatcher import get_all_link_codes


class TestGetAllLinkCodes(unittest.TestCase):
    @patch("dispatcher.requests.Session")  # remplace requests.Session par un faux
    def test_link_parsing(self, mock_session_class):

        fake_html = """
        <html>
            <a class="participant-link">http://localhost:8000/InitializeParticipant/code1</a>
            <a class="participant-link">http://localhost:8000/InitializeParticipant/code2</a>
            <a class="participant-link">http://localhost:8000/InitializeParticipant/code3</a>
        </html>
        """

        # comportement du "get"
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.text = fake_html
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = get_all_link_codes("blablabla")

        self.assertEqual(result, ["code1", "code2", "code3"])


if __name__ == "__main__":
    unittest.main()
