import { PutItemCommand } from "@aws-sdk/client-dynamodb"

import { ddbClient } from "../index"

//tanks array for creating entries in db
const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"]
//variables for store the random result
let result
//get timestamp
let new_Date = Date.now().toString()
let fullDate = new Date().toLocaleString()

export const populateDB = async () => {
  for (let tank = 0; tank < ACQUARIUM_QUEUE_NAMES.length; tank++) {
    const command = new PutItemCommand({
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
    const response = await ddbClient.send(command)

    if (!response) {
      console.error("Error populating DB\n")
    }
    console.info("Database populated")
  }
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

populateDB()
