#!/bin/bash
#
# sync-ai-rules.sh
# Syncs shared rules from jordan-os/.ai-rules/ plus project-specific rules
# to .cursor/rules/ and .claude/rules/ in each project.
#
# Project-specific rules override shared rules when filenames conflict.
#
# Run from jordan-os directory: ./.ai-rules/sync-ai-rules.sh
#

set -e

# Get directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JORDAN_OS_DIR="$(dirname "$SCRIPT_DIR")"
SHARED_RULES_DIR="$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔄 Syncing AI rules across jordan-os projects..."
echo ""

# Discover projects (directories with CLAUDE.md or .git)
discover_projects() {
    local projects=()
    for dir in "$JORDAN_OS_DIR"/*/; do
        [ -d "$dir" ] || continue
        local name=$(basename "$dir")
        # Skip hidden directories and the .ai-rules directory itself
        [[ "$name" == .* ]] && continue
        # Check if it's a project (has CLAUDE.md or .git)
        if [ -f "$dir/CLAUDE.md" ] || [ -d "$dir/.git" ]; then
            projects+=("$name")
        fi
    done
    echo "${projects[@]}"
}

# Function to add alwaysApply: true to frontmatter
add_always_apply() {
    local input_file="$1"
    local output_file="$2"
    local value="${3:-true}"

    if head -1 "$input_file" | grep -q "^---$"; then
        if grep -q "alwaysApply:" "$input_file"; then
            cp "$input_file" "$output_file"
        else
            awk -v val="$value" '
                NR==1 { print; next }
                /^---$/ && !added { print "alwaysApply: " val; added=1 }
                { print }
            ' "$input_file" > "$output_file"
        fi
    else
        {
            echo "---"
            echo "alwaysApply: $value"
            echo "---"
            echo ""
            cat "$input_file"
        } > "$output_file"
    fi
}

# Sync rules to a single project
sync_project() {
    local project_name="$1"
    local project_dir="$JORDAN_OS_DIR/$project_name"
    local project_rules_dir="$project_dir/.ai-rules"
    local cursor_out="$project_dir/.cursor/rules"
    local claude_out="$project_dir/.claude/rules"
    local claude_skills_out="$project_dir/.claude/skills"

    echo -e "${BLUE}📦 $project_name${NC}"

    # Create output directories
    mkdir -p "$cursor_out" "$claude_out" "$claude_skills_out"

    # Track counts
    local global_count=0
    local conditional_count=0
    local skill_count=0

    # --- GLOBAL RULES ---
    # First: shared global rules
    if [ -d "$SHARED_RULES_DIR/global" ]; then
        for file in "$SHARED_RULES_DIR/global/"*.md; do
            [ -f "$file" ] || continue
            local basename=$(basename "$file" .md)
            # Check if project has override
            if [ -f "$project_rules_dir/global/$basename.md" ]; then
                continue  # Skip, project will override
            fi
            add_always_apply "$file" "$cursor_out/${basename}.mdc"
            global_count=$((global_count + 1))
        done
    fi

    # Then: project-specific global rules (override shared)
    if [ -d "$project_rules_dir/global" ]; then
        for file in "$project_rules_dir/global/"*.md; do
            [ -f "$file" ] || continue
            local basename=$(basename "$file" .md)
            add_always_apply "$file" "$cursor_out/${basename}.mdc"
            global_count=$((global_count + 1))
        done
    fi

    # --- CONDITIONAL RULES ---
    # First: shared conditional rules
    if [ -d "$SHARED_RULES_DIR/conditional" ]; then
        for file in "$SHARED_RULES_DIR/conditional/"*.md; do
            [ -f "$file" ] || continue
            local basename=$(basename "$file" .md)
            if [ -f "$project_rules_dir/conditional/$basename.md" ]; then
                continue  # Skip, project will override
            fi
            add_always_apply "$file" "$cursor_out/${basename}.mdc" "false"
            cp "$file" "$claude_out/${basename}.md"
            conditional_count=$((conditional_count + 1))
        done
    fi

    # Then: project-specific conditional rules
    if [ -d "$project_rules_dir/conditional" ]; then
        for file in "$project_rules_dir/conditional/"*.md; do
            [ -f "$file" ] || continue
            local basename=$(basename "$file" .md)
            add_always_apply "$file" "$cursor_out/${basename}.mdc" "false"
            cp "$file" "$claude_out/${basename}.md"
            conditional_count=$((conditional_count + 1))
        done
    fi

    # --- SKILLS (Claude Code only) ---
    # First: shared skills
    if [ -d "$SHARED_RULES_DIR/skills" ]; then
        for skill_dir in "$SHARED_RULES_DIR/skills/"*/; do
            [ -d "$skill_dir" ] || continue
            local skill_name=$(basename "$skill_dir")
            # Check if project has override
            if [ -d "$project_rules_dir/skills/$skill_name" ]; then
                continue  # Skip, project will override
            fi
            mkdir -p "$claude_skills_out/$skill_name"
            for file in "$skill_dir"*; do
                [ -f "$file" ] || continue
                cp "$file" "$claude_skills_out/$skill_name/"
            done
            skill_count=$((skill_count + 1))
        done
    fi

    # Then: project-specific skills
    if [ -d "$project_rules_dir/skills" ]; then
        for skill_dir in "$project_rules_dir/skills/"*/; do
            [ -d "$skill_dir" ] || continue
            local skill_name=$(basename "$skill_dir")
            mkdir -p "$claude_skills_out/$skill_name"
            for file in "$skill_dir"*; do
                [ -f "$file" ] || continue
                cp "$file" "$claude_skills_out/$skill_name/"
            done
            skill_count=$((skill_count + 1))
        done
    fi

    echo "   ✓ Global: $global_count | Conditional: $conditional_count | Skills: $skill_count"
}

# Main
echo "🔍 Discovering projects..."
projects=($(discover_projects))
echo "   Found: ${projects[*]}"
echo ""

for project in "${projects[@]}"; do
    sync_project "$project"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ Sync complete!${NC}"
echo ""
echo "Shared rules: $SHARED_RULES_DIR"
echo "Projects synced: ${#projects[@]}"
echo ""
echo -e "${YELLOW}Remember: Edit shared rules in jordan-os/.ai-rules/${NC}"
echo -e "${YELLOW}          Edit project rules in {project}/.ai-rules/${NC}"
