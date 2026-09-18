"""
Zoho CRM Read-Only MCP Server

A Model Context Protocol server that provides read-only access to Zoho CRM data.
Uses Zoho CRM API v2 with OAuth 2.0 authentication.

Environment Variables (set via config.yaml env: section):
  ZOHO_CRM_ACCESS_TOKEN  - OAuth access token (Zoho-oauthtoken)
  ZOHO_CRM_ORG_ID        - Optional: organization ID for multi-org accounts

Read-only scopes required when generating the token:
  ZohoCRM.modules.READ   - Read access to all modules
  Or granular scopes like ZohoCRM.Contacts.READ, ZohoCRM.Deals.READ, etc.

Usage:
  python zoho_crm_mcp_server.py

Configured as a stdio MCP server in Hermes config.yaml.
"""

import os
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult
from mcp.types import ListToolsRequest, CallToolRequest, ListToolsResult

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

log = logging.getLogger("zoho_crm_mcp")
logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN = os.environ.get("ZOHO_CRM_ACCESS_TOKEN", "")
ORG_ID = os.environ.get("ZOHO_CRM_ORG_ID", "")
BASE_URL = "https://www.zohoapis.com/crm/v2"

if not ACCESS_TOKEN:
    log.warning(
        "ZOHO_CRM_ACCESS_TOKEN not set — server will start but all calls will fail "
        "with 'token not configured'. Set it in config.yaml under mcp_servers.env."
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    """Build request headers with the OAuth token."""
    headers = {
        "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if ORG_ID:
        headers["X-org-id"] = ORG_ID
    return headers


def _zoho_get(path: str, params: dict | None = None) -> dict:
    """Make a GET request to the Zoho CRM API v2 and return parsed JSON."""
    import httpx2  # stdlib-compatible via mcp deps

    url = f"{BASE_URL}{path}"
    log.info("GET %s params=%s", url, params)
    resp = httpx2.get(url, headers=_headers(), params=params, timeout=30.0)
    resp.raise_for_status()
    data = resp.json()

    # Zoho wraps results: {"data": [...], "info": {...}}
    return data


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS: list[Tool] = [
    Tool(
        name="zoho_crm_list_contacts",
        description="List contacts from Zoho CRM. Supports pagination via limit (default 20, max 200) and page.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max records to return (default 20, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default 1)",
                    "minimum": 1,
                },
                "search": {
                    "type": "string",
                    "description": "Search term to filter contacts by name or email",
                },
            },
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_get_contact",
        description="Get a single contact by its Zoho CRM record ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Zoho CRM record ID (e.g. 567890123)",
                    "minLength": 1,
                }
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_list_deals",
        description="List deals (sales pipeline) from Zoho CRM. Supports pagination and search.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max records to return (default 20, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default 1)",
                    "minimum": 1,
                },
                "search": {
                    "type": "string",
                    "description": "Search term to filter deals by name",
                },
            },
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_get_deal",
        description="Get a single deal by its Zoho CRM record ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Zoho CRM record ID",
                    "minLength": 1,
                }
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_list_accounts",
        description="List accounts (companies/organizations) from Zoho CRM.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max records to return (default 20, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default 1)",
                    "minimum": 1,
                },
                "search": {
                    "type": "string",
                    "description": "Search term to filter accounts by name",
                },
            },
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_get_account",
        description="Get a single account by its Zoho CRM record ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Zoho CRM record ID",
                    "minLength": 1,
                }
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_list_tasks",
        description="List tasks from Zoho CRM.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max records to return (default 20, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default 1)",
                    "minimum": 1,
                },
            },
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_get_task",
        description="Get a single task by its Zoho CRM record ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Zoho CRM record ID",
                    "minLength": 1,
                }
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_list_users",
        description="List users in the Zoho CRM organization.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max records to return (default 50, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                }
            },
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_search",
        description="Search across modules in Zoho CRM. Specify module name (contacts, deals, accounts, tasks, leads, campaigns, products, events, calls, notes, invoices, quotes, purchase_orders, sales_orders, cases, solutions, custom_modules) and a search string.",
        inputSchema={
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "description": "Module API name (contacts, deals, accounts, tasks, leads, campaigns, products, events, calls, notes, invoices, quotes, purchase_orders, sales_orders, cases, solutions)",
                    "enum": [
                        "contacts", "deals", "accounts", "tasks", "leads",
                        "campaigns", "products", "events", "calls", "notes",
                        "invoices", "quotes", "purchase_orders", "sales_orders",
                        "cases", "solutions"
                    ],
                },
                "search": {
                    "type": "string",
                    "description": "Search term (e.g. a name, email, or deal name)",
                    "minLength": 1,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 20, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                },
            },
            "required": ["module", "search"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_get_module",
        description="Generic read access to any Zoho CRM module by API name. Use for modules not explicitly covered by the dedicated tools above. Supports pagination.",
        inputSchema={
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "description": "Module API name (e.g. 'Leads', 'Cases', 'Solutions', or any custom module)",
                    "minLength": 1,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max records (default 20, max 200)",
                    "minimum": 1,
                    "maximum": 200,
                },
                "page": {
                    "type": "integer",
                    "description": "Page number (default 1)",
                    "minimum": 1,
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific fields to return (optional)",
                },
            },
            "required": ["module"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_get_record",
        description="Get any record by its module API name and record ID. Generic read access for any Zoho CRM module.",
        inputSchema={
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "description": "Module API name (e.g. 'Contacts', 'Deals', 'Leads', 'Accounts')",
                    "minLength": 1,
                },
                "id": {
                    "type": "string",
                    "description": "Zoho CRM record ID",
                    "minLength": 1,
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific fields to return (optional)",
                },
            },
            "required": ["module", "id"],
            "additionalProperties": False,
        },
    ),
    Tool(
        name="zoho_crm_aggregation",
        description="Get count aggregation for a module (e.g. total deals, total contacts). Supports grouping by a field.",
        inputSchema={
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "description": "Module API name (e.g. 'Contacts', 'Deals', 'Accounts')",
                    "minLength": 1,
                },
                "group_by": {
                    "type": "string",
                    "description": "Optional field to group count by (e.g. 'Stage' for deals, 'Industry' for accounts)",
                },
            },
            "required": ["module"],
            "additionalProperties": False,
        },
    ),
]


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

async def _handle_list(module_path: str, limit: int = 20, page: int = 1, search: str = "") -> CallToolResult:
    """Generic list handler for contacts, deals, accounts, tasks."""
    params: dict[str, Any] = {"per_page": limit, "page": page}
    if search:
        # Zoho search via params: search=term
        params["search"] = search

    try:
        data = _zoho_get(f"/{module_path}", params)
        records = data.get("data", [])
        info = data.get("info", {})
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "count": len(records),
                            "page": page,
                            "per_page": limit,
                            "total_pages": info.get("total_pages"),
                            "total_records": info.get("more_records"),
                            "data": records,
                        },
                        indent=2,
                    ),
                )
            ]
        )
    except Exception as e:
        log.exception("Error listing %s", module_path)
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Error: {e}")],
        )


async def _handle_get(module_path: str, record_id: str) -> CallToolResult:
    """Generic get handler for a single record."""
    try:
        data = _zoho_get(f"/{module_path}/{record_id}")
        records = data.get("data", [])
        if not records:
            return CallToolResult(
                content=[TextContent(type="text", text=f"No record found with ID {record_id} in {module_path}")]
            )
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(records[0], indent=2))]
        )
    except Exception as e:
        log.exception("Error getting %s/%s", module_path, record_id)
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Error: {e}")],
        )


async def _handle_search(module: str, search: str, limit: int = 20) -> CallToolResult:
    """Search a module using Zoho's search endpoint."""
    try:
        data = _zoho_get(f"/{module}/search", {"search": search, "per_page": limit})
        records = data.get("data", [])
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {"count": len(records), "search": search, "data": records}, indent=2
                    ),
                )
            ]
        )
    except Exception as e:
        log.exception("Error searching %s for '%s'", module, search)
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Error: {e}")],
        )


async def _handle_module(module: str, limit: int = 20, page: int = 1, fields: list[str] | None = None) -> CallToolResult:
    """Generic module listing with optional fields filter."""
    params: dict[str, Any] = {"per_page": limit, "page": page}
    if fields:
        params["fields"] = ",".join(fields)

    try:
        data = _zoho_get(f"/{module}", params)
        records = data.get("data", [])
        info = data.get("info", {})
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "count": len(records),
                            "page": page,
                            "per_page": limit,
                            "data": records,
                        },
                        indent=2,
                    ),
                )
            ]
        )
    except Exception as e:
        log.exception("Error listing module %s", module)
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Error: {e}")],
        )


async def _handle_record(module: str, record_id: str, fields: list[str] | None = None) -> CallToolResult:
    """Generic get any record."""
    params: dict[str, Any] = {}
    if fields:
        params["fields"] = ",".join(fields)

    try:
        data = _zoho_get(f"/{module}/{record_id}", params)
        records = data.get("data", [])
        if not records:
            return CallToolResult(
                content=[TextContent(type="text", text=f"No record found: {module}/{record_id}")]
            )
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(records[0], indent=2))]
        )
    except Exception as e:
        log.exception("Error getting %s/%s", module, record_id)
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Error: {e}")],
        )


async def _handle_aggregation(module: str, group_by: str | None = None) -> CallToolResult:
    """Count aggregation for a module."""
    params: dict[str, Any] = {"select_value": "Count"}
    if group_by:
        params["group_by"] = group_by

    try:
        data = _zoho_get(f"/{module}", params)
        records = data.get("data", [])
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "module": module,
                            "group_by": group_by,
                            "aggregations": records,
                        },
                        indent=2,
                    ),
                )
            ]
        )
    except Exception as e:
        log.exception("Error aggregating %s", module)
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Error: {e}")],
        )


# ---------------------------------------------------------------------------
# Tool dispatch map
# ---------------------------------------------------------------------------

DISPATCH = {
    "zoho_crm_list_contacts": lambda args: _handle_list("Contacts", args.get("limit", 20), args.get("page", 1), args.get("search", "")),
    "zoho_crm_get_contact": lambda args: _handle_get("Contacts", args["id"]),
    "zoho_crm_list_deals": lambda args: _handle_list("Deals", args.get("limit", 20), args.get("page", 1), args.get("search", "")),
    "zoho_crm_get_deal": lambda args: _handle_get("Deals", args["id"]),
    "zoho_crm_list_accounts": lambda args: _handle_list("Accounts", args.get("limit", 20), args.get("page", 1), args.get("search", "")),
    "zoho_crm_get_account": lambda args: _handle_get("Accounts", args["id"]),
    "zoho_crm_list_tasks": lambda args: _handle_list("Tasks", args.get("limit", 20), args.get("page", 1)),
    "zoho_crm_get_task": lambda args: _handle_get("Tasks", args["id"]),
    "zoho_crm_list_users": lambda args: _handle_list("Users", args.get("limit", 50)),
    "zoho_crm_search": lambda args: _handle_search(args["module"], args["search"], args.get("limit", 20)),
    "zoho_crm_get_module": lambda args: _handle_module(args["module"], args.get("limit", 20), args.get("page", 1), args.get("fields")),
    "zoho_crm_get_record": lambda args: _handle_record(args["module"], args["id"], args.get("fields")),
    "zoho_crm_aggregation": lambda args: _handle_aggregation(args["module"], args.get("group_by")),
}


# ---------------------------------------------------------------------------
# MCP request handlers (SDK 2.1.1+ uses add_request_handler)
# ---------------------------------------------------------------------------

async def _handle_list_tools(
    _request: "ListToolsRequest",
) -> "ListToolsResult":
    """Handle tools/list — return the 13 Zoho CRM tool definitions."""
    log.info("Listing %d Zoho CRM tools", len(TOOLS))
    return ListToolsResult(tools=TOOLS)


async def _handle_call_tool(
    request: "CallToolRequest",
) -> CallToolResult:
    """Handle tools/call — dispatch to the right Zoho CRM function."""
    if not ACCESS_TOKEN:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text="ZOHO_CRM_ACCESS_TOKEN is not configured. Set it in config.yaml under mcp_servers.env.")],
        )

    args = request.params or {}
    handler = DISPATCH.get(request.name)
    if handler is None:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Unknown tool: {request.name}")],
        )

    log.info("Calling tool %s with args %s", request.name, args)
    return await handler(args)


# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

async def main():
    """Run the Zoho CRM MCP server via stdio."""
    server = Server("zoho_crm_readonly")

    server.add_request_handler(
        "tools/list",
        ListToolsRequest,
        _handle_list_tools,
    )

    server.add_request_handler(
        "tools/call",
        CallToolRequest,
        _handle_call_tool,
    )

    log.info("Zoho CRM read-only MCP server starting — stdio transport")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
