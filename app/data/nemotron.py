from typing import Any

from app.models.dataset import DatasetRecord


def convert_nemotron_record(
    record: dict[str, Any],
    index: int,
) -> DatasetRecord:
    """Convert one NVIDIA Nemotron record to AegisAI schema."""

    attack_category = str(record.get("attack_category", "unknown"))

    return DatasetRecord(
        text=str(record["injection"]["injection_text"]),
        label=1,
        threat_type=attack_category,
        severity=None,
        source_dataset="nemotron",
        source_id=str(record.get("id", index)),
        group_id=None,
        metadata={
            "domain": record.get("domain"),
            "target_tool": record.get("target_tool"),
            "injection_vector": record.get("injection_vector"),
            "agent_ref": record.get("agent_ref"),
            "required_tools": record.get("required_tools", []),
            "target_args": record.get("injection", {}).get("target_args"),
            "goal": record.get("injection", {}).get("goal"),
            "verification_type": record.get("injection", {}).get(
                "verification_type"
            ),
            "used_in": record.get("used_in", []),
            "license": record.get("license"),
        },
    )
