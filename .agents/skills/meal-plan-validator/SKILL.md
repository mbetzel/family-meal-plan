---
name: meal-plan-validator
description: >-
  Use this skill whenever editing, swapping, or adding meals or recipes in printable_meal_plan.html,
  printable_recipe_book.html, or printable_shopping_list.html. It guides the multi-step verification
  of schedule invariants, ingredient accounting, subagent validation, and zero orphaned grocery items.
---

# Meal Plan, Recipe & Ingredient Validation

This skill outlines the standard validation runbook to ensure full synchronization across the family meal planning documents.

## Strict Schedule Invariants

1. **Wednesdays are ALWAYS Leftovers Night**:
   - Reheat instructions only (`badge-reheat`).
   - Strictly **NO recipe card** in `printable_recipe_book.html`.
2. **Sundays are ALWAYS Pizza Night**:
   - Takeout or frozen pizza + high-protein salad (`badge-takeout`).
   - Strictly **NO recipe card** in `printable_recipe_book.html`.
3. **Active Cooking Count**:
   - Exactly 20 recipe cards in `printable_recipe_book.html` (5 days x 4 weeks: Mon, Tue, Thu, Fri, Sat).

## Mandatory Triple Update Sequence

Whenever modifying a meal or recipe:
1. Update `printable_meal_plan.html` (4-week calendar, Mom's macros, Dad's kicks, Kids' plates).
2. Update `printable_recipe_book.html` (recipe card, ingredients, steps, customizations).
3. Update `printable_shopping_list.html` (Costco Wholesale bulk proteins/staples, Willy Street Co-op produce/specialty, meal annotations).

## Validation & Verification Workflow

### Step 1: Run the Automated Validation Suite
Execute the automated validator in WSL:
```bash
wsl python3 scripts/validate_ingredients.py
```

The script verifies:
- Exactly 20 recipe cards.
- Zero Wednesday recipe cards and zero Sunday recipe cards.
- Every recipe ingredient, Mom portion, Dad kick, and Kid side is accounted for in Costco, Willy Street, or Master Pantry.
- Zero orphaned shopping list items (every item has an active meal consumer).

### Step 2: Invoke the `ingredient-validator` Subagent
Whenever complex modifications or batch edits occur, invoke the dedicated subagent:
```json
{
  "TypeName": "ingredient-validator",
  "Role": "Ingredient & Invariant Auditor",
  "Prompt": "Audit printable_meal_plan.html, printable_recipe_book.html, and printable_shopping_list.html via scripts/validate_ingredients.py and verify zero missing ingredients, zero orphaned items, and strict Wed/Sun invariants."
}
```

### Step 3: Fix Discrepancies Before Completion
If any missing or orphaned ingredients are reported:
1. Update the appropriate store section in `printable_shopping_list.html`.
2. Re-run `wsl python3 scripts/validate_ingredients.py` until it exits with code 0:
   `🎉 AUDIT PASSED: 100% synchronization and adherence to all rules.`
