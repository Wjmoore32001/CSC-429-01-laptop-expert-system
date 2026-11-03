from engine import ForwardChainingEngine
from kb_loader import load_rules

KB_PATH = "kb/laptop_rules.json"


def collect_initial_facts():
    facts = []

    # Ask questions to collect facts for reasoning
    if input("Is portability important? (y/n): ").lower().startswith("y"):
        facts.append("portable")

    if input("Do you need long battery life? (y/n): ").lower().startswith("y"):
        facts.append("long_battery")

    if input("Is your budget high? (y/n): ").lower().startswith("y"):
        facts.append("budget_high")
    elif input("Is your budget medium? (y/n): ").lower().startswith("y"):
        facts.append("budget_medium")
    else:
        facts.append("budget_low")

    if input("Will you use it for gaming? (y/n): ").lower().startswith("y"):
        facts.append("gaming")

    if input("Will you use it for creative work? (y/n): ").lower().startswith("y"):
        facts.append("creative_work")

    if input("Will you use it only for office work? (y/n): ").lower().startswith("y"):
        facts.append("office_only")

    if input("Do you need a large screen? (y/n): ").lower().startswith("y"):
        facts.append("large_screen")

    if input("Do you travel often? (y/n): ").lower().startswith("y"):
        facts.append("travel_often")

    if input("Do you need AI acceleration? (y/n): ").lower().startswith("y"):
        facts.append("needs_ai_accel")

    os = input("Preferred OS (windows/macos/linux/none): ").lower().strip()
    if os in ["windows", "macos", "linux"]:
        facts.append("pref_os_" + os)

    return facts


def main():
    # Load rules and create the inference engine
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)

    # Collect facts from the user
    facts = collect_initial_facts()
    engine.assert_facts(facts)

    # Run forward chaining
    engine.run()

    # Display results
    results = engine.conclusions()

    print("\nRecommendations:")
    if results["recommendations"]:
        for recommendation in results["recommendations"]:
            print("-", recommendation)
    else:
        print("No recommendations found.")

    print("\nSpecifications:")
    if results["specs"]:
        for spec in results["specs"]:
            print("-", spec)
    else:
        print("No additional specifications.")

    print("\nRules Fired:")
    for step in engine.trace:
        print(step["rule"], "->", step["conclusion"])


if __name__ == "__main__":
    main()
