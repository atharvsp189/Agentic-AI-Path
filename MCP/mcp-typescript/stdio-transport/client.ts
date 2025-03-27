import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const client = new Client({
  name: "example-client",
  version: "1.0.0"
}, {
  capabilities: {}
});

const transport = new StdioClientTransport({
  command: "tsx",
  args: ["server.ts"]
});
await client.connect(transport);

async function main() {
    console.log("Client connected");
    console.log("Tools: \n", await client.listTools());
    console.log("Resources: \n", await client.listResources());
    console.log("End")
}

main();