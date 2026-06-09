# Remove Qwen Model, QWEN.md, and MLX Artifacts

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the downloaded Qwen 3.5 2B 4-bit model directory, the QWEN.md agent instructions file, the HF cache entry, and any MLX remnants from this project. Free ~1.6 GB of disk space and clean the codebase.

**Architecture:** Simple deletions and git operations. No code depends on the Qwen model or MLX in this project — it was a side experiment. The `.planning/` historical docs reference Qwen but are preserved as-is (they document past decisions).

**Tech Stack:** git, shell (rm), HF CLI

---

## Inventory

| Item | Location | Size | Git Status | Action |
|------|----------|------|------------|--------|
| Qwen model directory | `Qwen3.5-2B-4bit/` | 1.6 GB | Untracked (`??`) | Delete |
| Qwen agent instructions | `QWEN.md` | ~9 KB | Tracked | Remove from git |
| HF cache (Qwen model) | `~/.cache/huggingface/hub/models--mlx-community--Qwen3.5-2B-4bit/` | 4 KB | N/A | Delete |
| MLX packages | pip | N/A | N/A | Already uninstalled |
| huggingface-hub | pip | ~80 KB | N/A | Keep |
| `~/.claude-qwen/` | Home dir | N/A | N/A | Keep |

**Not removed (historical references only, no functional impact):**
- `.planning/` docs that mention Qwen/MLX (these are completed phase records)
- `docs/plans/cleaning-3-body*.md` that mention Qwen (planning history)

---

### Task 1: Delete the Qwen model directory

**Files:**
- Delete: `Qwen3.5-2B-4bit/` (entire directory, 1.6 GB)

- [ ] **Step 1: Verify directory exists and confirm size**

```bash
du -sh <home>/Desktop/3_body_problem/Qwen3.5-2B-4bit/
ls <home>/Desktop/3_body_problem/Qwen3.5-2B-4bit/
```
Expected: ~1.6 GB, contains model.safetensors, config.json, tokenizer.json, etc.

- [ ] **Step 2: Delete the directory**

```bash
rm -rf <home>/Desktop/3_body_problem/Qwen3.5-2B-4bit/
```

- [ ] **Step 3: Verify deletion**

```bash
ls <home>/Desktop/3_body_problem/Qwen3.5-2B-4bit/ 2>&1
```
Expected: "No such file or directory"

---

### Task 2: Remove QWEN.md from git

**Files:**
- Delete: `QWEN.md`

- [ ] **Step 1: Verify QWEN.md is tracked by git**

```bash
git ls-files QWEN.md
```
Expected: `QWEN.md` (shows it's tracked)

- [ ] **Step 2: Remove from git tracking and delete file**

```bash
git rm QWEN.md
```

- [ ] **Step 3: Verify removal**

```bash
git status --short QWEN.md
```
Expected: `D QWEN.md` (staged for deletion)

---

### Task 3: Clean HF cache

**Files:**
- Delete: `~/.cache/huggingface/hub/models--mlx-community--Qwen3.5-2B-4bit/`

- [ ] **Step 1: Verify cache entry exists**

```bash
ls ~/.cache/huggingface/hub/models--mlx-community--Qwen3.5-2B-4bit/
```
Expected: directory exists with blob refs

- [ ] **Step 2: Delete the cache entry**

```bash
rm -rf ~/.cache/huggingface/hub/models--mlx-community--Qwen3.5-2B-4bit/
```

- [ ] **Step 3: Verify deletion**

```bash
ls ~/.cache/huggingface/hub/models--mlx-community--Qwen3.5-2B-4bit/ 2>&1
```
Expected: "No such file or directory"

---

### Task 4: Verify no remaining references

- [ ] **Step 1: Search codebase for active Qwen/MLX imports or dependencies**

```bash
grep -r "import mlx\|from mlx\|import qwen\|from qwen\|mlx_lm\|mlx-lm" <home>/Desktop/3_body_problem/ --include="*.py" --include="*.sh" --include="*.json" -l 2>/dev/null
```
Expected: no results (MLX/Qwen were never imported in project code)

- [ ] **Step 2: Check git status reflects all changes**

```bash
cd <home>/Desktop/3_body_problem && git status
```
Expected: `QWEN.md` deleted from index, `Qwen3.5-2B-4bit/` no longer shown as untracked

---

### Task 5: Commit

- [ ] **Step 1: Stage and commit**

```bash
git add QWEN.md
git commit -m "chore: remove QWEN.md agent instructions and Qwen 3.5 2B model directory

Qwen 3.5 2B 4-bit model (1.6 GB) and MLX are no longer used in this
project. Removes the QWEN.md agent instruction file and cleans up the
untracked model directory. MLX packages were already uninstalled."
```

---

## Verification

After all tasks:
- `Qwen3.5-2B-4bit/` no longer exists on disk (~1.6 GB freed)
- `QWEN.md` removed from git tracking
- HF cache entry cleaned
- No Python/shell scripts import mlx or qwen packages
- `.planning/` historical docs preserved (they record past decisions)
- `huggingface-hub` pip package kept (~80 KB, useful for future HF work)
