import { APIGatewayProxyEvent } from "aws-lambda"
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb"

const REGION = process.env.REGION

//db client
const ddbClient = new DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" })

//get timestamp
let new_Date = Date.now().toString()
let fullDate = new Date().toLocaleString()

export const lambdaHandler = async (event: any) => {
  const tank = event.tank

  try {
    const commandDB = new PutItemCommand({
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
    })
    const responseDB = await ddbClient.send(commandDB)

    if (!responseDB) {
    } else {
      console.info("Database populated")
    }
  } catch (error) {
    console.error(error)
  }
}
