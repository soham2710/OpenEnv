# RFC 006: Open Reward Standard (ORS) Support

**Status**: Draft
**Created**: 2026-04-22
**Authors**: @soham2710, @openenv-bot
**RFC ID**: 006

---

## Summary

This RFC proposes the integration of the Open Reward Standard (ORS) into OpenEnv, enabling environments to expose reward computation in a standardized, interoperable format. ORS support will be layered on top of the existing Rubric system, allowing environments to serialize, export, and adapt their reward logic for external consumers, benchmarks, and cross-framework compatibility.

## Motivation

- **Interoperability**: Enable OpenEnv environments to participate in cross-benchmark evaluations and competitions by exposing rewards in a standard format.
- **Transparency**: Allow external tools to inspect, audit, and visualize reward logic and component scores.
- **Reusability**: Facilitate sharing and reuse of reward definitions across environments and projects.
- **Compliance**: Align with emerging standards in RL and evaluation research.

## Design

### Architecture Overview
- ORS support will be implemented as an adapter layer on top of the Rubric system.
- Each environment's `rubric` can be exported to an ORS-compliant JSON/YAML format via a `to_ors()` method.
- The adapter will map Rubric hierarchies, weights, and gating logic to the ORS schema.
- Environments can optionally accept ORS definitions to construct rubrics dynamically.

### Core Abstractions
- `Rubric.to_ors() -> dict`: Serializes the rubric and its children to ORS format.
- `Rubric.from_ors(ors_dict) -> Rubric`: (Optional) Instantiates a rubric from an ORS definition.
- `Environment.export_reward_spec()`: Returns the ORS reward spec for the environment.

### Key Design Decisions
- **Adapter Pattern**: Use a non-intrusive adapter to avoid breaking existing environments.
- **Extensibility**: Allow custom rubric subclasses to override ORS export logic.
- **Versioning**: Include ORS version metadata in exports for forward compatibility.

## Examples

### Exporting a Rubric to ORS
```python
rubric = CodeRubric()
ors_spec = rubric.to_ors()
# Save or serve as JSON/YAML
```

### Environment Reward Export
```python
class MyEnv(Environment):
    def export_reward_spec(self):
        return self.rubric.to_ors()
```

### ORS Example Output
```json
{
  "ors_version": "1.0",
  "criteria": [
    {"name": "compiles", "type": "gate", "weight": 1.0},
    {"name": "tests", "type": "score", "weight": 0.7},
    {"name": "style", "type": "score", "weight": 0.3}
  ],
  "aggregation": "weighted_sum",
  "gating": ["compiles"]
}
```

---

## Migration
- Existing environments can add `to_ors()` to their rubrics for instant compatibility.
- New environments should implement reward logic using the Rubric system for seamless ORS support.

## Open Questions
- How to handle non-hierarchical or procedural reward logic?
- Should we support round-tripping (ORS -> Rubric -> ORS)?
- What is the minimal ORS schema for OpenEnv use cases?

---

## References
- [Open Reward Standard (ORS) Proposal](https://github.com/open-reward-standard/proposal)
- [RFC 004: Rubric System for Reward Computation](./004-rubrics.md)
