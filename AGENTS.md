# Family Meal Planning & Recipe Synchronization Rules

## Core Rule: Synchronized Triple Updates

Whenever any meal plan change, recipe addition, ingredient substitution, day swap, or customization update occurs, **ALL THREE** of the following companion documents must be updated in sync:

1. **`printable_meal_plan.html`** (Meal Plan Schedule)
   - Keep the 4-week calendar tables accurate.
   - Ensure dinner titles, cooking methods/badges (Air Fryer, Grill, Instant Pot, Skillet, Oven), Mom's calibrated portion notes with macro badges, Dad's flavor kicks, and Kids' plates match.

2. **`printable_shopping_list.html`** (Grocery Shopping List)
   - Keep the weekly store breakdown aligned:
     - **Costco Wholesale**: Bulk lean poultry (chicken breasts/tenders, 93/7 ground turkey), seafood (salmon, cod, shrimp), complex carbs (sweet potatoes, brown/wild rice, Banza pasta), bulk dairy, and master pantry staples.
     - **Willy Street Co-op North**: Fresh produce, specialty condiments (toum, harissa, kimchi, chili oils, artisan breads/tortillas).
   - Ensure item notes accurately reference which night/meal requires the ingredient.

3. **`printable_recipe_book.html`** (Detailed Recipe Book)
   - Keep the Table of Contents jump links updated.
   - Maintain the standard recipe card format:
     - Appliance badge, Prep time, Cook time, Yield.
     - Exact ingredient measurements matching grocery lists.
     - Step-by-step numbered cooking instructions (~30 min target).
     - 🥗 **Mom's Portion** (Calibrated 440–470 kcal, 35–42g Protein, 13–16g Healthy Fats, 42–48g Complex Carbs; include explicit macro badge `🎯 Mom's Macros`).
     - 🌶️ **Dad's Flavor** (spicy kicks, hot honey, chili crunch, toum, harissa, jalapeños).
     - 🧒 **Kids' Plate** (mild, deconstructed, kid-favorite sides, or dedicated kid alternatives on fish nights).

---

## Mandatory Subagent Ingredient & Invariant Validation

**Every single time** there is a change to the meal plan, recipe book, or grocery list:
1. You **MUST** run the `ingredient-validator` subagent (or execute `wsl python3 scripts/validate_ingredients.py`).
2. The validator systematically verifies:
   - **All ingredients accounted for**: Every ingredient across recipes, Mom's portions, Dad's kicks, and Kids' plates is covered by either the weekly shopping list (Costco Wholesale or Willy Street Co-op) or Master Pantry Staples.
   - **Zero orphaned shopping items**: No ingredient appears on a weekly shopping list without being utilized by at least one meal/side in that week.
   - **Strict schedule invariants**:
     - **Wednesdays are ALWAYS Leftovers Night** with reheat instructions and **NO recipe card** in `printable_recipe_book.html`.
     - **Sundays are ALWAYS Pizza Night** (takeout or frozen pizza + salad) and **NO recipe card** in `printable_recipe_book.html`.
3. If any discrepancy is flagged by the validator, fix all companion documents immediately before completing the turn.

---

## Schedule Invariants & Dietary Standards

- **Wednesday Leftover Night Invariant**: Wednesdays are strictly Family Leftovers Night (reheat previous nights' meals). There must be **NO recipe associated with Wednesdays** in `printable_recipe_book.html`.
- **Sunday Pizza Night Invariant**: Sundays are strictly Pizza Night (order out or frozen pizza with high-protein side salad). There must be **NO recipe associated with Sundays** in `printable_recipe_book.html`.
- **Thursday Vegetarian Cadence**: Thursdays are strictly High-Protein Vegetarian (extra-firm tofu, chickpeas, black beans, cannellini beans).
- **Daily Target Budget**: 1,350–1,450 kcal/day.
- **Macronutrient Ratio**: **30% Protein (~105g)** • **30% Fat (~46g)** • **40% Carbohydrates (~140g)**.
- **Dinner Calibration**: ~440–470 kcal per dinner (approx. 33% of daily intake).
- **Protein Source Restrictions & Cadence**: Core proteins emphasize **lean poultry** (chicken breast, tenderloins, 93/7 ground turkey), **seafood** (salmon, wild cod, shrimp), **high-protein plant-forward meals** (1 night/week), and **lean red meat** (90/10 lean ground beef, flank steak; bi-weekly on Weeks 1 & 3). Zero pork/bacon.
- **Carbohydrate Balancing**: Do NOT strip all carbohydrates from Mom's portions into zero-carb/keto. Always pair lean protein with nutrient-dense complex carbs (sweet potatoes, brown/wild rice, Banza chickpea pasta, whole wheat pitas/buns, corn, black beans) to satisfy her 40% carbohydrate target.

---

## Formatting & Design Consistency
- Preserve clean print stylesheets (`@media print`) across all three files so they remain printable/savable to PDF.
- Ensure the header navigation bar in each file links to the other two companion files.

---

## Tool & Command Execution Environment

- When running shell automation, file generation, or Python scripts, always execute via **WSL** (`wsl python3 ...` or `wsl <command>`) or write helper scripts to `scratch/` and invoke via WSL to ensure cross-platform consistency and prevent Windows PowerShell quoting errors.
