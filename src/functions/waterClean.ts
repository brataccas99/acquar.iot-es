import { DynamoDBClient, UpdateItemCommand } from "@aws-sdk/client-dynamodb"

const REGION = process.env.REGION
const ENDPOINT = "http://localhost:4566"
const TABLE_NAME = "Acquarium"

const client = new DynamoDBClient({ region: REGION, endpoint: ENDPOINT })

export const lambdaHandler = async (event: any) => {
  const tank = event.tank
  const waterChange = new Date().toLocaleString()

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
  }

  try {
    const command = new UpdateItemCommand(params)
    const response = await client.send(command)
    console.log("Update succeeded:", JSON.stringify(response))
  } catch (error) {
    console.error("Unable to update item. Error:", error)
  }
}
