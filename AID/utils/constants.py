RETURN_NAME = "<RETURN>"
LAMBDA_NAME = "<LAMBDA_{}>"  # needs to be formatted
BUILTIN_NAME = "<builtin>"
EXT_NAME = "<external>"

FUN_DEF = "FUNCTIONDEF"
NAME_DEF = "NAMEDEF"
MOD_DEF = "MODULEDEF"
CLS_DEF = "CLASSDEF"
EXT_DEF = "EXTERNALDEF"

OBJECT_BASE = "object"

CLS_INIT = "__init__"
ITER_METHOD = "__iter__"
NEXT_METHOD = "__next__"
STATIC_METHOD = "staticmethod"

INVALID_NAME = "<**INVALID**>"

CALL_GRAPH_OP = "call-graph"
KEY_ERR_OP = "key-error"


BUILDIN_LIST = ["abs", "aiter", "all", "anext", "any", "ascii",
                "bin", "bool", "bytearray", "bytes", "callable", "chr",
                "complex", "dict", "dir", "divmod", "float", "format",
                "frozenset", "getattr", "hasattr", "hash", "hex", "id",
                "int", "isinstance", "issubclass", "iter", "len", "list",
                "map", "max", "min", "next", "oct", "ord",
                "pow", "repr", "reversed", "round", "set", "slice",
                "sorted", "str", "sum", "tuple", "type", "vars",
                "zip"]


NETWORK_PROTOCOL_METHODS_LIST = ["socket.socket",
                                 
                                 "requests.Session", "requests.get", "requests.session.put", "requests.post", "requests.Session.send", "requests.Session.get", "requests.request", "requests.Session.headers.update",

                                 "requests_oauthlib.OAuth2Session.refresh_token", 

                                 "aiohttp.ClientSession.get", "aiohttp.ClientSession.request", "aiohttp.ClientSession", "aiohttp.ClientTimeout", "aiohttp.ClientSession.post", "aiohttp.client.ClientSession.request", "aiohttp.ClientResponse.text",

                                 "asyncio.open_connection", "asyncio.get_event_loop.create_datagram_endpoint", "asyncio.StreamWriter.write", "asyncio.DatagramTransport.sendto", "asyncio.BaseTransport.write",

                                 "httpx.AsyncClient", "httpx.AsyncClient.post", "httpx.AsyncClient.get",

                                 "urllib.request.Request",

                                 "bleak_retry_connector.establish_connection.write_gatt_char",

                                 "paho.mqtt.client.Client.publish",

                                 "btle.Peripheral",

                                 "pyserial.Serial",

                                 "aiocoap.Message",

                                 "websockets.client.connect",
                                 ]