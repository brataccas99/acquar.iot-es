import unittest
from unittest.mock import MagicMock, Mock, patch
import types
import subprocess
import sys
import os

from dotenv import dotenv_values, load_dotenv

# Get the directory path of bot.py
bot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "bot"))

# Add the bot directory to the Python module search path
sys.path.append(bot_dir)


from bot.bot import (
    lastEat,
    O2,
    first_start,
    send_help,
    generate_data,
    activeSensorsValues,
    sendEmail,
    giveFoodAcquarium,
    waterChange,
    generateO2,
    ONsensors,
    OFFsensors,
    switchSensorOn,
    switchSensorOff,
)

env_vars = dotenv_values(".env")

load_dotenv()

TOKEN = env_vars["BOT_TOKEN"]
CHAT_ID = env_vars["CHAT_ID"]


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = TOKEN
        self.cid = CHAT_ID
        self.message = MagicMock()
        self.message.chat.id = self.cid

    def test_start_command(self):
        message = MagicMock()
        message.from_user.username = "test_user"
        self.bot.send_message = MagicMock()

        first_start(message)

        self.bot.send_message.assert_called_once_with(
            self.cid,
            "Welcome test_user, press /help to get the list of commands",
            parse_mode="Markdown",
        )

    def test_help_command(self):
        self.bot.send_message = MagicMock()
        keyboard_mock = MagicMock()
        types.InlineKeyboardMarkup = MagicMock(return_value=keyboard_mock)
        types.InlineKeyboardButton = MagicMock()

        send_help(self.message)

        self.bot.send_message.assert_called_once_with(
            self.cid, "Choose a command:", reply_markup=keyboard_mock
        )
        types.InlineKeyboardMarkup.assert_called_once_with(row_width=2)
        types.InlineKeyboardButton.assert_has_calls(
            [
                MagicMock(
                    text="retrieve last measurements",
                    callback_data="activeSensorsValues",
                ),
                MagicMock(text="Do Routine", callback_data="generateData"),
                MagicMock(text=" O2", callback_data="O2"),
                MagicMock(text="lastEat", callback_data="lastEat"),
                MagicMock(text="Send Email", callback_data="sendEmail"),
                MagicMock(
                    text="Give Food Acquarium", callback_data="giveFoodAcquarium"
                ),
                MagicMock(text="Clean water", callback_data="waterChange"),
                MagicMock(text="Generate O2", callback_data="generateO2"),
                MagicMock(text="Activate Sensors", callback_data="ONsensors"),
                MagicMock(text="Deactivate Sensors", callback_data="OFFsensors"),
                MagicMock(text="Switch Tank On", callback_data="switchSensorOn"),
                MagicMock(text="Switch Tank Off", callback_data="switchSensorOff"),
            ],
            any_order=True,
        )

    def test_generate_data_command_success(self):
        subprocess.Popen = MagicMock()
        self.bot.send_message = MagicMock()
        lambda_client_mock = MagicMock()
        lambda_client_mock.invoke = MagicMock(return_value={"ResponseMetadata": {}})
        self.boto3.client = MagicMock(return_value=lambda_client_mock)

        generate_data(self.message)

        subprocess.Popen.assert_called_once_with(
            ["node", "current_working_directory\\dist\\device.js"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.bot.send_message.assert_called_once_with(self.cid, "Done!")
        lambda_client_mock.invoke.assert_called_once_with(
            FunctionName="onsensors",
            InvocationType="RequestResponse",
            Payload='{"cid": 123456789}',
        )

    def test_generate_data_command_error(self):
        subprocess.Popen = MagicMock()
        subprocess.Popen.return_value.returncode = 1
        self.bot.send_message = MagicMock()

        generate_data(self.message)

        subprocess.Popen.assert_called_once_with(
            ["node", "current_working_directory\\dist\\device.js"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.bot.send_message.assert_called_once_with(self.cid, "error generating data")

    def test_retrieve_last_measurements_command(self):
        self.bot.send_message = MagicMock()

        activeSensorsValues(self.message)

        self.bot.send_message.assert_called_once_with(
            self.cid, "Retrieving last measurements..."
        )

    def test_O2_command(self):
        self.bot.send_message = MagicMock()

        O2(self.message)

        self.bot.send_message.assert_called_once_with(self.cid, "Checking O2 levels...")

    def test_lastEat_command(self):
        self.bot.send_message = MagicMock()

        lastEat(self.message)

        self.bot.send_message.assert_called_once_with(
            self.cid, "Checking last feed time..."
        )

    @patch("bot.send_email")
    def test_sendEmail(mock_send_email):
        message = Mock()
        message.chat.id = 12345
        message.text = "test@example.com"

        sendEmail(message)

        mock_send_email.assert_called_with(
            "Email from bot_username",
            mock_send_email(),
            "bot_sender_email@example.com",
            "test@example.com",
        )

    @patch("bot.boto3.client")
    def test_giveFoodAcquarium(mock_boto3_client):
        message = Mock()
        message.chat.id = 12345
        message.text = "Tank1"

        giveFoodAcquarium(message)

        mock_boto3_client.assert_called_with(
            "lambda", endpoint_url="http://localhost:4566"
        )
        mock_boto3_client().invoke.assert_called_with(
            FunctionName="giveFoodAcquarium",
            InvocationType="RequestResponse",
            Payload='{"table": "Acquarium", "tank": "Tank1"}',
        )

    @patch("bot.boto3.client")
    def test_waterChange(mock_boto3_client):
        message = Mock()
        message.chat.id = 12345
        message.text = "Tank1"

        waterChange(message)

        mock_boto3_client.assert_called_with(
            "lambda", endpoint_url="http://localhost:4566"
        )
        mock_boto3_client().invoke.assert_called_with(
            FunctionName="waterChange",
            InvocationType="RequestResponse",
            Payload='{"table": "Acquarium", "tank": "Tank1"}',
        )

    @patch("bot.boto3.client")
    def test_generateO2(mock_boto3_client):
        message = Mock()
        message.chat.id = 12345
        message.text = "Tank1"

        generateO2(message)

        mock_boto3_client.assert_called_with(
            "lambda", endpoint_url="http://localhost:4566"
        )
        mock_boto3_client().invoke.assert_called_with(
            FunctionName="generateO2",
            InvocationType="RequestResponse",
            Payload='{"table": "Acquarium", "tank": "Tank1"}',
        )

    @patch("bot.boto3.client")
    def test_ONsensors(mock_boto3_client):
        message = Mock()
        message.chat.id = 12345

        ONsensors(message)

        mock_boto3_client.assert_called_with(
            "lambda", endpoint_url="http://localhost:4566"
        )
        mock_boto3_client().invoke.assert_called_with(
            FunctionName="onsensors",
            InvocationType="RequestResponse",
            Payload='{"cid": 12345}',
        )

    @patch("bot.boto3.client")
    def test_OFFsensors(mock_boto3_client):
        message = Mock()
        message.chat.id = 12345

        OFFsensors(message)

        mock_boto3_client.assert_called_with(
            "lambda", endpoint_url="http://localhost:4566"
        )
        mock_boto3_client().invoke.assert_called_with(
            FunctionName="offSensors",
            InvocationType="RequestResponse",
            Payload='{"cid": 12345}',
        )

    def test_switchSensorOn_command(self):
        self.bot.send_message = MagicMock()

        switchSensorOn(self.message)

        self.bot.send_message.assert_called_once_with(
            self.cid, "Switching sensor ON..."
        )

    def test_switchSensorOff_command(self):
        self.bot.send_message = MagicMock()

        switchSensorOff(self.message)

        self.bot.send_message.assert_called_once_with(
            self.cid, "Switching sensor OFF..."
        )


if __name__ == "__main__":
    unittest.main()
