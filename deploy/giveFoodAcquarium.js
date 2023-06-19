"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lambdaHandler = void 0;
const client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
const REGION = process.env.REGION;
// DB client
const ddbClient = new client_dynamodb_1.DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" });
const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"];
const lambdaHandler = async ( /*event: any*/) => {
    try {
        const scanCommand = new client_dynamodb_1.ScanCommand({
            TableName: "Acquarium",
        });
        const scanResponse = await ddbClient.send(scanCommand);
        if (scanResponse.Items && scanResponse.Items.length > 0) {
            for (const item of scanResponse.Items) {
                const tank = item.tank.S;
                if (tank === "red_fish_aq") {
                    const updatedItem = {
                        TableName: "Acquarium",
                        Item: {
                            tank: { S: item.tank.S || "" },
                            O2: { S: item.O2.S || "" },
                            lastEat: { S: getRandomHourMinute() },
                            waterChange: { S: item.waterChange.S || "" },
                            Active: { BOOL: item.Active.BOOL || false },
                            Daytime: { BOOL: item.Daytime.BOOL || false },
                            timeStamp: { N: item.timeStamp.N || "0" },
                        },
                    };
                    await ddbClient.send(new client_dynamodb_1.PutItemCommand(updatedItem));
                    console.log(`Updated lastEat for tank: ${tank}`);
                }
            }
        }
        else {
            console.log("No tank items found");
        }
    }
    catch (error) {
        console.error(error);
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
(0, exports.lambdaHandler)();
