import json
import os
import telebot
import boto3
from dotenv import dotenv_values, load_dotenv
from botocore.exceptions import NoCredentialsError
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import subprocess
import schedule


# Load variables from .env file
env_vars = dotenv_values(".env")

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
url = "http://localhost:4566"

bot = telebot.TeleBot(TOKEN)
dynamoDb = boto3.resource("dynamodb", endpoint_url=url)


def query_data_dynamodb(table):
    measurementTable = dynamoDb.Table(table)
    response = measurementTable.scan()
    return response["Items"]


def format_message(result):
    formatted_message = ""
    for item in result:
        tank = item["tank"]
        O2 = item["O2"]
        lastEat = item["lastEat"]
        waterChange = item["waterChange"]
        daytime = item["dayTime"].split(",")[0]  # Extracting only the date portion

        formatted_message += f"- {tank}: O2: {O2}, lastEat: {lastEat}, waterChange: {waterChange} ,daytime: {daytime}\n"

    return formatted_message


def retrieveO2(result):
    formatted_message = ""
    for item in result:
        tank = item["tank"]
        O2 = item["O2"]
        daytime = item["dayTime"].split(",")[0]  # Extracting only the date portion

        formatted_message += f"- {tank}: O2: {O2}, daytime: {daytime}\n"

    return formatted_message


def retrievelastEat(result):
    formatted_message = ""
    for item in result:
        tank = item["tank"]
        lastEat = item["lastEat"]
        daytime = item["dayTime"].split(",")[0]  # Extracting only the date portion

        formatted_message += f"- {tank}: lastEat: {lastEat}, daytime: {daytime}\n"

    return formatted_message


@bot.message_handler(commands=["start"])
def first_start(message):
    cid = message.chat.id
    bot.send_message(
        cid,
        f"Welcome {message.from_user.username}, press /help to get the list of commands",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    cid = message.chat.id

    # Create the inline buttons
    button_active_sensors = types.InlineKeyboardButton(
        "retrieve last measurements", callback_data="activeSensorsValues"
    )
    button_generate_data = types.InlineKeyboardButton(
        "Do Routine", callback_data="generateData"
    )
    button__O2 = types.InlineKeyboardButton(" O2", callback_data="O2")
    button__lastEat = types.InlineKeyboardButton("lastEat", callback_data="lastEat")
    button_send_email = types.InlineKeyboardButton(
        "Send Email", callback_data="sendEmail"
    )
    button_give_food_acquarium = types.InlineKeyboardButton(
        "Give Food Acquarium", callback_data="giveFoodAcquarium"
    )
    button_waterChange = types.InlineKeyboardButton(
        "Clean water", callback_data="waterChange"
    )
    button_generateO2 = types.InlineKeyboardButton(
        "Generate O2", callback_data="generateO2"
    )
    button_activate_sensors = types.InlineKeyboardButton(
        "Activate Sensors", callback_data="ONsensors"
    )
    button_deactivate_sensors = types.InlineKeyboardButton(
        "Deactivate Sensors", callback_data="OFFsensors"
    )
    button_switch_tank_on = types.InlineKeyboardButton(
        "Switch Tank On", callback_data="switchSensorOn"
    )
    button_switch_tank_off = types.InlineKeyboardButton(
        "Switch Tank Off", callback_data="switchSensorOff"
    )

    # Create the inline keyboard markup
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        button_active_sensors,
        button_generate_data,
        button__O2,
        button__lastEat,
        button_send_email,
        button_generateO2,
        button_give_food_acquarium,
        button_waterChange,
        button_activate_sensors,
        button_deactivate_sensors,
        button_switch_tank_on,
        button_switch_tank_off,
    )

    # Send the message with inline buttons
    bot.send_message(cid, "Choose a command:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if call.data == "activeSensorsValues":
        activeSensorsValues(call.message)
    elif call.data == "generateData":
        generate_data(call.message)
    elif call.data == "O2":
        O2(call.message)
    elif call.data == "lastEat":
        lastEat(call.message)
    elif call.data == "sendEmail":
        sendEmail(call.message)
    elif call.data == "giveFoodAcquarium":
        giveFoodAcquarium(call.message)
    elif call.data == "generateO2":
        generateO2(call.message)
    elif call.data == "waterChange":
        waterChange(call.message)
    elif call.data == "ONsensors":
        ONsensors(call.message)
    elif call.data == "OFFsensors":
        OFFsensors(call.message)
    elif call.data == "switchSensorOn":
        switchSensorOn(call.message)
    elif call.data == "switchSensorOff":
        switchSensorOff(call.message)


@bot.message_handler(commands=["generateData"])
def generate_data(message):
    cid = message.chat.id
    # command = ["node", "..\\dist\\device.js"]
    command = ["node", f"{os.getcwd()}\\dist\\device.js"]
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
    except Exception as e:
        print(e)
    output = output.decode("utf-8")
    error = error.decode("utf-8")
    if process.returncode != 0:
        print(f"Error executing Node.js script: {error}")
        bot.send_message(cid, "error generating data")
    else:
        print(f"Output:\n{output}")
        bot.send_message(cid, "Processing....")
        lambda_client = boto3.client("lambda", endpoint_url=url)
        response = lambda_client.invoke(
            FunctionName="onSensors",
            InvocationType="RequestResponse",
            Payload=json.dumps({"cid": cid}),
        )
        bot.send_message(cid, "Done!")


@bot.message_handler(commands=["activeSensorsValues"])
def activeSensorsValues(message):
    cid = message.chat.id
    try:
        result = query_data_dynamodb("Acquarium")
    except Exception as e:
        print(e)
    bot.send_message(cid, format_message(result))


@bot.message_handler(commands=["O2"])
def O2(message):
    cid = message.chat.id
    try:
        result = query_data_dynamodb("Acquarium")
    except Exception as e:
        print(e)
    bot.send_message(cid, retrieveO2(result))


@bot.message_handler(commands=["lastEat"])
def lastEat(message):
    cid = message.chat.id
    try:
        result = query_data_dynamodb("Acquarium")
    except Exception as e:
        print(e)
    bot.send_message(cid, retrievelastEat(result))


@bot.message_handler(commands=["sendEmail"])
def sendEmail(message):
    cid = message.chat.id
    try:
        bot.send_message(cid, "Please insert your email")
        bot.register_next_step_handler(message, process_email)
    except Exception as e:
        bot.send_message(cid, f"Error sending email: {str(e)}")
        # TODO vedere se abbiamo voglia di recuperare la mail nella root del container


def process_email(message):
    cid = message.chat.id
    recipient = message.text

    try:
        subject = f"Email from {bot.get_me().username}"
        body = format_message(query_data_dynamodb("Acquarium"))
        sender = env_vars["SENDER_EMAIL"]

        send_email(subject, body, sender, recipient)
        bot.send_message(cid, "Email sent successfully!")
    except Exception as e:
        bot.send_message(cid, f"Error sending email: {str(e)}")


def send_email(subject, body, sender, recipient):
    aws_access_key_id = env_vars["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = env_vars["AWS_SECRET_ACCESS_KEY"]
    aws_region = env_vars["REGION"]

    # Configure Boto3 client for SES
    ses_client = boto3.client(
        "ses",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=env_vars["ENDPOINT"],
    )

    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={"ToAddresses": [recipient]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        print("Email sent! Message ID:", response["MessageId"])
    except NoCredentialsError:
        print("Failed to send email: AWS credentials not found.")


@bot.message_handler(commands=["OFFsensors"])
def OFFsensors(message):
    cid = message.chat.id

    try:
        lambda_client = boto3.client("lambda", endpoint_url=url)
        response = lambda_client.invoke(
            FunctionName="offSensors",
            InvocationType="RequestResponse",
            Payload=json.dumps({"cid": cid}),
        )
        bot.send_message(cid, "Active status updated successfully!")

    except Exception as e:
        bot.send_message(cid, f"Error updating active status: {str(e)}")


@bot.message_handler(commands=["ONsensors"])
def ONsensors(message):
    cid = message.chat.id

    try:
        lambda_client = boto3.client("lambda", endpoint_url=url)
        response = lambda_client.invoke(
            FunctionName="onSensors",
            InvocationType="RequestResponse",
            Payload=json.dumps({"cid": cid}),
        )

        bot.send_message(cid, "Active status updated successfully!")

    except Exception as e:
        bot.send_message(cid, f"Error updating active status: {str(e)}")


@bot.message_handler(commands=["giveFoodAcquarium"])
def giveFoodAcquarium(message):
    cid = message.chat.id

    try:
        table = dynamoDb.Table("Acquarium")
        response = table.scan()
        items = response["Items"]
        tanks = list(set(item["tank"] for item in items))

        if not tanks:
            bot.send_message(cid, "No tanks found in the table.")
            return

        keyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        buttons = [KeyboardButton(tank) for tank in tanks]
        keyboard.add(*buttons)

        bot.send_message(cid, "Select a tank:", reply_markup=keyboard)

        bot.register_next_step_handler(message, process_giveFoodAcquarium)

    except Exception as e:
        bot.send_message(cid, f"Error toggling active status: {str(e)}")


@bot.message_handler(commands=["waterChange"])
def waterChange(message):
    cid = message.chat.id
    try:
        table = dynamoDb.Table("Acquarium")
        response = table.scan()
        items = response["Items"]

        tanks = list(set(item["tank"] for item in items))

        if not tanks:
            bot.send_message(cid, "No tanks found in the table.")
            return

        keyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        buttons = [KeyboardButton(tank) for tank in tanks]
        keyboard.add(*buttons)

        bot.send_message(cid, "Select a tank:", reply_markup=keyboard)

        bot.register_next_step_handler(message, process_waterChange)

    except Exception as e:
        bot.send_message(cid, f"Error toggling active status: {str(e)}")


@bot.message_handler(commands=["generateO2"])
def generateO2(message):
    cid = message.chat.id

    try:
        table = dynamoDb.Table("Acquarium")
        response = table.scan()
        items = response["Items"]

        tanks = list(set(item["tank"] for item in items))

        if not tanks:
            bot.send_message(cid, "No tanks found in the table.")
            return

        keyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        buttons = [KeyboardButton(tank) for tank in tanks]
        keyboard.add(*buttons)

        bot.send_message(cid, "Select a tank:", reply_markup=keyboard)

        bot.register_next_step_handler(message, process_generateO2)

    except Exception as e:
        bot.send_message(cid, f"Error toggling active status: {str(e)}")


def process_waterChange(message):
    cid = message.chat.id
    tank = message.text

    lambda_client = boto3.client("lambda", endpoint_url=url)
    response = lambda_client.invoke(
        FunctionName="waterClean",
        InvocationType="RequestResponse",
        Payload=json.dumps({"table": "Acquarium", "tank": tank}),
    )
    bot.send_message(
        cid,
        "water cleaned!, you should remove the dirty tank and place a clean water one",
    )


def process_giveFoodAcquarium(message):
    cid = message.chat.id
    tank = message.text

    lambda_client = boto3.client("lambda", endpoint_url=url)
    response = lambda_client.invoke(
        FunctionName="giveFoodAcquarium",
        InvocationType="RequestResponse",
        Payload=json.dumps({"table": "Acquarium", "tank": tank}),
    )
    bot.send_message(cid, "acquarium feeded!")


def process_generateO2(message):
    cid = message.chat.id
    tank = message.text

    lambda_client = boto3.client("lambda", endpoint_url=url)
    response = lambda_client.invoke(
        FunctionName="generateO2",
        InvocationType="RequestResponse",
        Payload=json.dumps({"table": "Acquarium", "tank": tank}),
    )
    bot.send_message(cid, "oxygen regenerated!")


@bot.message_handler(commands=["switchSensorOn"])
def switchSensorOn(message):
    cid = message.chat.id

    try:
        table = dynamoDb.Table("Acquarium")
        response = table.scan()
        items = response["Items"]

        tanks = list(set(item["tank"] for item in items))

        if not tanks:
            bot.send_message(cid, "No tanks found in the table.")
            return

        keyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        buttons = [KeyboardButton(tank) for tank in tanks]
        keyboard.add(*buttons)

        bot.send_message(cid, "Select a tank:", reply_markup=keyboard)

        bot.register_next_step_handler(message, process_tank_selection_on)

    except Exception as e:
        bot.send_message(cid, f"Error toggling active status: {str(e)}")


@bot.message_handler(commands=["switchSensorOff"])
def switchSensorOff(message):
    cid = message.chat.id

    try:
        table = dynamoDb.Table("Acquarium")
        response = table.scan()
        items = response["Items"]

        tanks = list(set(item["tank"] for item in items))

        if not tanks:
            bot.send_message(cid, "No tanks found in the table.")
            return

        keyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        buttons = [KeyboardButton(tank) for tank in tanks]
        keyboard.add(*buttons)

        bot.send_message(cid, "Select a tank:", reply_markup=keyboard)

        bot.register_next_step_handler(message, process_tank_selection_off)

    except Exception as e:
        bot.send_message(cid, f"Error toggling active status: {str(e)}")


def process_tank_selection_on(message):
    cid = message.chat.id
    tank = message.text

    lambda_client = boto3.client("lambda", endpoint_url=url)
    response = lambda_client.invoke(
        FunctionName="onSensorAcquarium",
        InvocationType="RequestResponse",
        Payload=json.dumps({"table": "Acquarium", "tank": tank}),
    )
    bot.send_message(cid, "Done!")


def process_tank_selection_off(message):
    cid = message.chat.id
    tank = message.text

    lambda_client = boto3.client("lambda", endpoint_url=url)
    response = lambda_client.invoke(
        FunctionName="offSensorAcquarium",
        InvocationType="RequestResponse",
        Payload=json.dumps({"table": "Acquarium", "tank": tank}),
    )
    bot.send_message(cid, "Done!")


schedule.every(5).seconds.do(generateO2)
schedule.every(7).seconds.do(waterChange)
schedule.every().day.at("07:00").do(giveFoodAcquarium)
schedule.every().day.at("13:00").do(giveFoodAcquarium)
schedule.every().day.at("19:00").do(giveFoodAcquarium)

bot.polling()
