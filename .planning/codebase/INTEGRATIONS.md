# Integrations

## External Services

**None.** This project is entirely offline/local. No APIs, databases, cloud services, or authentication providers.

## Internal Integrations

### Brutus CLI ↔ Python Pipeline

The Python pipeline invokes the Brutus C++ binary via subprocess:

- **Runner scripts** (`simulation_data/Scripts/brutus_runners/`) call `./brutus` with CLI args
- **Input:** IC text files (3 lines, 7 fields each: `m x y z vx vy vz`)
- **Output:** Brutus trajectory files (timestamped snapshots with optional `Result:` footer)
- **Timeout:** 3000 seconds per simulation in batch runners

### File-Based Data Flow

All integration is file-based — no databases, message queues, or network calls.

```
IC files (.txt) → Brutus binary → trajectory files (.txt)
                                → metrics extraction → JSON metrics
IC files + trajectories → data-processing-pipeline → HDF5 → PINN training
```

## Data Formats

| Format | Usage | Location |
|--------|-------|----------|
| **Plain text** | IC files, Brutus output (high-precision decimal strings) | `simulation_data/Data/` |
| **JSON** | Metrics, prescreening indexes, blacklists, configs | `simulation_data/Data/metrics/`, `Documentation/` |
| **HDF5** | Preprocessed PINN training data | `pinn/data-handling/core/preprocessed-data/` |
| **Markdown** | Documentation, methodology instructions | `simulation_data/Documentation/`, `pinn_instruction/` |

## Webhooks / Scheduled Tasks

None.
