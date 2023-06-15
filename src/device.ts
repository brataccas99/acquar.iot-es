import { SendMessageCommand } from "@aws-sdk/client-sqs"

import { queueClient } from "./index"

const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"]

const SQS_QUEUE_URL = process.env.ENDPOINT + "/000000000000/"

//get timestamp
let new_Date = Date.now().toString()
let fullDate = new Date().toLocaleString()

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

const uploadToQueues = async (sqsQueueUrl = SQS_QUEUE_URL) => {
  for (let queue = 0; queue < ACQUARIUM_QUEUE_NAMES.length; queue++) {
    let random = getValue(2, 5)

    for (let count = 0; count < random; count++) {
      const command = new SendMessageCommand({
        QueueUrl: SQS_QUEUE_URL + ACQUARIUM_QUEUE_NAMES[queue],
        DelaySeconds: 1,
        MessageBody: `{ "acquarium":"${ACQUARIUM_QUEUE_NAMES[queue].toString()}","temperature":"${getValue(
          10,
          35
        ).toString()} Celsius",
        "O2":"${getRandomHourMinute()} hh:mm","lastEat":"${getRandomHourMinute()} hh:mm",
        "waterChange":"${Date.now.toString()}} gg/MM/yyyy",
        "timeStamp":"${new_Date}",
        "dayTime":"${fullDate}"}`,
      })
      const response = await queueClient.send(command)

      if (!response) {
        console.error("Error sending to queue", ACQUARIUM_QUEUE_NAMES[queue])
      }
      console.info("Message sent")
    }
  }
}

uploadToQueues()
