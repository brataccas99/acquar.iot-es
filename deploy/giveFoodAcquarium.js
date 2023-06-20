"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lambdaHandler = void 0;
const client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
const REGION = process.env.REGION;
const ENDPOINT = "http://localhost:4566";
const TABLE_NAME = "Acquarium";
const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"];
const client = new client_dynamodb_1.DynamoDBClient({ region: REGION, endpoint: ENDPOINT });
const lambdaHandler = async () => {
    const tank = "red_fish_aq";
    const lastEat = getRandomHourMinute() + "hh:mm";
    const params = {
        TableName: TABLE_NAME,
        Key: {
            tank: { S: tank },
        },
        UpdateExpression: "SET lastEat = :lastEat",
        ExpressionAttributeValues: {
            ":lastEat": { S: lastEat },
        },
        ReturnValues: "UPDATED_NEW",
    };
    try {
        const command = new client_dynamodb_1.UpdateItemCommand(params);
        const response = await client.send(command);
        console.log("Update succeeded:", JSON.stringify(response));
    }
    catch (error) {
        console.error("Unable to update item. Error:", error);
    }
};
exports.lambdaHandler = lambdaHandler;
function getRandomHourMinute() {
    const hour = Math.floor(Math.random() * 24);
    const minute = Math.floor(Math.random() * 60);
    const hourString = hour.toString().padStart(2, "0");
    const minuteString = minute.toString().padStart(2, "0");
    return `${hourString}:${minuteString}`;
}
function getValue(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min);
}
(0, exports.lambdaHandler)();
