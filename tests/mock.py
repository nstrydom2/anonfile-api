import json

from unittest.mock import patch, Mock, MagicMock

from requests import Response


class MockData:
    @staticmethod
    def get_json_response(raw_obj):
        json_response = Mock(spec=Response)
        json_response.__enter__ = MagicMock(return_value=json_response)
        json_response.__exit__ = MagicMock()
        json_response.status_code = 200
        json_response.json.return_value = json.dumps(raw_obj)
        return json_response

    @staticmethod
    def get_html_response(filename):
        with open(filename, "r", encoding="utf-8") as html_file:
            html_response = Mock(spec=Response)
            html_response.__enter__ = MagicMock(return_value=html_response)
            html_response.__exit__ = MagicMock()
            html_response.status_code = 200
            html_response.text = html_file.read()
            return html_response

    @staticmethod
    def get_file_response(filename):
        with open(filename, "rb") as file:
            file_response = Mock(spec=Response)
            file_response.__enter__ = MagicMock(return_value=file_response)
            file_response.__exit__ = MagicMock()
            file_response.status_code = 200
            file_response.iter_content.return_value = (chunk for chunk in file.read())
            return file_response
