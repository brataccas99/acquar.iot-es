import unittest
from unittest.mock import MagicMock
import telebot, types
import subprocess
from dotenv import dotenv_values, load_dotenv

env_vars = dotenv_values(".env")
TOKEN = env_vars["BOT_TOKEN"]
CHAT_ID = env_vars["CHAT_ID"]


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = telebot.TeleBot(TOKEN)
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

    # Add more test cases for other functions


if __name__ == "__main__":
    unittest.main()
