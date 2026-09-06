"""Resource handlers for Passbolt Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListVaultItemParams, GetVaultItemParams,
    VaultItemRecord, VaultItemList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_vault_items", "List vault_items in Passbolt.", action_type="read", chain_callable=True, event="passbolt-connector.list_vault_items", effects=["read:vault_items"], data_model=VaultItemList)
async def list_vault_items(params: ListVaultItemParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_vault_items(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.ok({"vault_items": items, "total": len(items)}, summary=f"Found {len(items)} vault_items.")
    except Exception as e:
        return ActionResult.error(f"Error listing vault_items: {e}")

@chat.function("get_vaultitem", "Get details of one VaultItem in Passbolt.", action_type="read", chain_callable=True, event="passbolt-connector.get_vaultitem", effects=["read:vaultitem"], data_model=VaultItemRecord)
async def get_vaultitem(params: GetVaultItemParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_vaultitem(params.vaultitem_id)
        rid = str(r.get("id") or params.vaultitem_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.ok({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved VaultItem {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving VaultItem: {e}")

@chat.function("audit_vaultitem_health", "Audit health of Passbolt vault_items and connectivity.", action_type="read", chain_callable=True, event="passbolt-connector.audit_vaultitem_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_vaultitem_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_vault_items(limit=50)
        return ActionResult.ok({
            "healthy": True,
            "total_vault_items": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"Passbolt healthy. Sampled {len(items)} vault_items."
        }, summary=f"Passbolt health check passed with {len(items)} vault_items.")
    except Exception as e:
        return ActionResult.error(f"Error auditing Passbolt health: {e}")
