"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lambdaHandler = void 0;
const client_dynamodb_1 = require("@aws-sdk/client-dynamodb");
const REGION = process.env.REGION;
//db client
const ddbClient = new client_dynamodb_1.DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" });
//get timestamp
let new_Date = Date.now().toString();
let fullDate = new Date().toLocaleString();
const lambdaHandler = async (event) => {
    const tank = event.tank;
    try {
        const commandDB = new client_dynamodb_1.PutItemCommand({
            TableName: "Acquarium",
            Item: {
                tank: { S: tank },
                temperature: { S: 0 + "Celsius" },
                O2: { S: "00:00" + "hh:mm" },
                lastEat: { S: "00:00" + "hh:mm" },
                waterChange: { S: fullDate },
                timeStamp: { S: new_Date },
                dayTime: { S: fullDate },
                active: { BOOL: false },
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
};
exports.lambdaHandler = lambdaHandler;
