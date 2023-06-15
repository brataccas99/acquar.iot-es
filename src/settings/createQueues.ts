import { CreateQueueCommand } from "@aws-sdk/client-sqs"

import { queueClient } from "../index"

const ACQUARIUM_QUEUE_NAMES = ["tropical_fish_aq", "red_fish_aq", "shark_aq"]

export const createQueues = async (sqsQueueName = ACQUARIUM_QUEUE_NAMES) => {
  for (let queue = 0; queue < ACQUARIUM_QUEUE_NAMES.length; queue++) {
    const command = new CreateQueueCommand({
      QueueName: ACQUARIUM_QUEUE_NAMES[queue],
      Attributes: {
        DelaySeconds: "60",
        MessageRetentionPeriod: "86400",
      },
    })

    const response = await queueClient.send(command)

    if (!response) {
      console.error("Error. Queue", ACQUARIUM_QUEUE_NAMES[queue], "not created")
    }

    console.log("Queue", ACQUARIUM_QUEUE_NAMES[queue], "created")
  }
}
