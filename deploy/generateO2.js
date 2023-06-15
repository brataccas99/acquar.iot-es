"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lambdaHandler = void 0;
const client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
const REGION = process.env.REGION;
// DB client
const ddbClient = new client_dynamodb_1.DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" });
const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"];
let result;
const lambdaHandler = async (event) => {
    const tank = event.tank;
    const input = {
        TableName: "Acquarium",
        Key: {
            tank: { S: ACQUARIUM_QUEUE_NAMES[tank] },
        },
        ExpressionAttributeNames: {
            "#WC": "waterChange",
        },
        ExpressionAttributeValues: {
            ":wc": {
                S: getRandomHourMinute(),
            },
        },
        ReturnValues: "ALL_NEW",
        UpdateExpression: "SET #WC = :wc",
    };
    try {
        const command = new client_dynamodb_1.UpdateItemCommand(input);
        const responseDB = await ddbClient.send(command);
        if (!responseDB) {
        }
        else {
            console.info("Database populated");
        }
    }
    catch (error) {
        console.error(error);
    }
    function getRandomHourMinute() {
        const hour = Math.floor(Math.random() * 24);
        const minute = Math.floor(Math.random() * 60);
        const hourString = hour.toString().padStart(2, "0");
        const minuteString = minute.toString().padStart(2, "0");
        return `${hourString}:${minuteString}`;
    }
};
exports.lambdaHandler = lambdaHandler;
