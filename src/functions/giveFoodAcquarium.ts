import { DynamoDBClient, UpdateItemCommand } from "@aws-sdk/client-dynamodb"

const REGION = process.env.REGION

//db client
const ddbClient = new DynamoDBClient({ region: REGION, endpoint: "http://localhost:4566" })
const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"]
let result

export const lambdaHandler = async (/*event: any*/) => {
  const tank: any = "red_fish_aq"

  try {
    const commandDB = new UpdateItemCommand({
      TableName: "Acquarium",
      Key: {
        tank: { S: ACQUARIUM_QUEUE_NAMES[tank] },
      },
      UpdateExpression: "SET lastEat = :lastEatValue",
      ExpressionAttributeValues: {
        ":lastEatValue": { S: (result = getRandomHourMinute().toString() + "hh:mm") },
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

  function getRandomHourMinute(): string {
    const hour = Math.floor(Math.random() * 24)
    const minute = Math.floor(Math.random() * 60)

    const hourString = hour.toString().padStart(2, "0")
    const minuteString = minute.toString().padStart(2, "0")

    return `${hourString}:${minuteString}`
  }
}

lambdaHandler()
