import { CreateTableCommand } from "@aws-sdk/client-dynamodb"
import { ddbClient } from "../index"

export const runDB = async () => {
  const command = new CreateTableCommand({
    TableName: "Acquarium",

    AttributeDefinitions: [
      {
        AttributeName: "tank",
        AttributeType: "S",
      },
    ],
    KeySchema: [
      {
        AttributeName: "tank",
        KeyType: "HASH",
      },
    ],
    ProvisionedThroughput: {
      ReadCapacityUnits: 10,
      WriteCapacityUnits: 10,
    },
  })

  const response = await ddbClient.send(command)

  if (!response) {
    console.error("Error. Table not created")
  }

  return response
}
