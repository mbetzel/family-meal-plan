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

## Mom's Dietary Standards & Nutrition Invariants

- **Daily Target Budget**: 1,350–1,450 kcal/day.
- **Macronutrient Ratio**: **30% Protein (~105g)** • **30% Fat (~46g)** • **40% Carbohydrates (~140g)**.
- **Dinner Calibration**: ~440–470 kcal per dinner (approx. 33% of daily intake).
- **Protein Source Restrictions**: **0% Red Meat and 0% Pork** (no ground beef, steak, pork chops, or pork bacon as primary protein). All core proteins must be **lean poultry** (chicken breast, tenderloins, 93/7 ground turkey) or **seafood** (salmon, wild cod, shrimp).
- **Carbohydrate Balancing**: Do NOT strip all carbohydrates from Mom's portions into zero-carb/keto. Always pair lean protein with nutrient-dense complex carbs (sweet potatoes, brown/wild rice, Banza chickpea pasta, whole wheat pitas/buns, corn, black beans) to satisfy her 40% carbohydrate target.

---

## Formatting & Design Consistency
- Preserve clean print stylesheets (`@media print`) across all three files so they remain printable/savable to PDF.
- Ensure the header navigation bar in each file links to the other two companion files.

---

## Tool & Command Execution Environment

- When running shell automation, file generation, or Python scripts, always execute via **WSL** (`wsl python3 ...` or `wsl <command>`) or write helper scripts to `scratch/` and invoke via WSL to ensure cross-platform consistency and prevent Windows PowerShell quoting errors.
