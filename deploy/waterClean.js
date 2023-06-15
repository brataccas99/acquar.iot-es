"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lambdaHandler = void 0;
const client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
const REGION = process.env.REGION;
//db client
const ddbClient = new client_dynamodb_1.DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" });
const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"];
//get timestamp
let fullDate = new Date().toLocaleString();
const lambdaHandler = async (event) => {
    const tank = event.tank;
    try {
        const commandDB = new client_dynamodb_1.UpdateItemCommand({
            TableName: "Acquarium",
            Key: {
                tank: { S: ACQUARIUM_QUEUE_NAMES[tank] },
            },
            UpdateExpression: "SET waterChange = :waterChangeValue",
            ExpressionAttributeValues: {
                ":waterChangeValue": { S: fullDate },
            },
        });
        const responseDB = await ddbClient.send(commandDB);
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
