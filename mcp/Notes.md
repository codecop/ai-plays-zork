# Idea: make Zork an MCP, so it is a tool

* Python and the MCP SDK
* FastMCP <https://github.com/jlowin/fastmcp>
* maybe build it from scratch to learn it?
* <https://towardsdatascience.com/creating-and-deploying-an-mcp-server-from-scratch/> like Mistral

## from scratch

* MCP specification <https://modelcontextprotocol.info/specification/2024-11-05/>

### look at protocol

* JSON-RPC message format, uses JSON-RPC 2.0
  * Request object

```
A rpc call is represented by sending a Request object to a Server. The Request object has the following members:

jsonrpc
    A String specifying the version of the JSON-RPC protocol. MUST be exactly "2.0".

method
    A String containing the name of the method to be invoked. Method names that begin with the word rpc followed by a period character (U+002E or ASCII 46) are reserved for rpc-internal methods and extensions and MUST NOT be used for anything else.

params
    A Structured value that holds the parameter values to be used during the invocation of the method. This member MAY be omitted.

id
    An identifier established by the Client that MUST contain a String, Number, or NULL value if included. If it is not included it is assumed to be a notification. The value SHOULD normally not be Null [1] and Numbers SHOULD NOT contain fractional parts [2] 
```

Example of a request:

```json
{
  "jsonrpc": "2.0",
  "method": "subtract",
  "params": [42, 23],
  "id": 1
}
```

MCP defines three core message types based on JSON-RPC 2.0:

* Requests: Bidirectional messages with method and parameters expecting a response
* Responses: Successful results or errors matching specific request IDs
* Notifications: One-way messages requiring no response

### Features

* Resources: Context and data, for the user or the AI model to use <- just query?
* Prompts: Templated messages and workflows for users <- what is this?
* Tools: Functions for the AI model to execute <- this is obvious

### Servers

Each server provides focused functionality in isolation
