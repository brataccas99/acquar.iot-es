"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lambdaHandler = void 0;
const client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
const REGION = process.env.REGION;
const ENDPOINT = "http://localhost:4566";
const TABLE_NAME = "Acquarium";
const client = new client_dynamodb_1.DynamoDBClient({ region: REGION, endpoint: ENDPOINT });
const lambdaHandler = async (event) => {
    const tank = event.tank;
    const O2 = getRandomHourMinute() + " hh:mm";
    const params = {
        TableName: TABLE_NAME,
        Key: {
            tank: { S: tank },
        },
        UpdateExpression: "SET O2 = :O2",
        ExpressionAttributeValues: {
            ":O2": { S: O2 },
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
