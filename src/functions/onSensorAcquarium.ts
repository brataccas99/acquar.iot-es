import { APIGatewayProxyEvent } from "aws-lambda"
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb"

const REGION = process.env.REGION

//db client
const ddbClient = new DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" })

//get timestamp
let new_Date = Date.now().toString()
let fullDate = new Date().toLocaleString()

const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"]
let result

export const lambdaHandler = async (event: any) => {
  const tank = event.tank

  try {
    const commandDB = new PutItemCommand({
      TableName: "Acquarium",
      Item: {
        tank: { S: ACQUARIUM_QUEUE_NAMES[tank] },
        temperature: { S: (result = getValue(10, 35).toString() + "Celsius") },
        O2: { S: (result = getRandomHourMinute().toString() + "hh:mm") },
        lastEat: { S: (result = getRandomHourMinute().toString() + "hh:mm") },
        waterChange: { S: (result = fullDate) },
        timeStamp: { S: new_Date },
        dayTime: { S: fullDate },
        active: { BOOL: true },
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

  function getValue(min: number, max: number) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min + 1) + min) // The maximum is inclusive and the minimum is inclusive
  }

  function getRandomHourMinute(): string {
    const hour = Math.floor(Math.random() * 24)
    const minute = Math.floor(Math.random() * 60)

    const hourString = hour.toString().padStart(2, "0")
    const minuteString = minute.toString().padStart(2, "0")

    return `${hourString}:${minuteString}`
  }
}
