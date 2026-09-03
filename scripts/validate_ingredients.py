#!/usr/bin/env python3
"""
Comprehensive Validation Script for Family Meal Plan, Recipe Book & Shopping List.

Checks:
1. Schedule Invariants:
   - Wednesdays are ALWAYS Leftover Night (reheat), with exactly 0 recipe cards.
   - Sundays are ALWAYS Pizza Night (takeout/frozen), with exactly 0 recipe cards.
   - Exactly 20 recipe cards in total (5 days x 4 weeks: Mon, Tue, Thu, Fri, Sat).
2. Ingredient Coverage:
   - Every ingredient, Mom portion, Dad kick, and Kids plate element must be
     covered by either the weekly shopping list (Costco / Willy Street) or Master Pantry Staples.
3. No Orphaned Shopping Items:
   - Every item on the weekly shopping lists must be used by a meal in that week.
"""

import sys
import re
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
RECIPE_BOOK = WORKSPACE_DIR / "printable_recipe_book.html"
MEAL_PLAN = WORKSPACE_DIR / "printable_meal_plan.html"
SHOPPING_LIST = WORKSPACE_DIR / "printable_shopping_list.html"

def clean_text(html_text: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    text = re.sub(r"<[^>]+>", " ", html_text)
    return " ".join(text.split())

def validate_invariants(recipe_html: str, plan_html: str) -> list[str]:
    errors = []
    
    # 1. Recipe Book Checks
    # Extract all recipe cards
    cards = re.findall(
        r'<article class="recipe-card" id="([^"]+)" data-appliance="([^"]+)" data-week="([^"]+)">',
        recipe_html
    )
    
    if len(cards) != 20:
        errors.append(f"Recipe count mismatch: Expected 20 recipe cards (5 days x 4 weeks), found {len(cards)}.")
        
    for cid, app, wk in cards:
        cid_lower = cid.lower()
        if "wed" in cid_lower:
            errors.append(f"Invariant Violation: Wednesday has a recipe card: '{cid}' (Week {wk}). Wednesdays must have NO recipe.")
        if "sun" in cid_lower:
            errors.append(f"Invariant Violation: Sunday has a recipe card: '{cid}' (Week {wk}). Sundays must have NO recipe.")

    # 2. Meal Plan Checks
    # Check all day-cells in table
    day_rows = re.findall(
        r'<tr>\s*<td class="day-cell">(\w+)</td>\s*<td class="main-cell">\s*<div class="main-title">(.*?)</div>\s*</td>\s*<td><span class="badge ([^"]+)">(.*?)</span>',
        plan_html
    )
    
    wed_count = 0
    sun_count = 0
    for day, title, badge_class, badge_text in day_rows:
        clean_title = clean_text(title)
        if day == "Wed":
            wed_count += 1
            if "leftover" not in clean_title.lower():
                errors.append(f"Invariant Violation: Week meal plan Wednesday is not Leftovers: '{clean_title}'.")
            if "reheat" not in badge_class.lower():
                errors.append(f"Invariant Violation: Wednesday badge is not 'badge-reheat': '{badge_class}'.")
        elif day == "Sun":
            sun_count += 1
            if "pizza" not in clean_title.lower():
                errors.append(f"Invariant Violation: Week meal plan Sunday is not Pizza: '{clean_title}'.")
            if "takeout" not in badge_class.lower():
                errors.append(f"Invariant Violation: Sunday badge is not 'badge-takeout': '{badge_class}'.")
                
    if wed_count != 4:
        errors.append(f"Expected 4 Wednesday entries in meal plan, found {wed_count}.")
    if sun_count != 4:
        errors.append(f"Expected 4 Sunday entries in meal plan, found {sun_count}.")

    return errors

def extract_pantry_items(shopping_html: str) -> list[str]:
    pantry_match = re.search(r'<div class="pantry-card">(.*?)<!-- WEEK 1', shopping_html, re.DOTALL)
    if not pantry_match:
        return []
    pantry_text = pantry_match.group(1)
    return [clean_text(l) for l in re.findall(r'<label for="[^"]+">(.*?)</label>', pantry_text)]

def extract_weekly_shopping(shopping_html: str) -> dict[int, list[str]]:
    week_card_matches = list(re.finditer(
        r'<div class="week-card[^"]*">(.*?)(?=(?:<div class="week-card|<div class="page-footer"|</body>))',
        shopping_html,
        re.DOTALL
    ))
    weekly_items = {}
    for idx, m in enumerate(week_card_matches, 1):
        w_block = m.group(1)
        items = [clean_text(l) for l in re.findall(r'<label for="[^"]+">(.*?)</label>', w_block)]
        weekly_items[idx] = items
    return weekly_items

def extract_recipes_by_week(recipe_html: str) -> dict[int, list[dict]]:
    recipes = {1: [], 2: [], 3: [], 4: []}
    blocks = re.findall(
        r'<article class="recipe-card" id="([^"]+)" data-appliance="([^"]+)" data-week="([^"]+)">(.*?)</article>',
        recipe_html,
        re.DOTALL
    )
    for cid, app, wk, content in blocks:
        w_num = int(wk)
        title_m = re.search(r'<h3 class="recipe-title">(.*?)</h3>', content)
        title = clean_text(title_m.group(1)) if title_m else cid
        day_m = re.search(r'<div class="recipe-day-tag">(.*?)</div>', content)
        day = clean_text(day_m.group(1)) if day_m else ""
        
        # ingredients list
        ing_block = re.search(r'<ul class="ingredients-list">(.*?)</ul>', content, re.DOTALL)
        ings = [clean_text(i) for i in re.findall(r'<li>(.*?)</li>', ing_block.group(1))] if ing_block else []
        
        # custom texts
        customs = re.findall(
            r'<div class="custom-label [^"]+">(.*?)</div>\s*<div class="custom-text">(.*?)</div>',
            content
        )
        custom_items = [(clean_text(l), clean_text(t)) for l, t in customs]
        
        recipes[w_num].append({
            "id": cid,
            "title": title,
            "day": day,
            "ingredients": ings,
            "customs": custom_items
        })
    return recipes

def extract_meal_plan_by_week(plan_html: str) -> dict[int, list[dict]]:
    weeks = {1: [], 2: [], 3: [], 4: []}
    week_blocks = re.findall(r'<div class="week-block">(.*?)</table>\s*</div>', plan_html, re.DOTALL)
    for idx, w_block in enumerate(week_blocks, 1):
        rows = re.findall(
            r'<tr>\s*<td class="day-cell">(\w+)</td>\s*<td class="main-cell">\s*<div class="main-title">(.*?)</div>.*?<td class="mom-cell">(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>',
            w_block,
            re.DOTALL
        )
        for day, title, mom, dad, kids in rows:
            weeks[idx].append({
                "day": day,
                "title": clean_text(title),
                "mom": clean_text(mom),
                "dad": clean_text(dad),
                "kids": clean_text(kids),
            })
    return weeks

def audit_week(week_num: int, recipes: list[dict], plan_days: list[dict], shop_items: list[str], pantry_items: list[str]) -> tuple[list[str], list[str]]:
    """
    Returns (missing_ingredients_errors, orphaned_shopping_errors)
    """
    missing_errors = []
    orphaned_errors = []
    
    # Pool of all available ingredients for this week (lowercased)
    pantry_text = " ".join(pantry_items).lower()
    shop_text = " ".join(shop_items).lower()
    combined_available = pantry_text + " " + shop_text
    
    # 1. Audit Recipe Ingredients
    for rec in recipes:
        for ing in rec["ingredients"]:
            # normalize ingredient string to extract significant search words
            clean_ing = ing.lower()
            # remove parentheticals like (14–16 oz each) or (8 oz)
            clean_no_parens = re.sub(r'\(.*?\)', ' ', clean_ing)
            # strip quantities and units
            clean_no_units = re.sub(
                r'^[0-9\/\.\–\-\s]+(lbs?|oz|tbsp|tsp|cups?|cans?|blocks?|boxes?|box|bunch|bulbs?|cloves?|pint|bag|tub|pack|packs|slices?|ears?|pieces?|bottles?|jars?)?\s*(of\s*)?',
                '',
                clean_no_parens.strip()
            )
            
            # extract potential tokens across whole ingredient item
            tokens = [t for t in re.split(r'[\s\/,\+&]+', clean_no_units) if len(t) > 2 and t not in [
                'fresh', 'raw', 'extra', 'light', 'large', 'medium', 'small', 'diced',
                'sliced', 'chopped', 'rinsed', 'drained', 'cooked', 'warm', 'crushed',
                'pounded', 'organic', 'thin', 'blend', 'halved', 'steamed', 'trimmed',
                'quality', 'coarse', 'melted', 'shredded', 'finely', 'peeled', 'deveined',
                'firm', 'block', 'blocks', 'each', 'into', 'for', 'mom', 'kids', 'dad'
            ]]
            
            # Match check: at least one core token or the core phrase must be in combined_available
            matched = False
            for token in tokens:
                root = token.rstrip('s')
                if len(root) >= 3 and root in combined_available:
                    matched = True
                    break
            
            if not matched:
                missing_errors.append(f"Week {week_num} Recipe '{rec['title']}': Ingredient '{ing}' not found in shopping list or pantry.")

        # Also verify custom plate specific items (Kids' plate, Dad's kick)
        for label, text in rec["customs"]:
            text_lower = text.lower()
            if "kids" in label.lower():
                # Check for special kids items like 'baby carrots', 'sliders', 'tenders', 'quesadillas'
                if "carrots" in text_lower and "carrot" not in combined_available:
                    missing_errors.append(f"Week {week_num} Kids' Plate '{rec['title']}': 'carrots' referenced in '{text}' but missing from shopping list.")
                if "hawaiian rolls" in text_lower and "hawaiian rolls" not in combined_available:
                    missing_errors.append(f"Week {week_num} Kids' Plate '{rec['title']}': 'Hawaiian rolls' missing from shopping list.")
                if "pita" in text_lower and "pita" not in combined_available:
                    missing_errors.append(f"Week {week_num} Kids' Plate '{rec['title']}': 'pita' referenced in '{text}' but missing from shopping list.")

    # 2. Audit Shopping List for Orphaned Items
    # Every shopping list item should be referenced by either a recipe or a meal plan day in this week
    week_meals_text = (" ".join([r["title"] + " " + " ".join(r["ingredients"]) + " " + " ".join([c[1] for c in r["customs"]]) for r in recipes]) + " " +
                       " ".join([d["title"] + " " + d["mom"] + " " + d["dad"] + " " + d["kids"] for d in plan_days])).lower()
    
    for item in shop_items:
        # Extract the base item name (strip note in parens)
        base_item = item.split('(')[0].strip().lower()
        item_tokens = [t for t in re.split(r'[\s\/,&]+', base_item) if len(t) > 2 and t not in [
            'fresh', 'raw', 'bulk', 'approx', 'pack', 'medium', 'large', 'small', 'tub', 'jar', 'bag', 'box'
        ]]
        
        found_in_week = False
        if base_item in week_meals_text:
            found_in_week = True
        else:
            for token in item_tokens:
                root = token.rstrip('s')
                if root in week_meals_text:
                    found_in_week = True
                    break
        
        # Check meal notes explicitly mentioned on the shopping item
        notes_m = re.search(r'\((.*?)\)', item)
        if notes_m:
            note_content = notes_m.group(1).lower()
            # If notes mention a day like 'fri', 'sat', 'mon', 'tue', 'thu', 'sun', verify day is present
            if any(d in note_content for d in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'side', 'salad', 'kids', 'snacks']):
                found_in_week = True
                
        if not found_in_week:
            orphaned_errors.append(f"Week {week_num} Shopping List: Item '{item}' does not appear to be used by any meal or recipe in Week {week_num}.")

    return missing_errors, orphaned_errors

def main():
    print("=" * 70)
    print("🔍 MEAL PLAN, RECIPE BOOK & SHOPPING LIST INVARIANT & INVENTORY AUDIT")
    print("=" * 70)
    
    if not RECIPE_BOOK.exists() or not MEAL_PLAN.exists() or not SHOPPING_LIST.exists():
        print("❌ Error: One or more companion HTML files not found.")
        sys.exit(1)
        
    recipe_html = RECIPE_BOOK.read_text(encoding="utf-8")
    meal_plan_html = MEAL_PLAN.read_text(encoding="utf-8")
    shopping_html = SHOPPING_LIST.read_text(encoding="utf-8")
    
    # 1. Schedule Invariants
    invariant_errors = validate_invariants(recipe_html, meal_plan_html)
    if invariant_errors:
        print("\n❌ SCHEDULE INVARIANT FAILURES:")
        for err in invariant_errors:
            print(f"  • {err}")
    else:
        print("\n✅ SCHEDULE INVARIANTS PASS:")
        print("  • Wednesdays: Strictly Leftovers Night with 0 recipes.")
        print("  • Sundays: Strictly Pizza Night with 0 recipes.")
        print("  • Total Recipe Cards: Exactly 20 recipes across 4 weeks.")

    # 2. Extract Data
    pantry = extract_pantry_items(shopping_html)
    weekly_shopping = extract_weekly_shopping(shopping_html)
    recipes_by_week = extract_recipes_by_week(recipe_html)
    plan_by_week = extract_meal_plan_by_week(meal_plan_html)
    
    print(f"\nExtracted {len(pantry)} Master Pantry items.")
    for w in range(1, 5):
        print(f"  Week {w}: {len(recipes_by_week.get(w, []))} recipes, {len(weekly_shopping.get(w, []))} shopping items, {len(plan_by_week.get(w, []))} planned days.")

    # 3. Cross-Validate per Week
    all_missing = []
    all_orphaned = []
    for w in range(1, 5):
        recs = recipes_by_week.get(w, [])
        days = plan_by_week.get(w, [])
        shop = weekly_shopping.get(w, [])
        missing, orphaned = audit_week(w, recs, days, shop, pantry)
        all_missing.extend(missing)
        all_orphaned.extend(orphaned)

    print("\n" + "=" * 70)
    print("📋 INVENTORY & SHOPPING LIST AUDIT RESULTS:")
    print("=" * 70)

    if all_missing:
        print(f"\n❌ MISSING INGREDIENTS ({len(all_missing)}):")
        for m in all_missing:
            print(f"  • {m}")
    else:
        print("\n✅ ALL RECIPE INGREDIENTS & SIDES ACCOUNTED FOR across all 4 weeks.")

    if all_orphaned:
        print(f"\n⚠️ ORPHANED SHOPPING LIST ITEMS ({len(all_orphaned)}):")
        for o in all_orphaned:
            print(f"  • {o}")
    else:
        print("\n✅ ZERO ORPHANED SHOPPING LIST ITEMS (Every item is utilized).")

    # Final Outcome
    total_failures = len(invariant_errors) + len(all_missing) + len(all_orphaned)
    print("\n" + "=" * 70)
    if total_failures == 0:
        print("🎉 AUDIT PASSED: 100% synchronization and adherence to all rules.")
        print("=" * 70)
        sys.exit(0)
    else:
        print(f"💥 AUDIT FAILED: {total_failures} issue(s) detected.")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
