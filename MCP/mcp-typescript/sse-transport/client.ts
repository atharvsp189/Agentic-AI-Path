import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const client = new Client({
    name: "example-client",
    version: "1.0.0"
}, {
  capabilities: {}
});

const transport = new SSEClientTransport(
  new URL("http://localhost:3001/sse")
);
await client.connect(transport);

console.log("Client connected");

async function main() {
    console.log("Client connected");
    console.log("Tools: \n", await client.listTools());
    console.log("Resources: \n", await client.listResources());
    console.log("End")
}

main();