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
    const waterChange = new Date().toLocaleString();
    const params = {
        TableName: TABLE_NAME,
        Key: {
            tank: { S: tank },
        },
        UpdateExpression: "SET waterChange = :waterChange",
        ExpressionAttributeValues: {
            ":waterChange": { S: waterChange },
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
