# ============================================
# NEETI.PY — ETHICS & STRATEGY GATE
# Auto-approves or flags based on your rules
# ============================================

from config import RULES

class NeetiAgent:
    """Approval Gate — Your rules, automated"""

    FORBIDDEN_PHRASES = [
        "kill them", "attack him", "beat them", 
        "violent overthrow", "destroy them", "eliminate"
    ]

    def __init__(self, content_queue):
        self.queue = content_queue
        self.approved = []
        self.flagged = []

    def evaluate(self, piece):
        """Evaluate single content piece"""
        score = 0
        flags = []
        content_lower = piece["content"].lower()

        forbidden_found = [p for p in self.FORBIDDEN_PHRASES if p in content_lower]
        if forbidden_found:
            score += 10
            flags.append(f"FORBIDDEN: {forbidden_found}")

        has_solution = any(word in content_lower for word in ["solution", "framework", "1)", "action", "approach"])
        if RULES["must_include_solution"] and not has_solution:
            score += 5
            flags.append("NO_SOLUTION")

        attack_phrases = ["chor hai", "dhokhebaaz", "nalayak", "useless person", "criminal"]
        found_attacks = [p for p in attack_phrases if p in content_lower]
        if RULES["no_personal_attacks"] and found_attacks:
            score += 8
            flags.append(f"ATTACK: {found_attacks}")

        focus_match = any(cat in piece.get("policy_angle", "").lower() for cat in RULES["focus_areas"])
        if not focus_match and "general" not in piece.get("policy_angle", "").lower():
            score += 2
            flags.append("OFF_FOCUS")

        return {
            "score": score,
            "flags": flags,
            "decision": "APPROVE" if score == 0 else "FLAG",
            "reason": "Clean — ready to post" if score == 0 else " | ".join(flags)
        }

    def run(self):
        """Full evaluation cycle"""
        print("[NEETI] Evaluating content against your rules...")
        print(f"       Religion: {'OK' if RULES['religion_ok'] else 'Restricted'}")
        print(f"       Must have solution: {'YES' if RULES['must_include_solution'] else 'NO'}")
        print(f"       No personal attacks: {'YES' if RULES['no_personal_attacks'] else 'NO'}")

        for piece in self.queue:
            result = self.evaluate(piece)

            item = {
                "variant_id": piece["variant_id"],
                "format": piece["format"],
                "content": piece["content"],
                "evaluation": result
            }

            if result["decision"] == "APPROVE":
                self.approved.append(item)
                print(f"   ✅ {piece['variant_id']} — APPROVED")
            else:
                self.flagged.append(item)
                print(f"   ⚠️  {piece['variant_id']} — FLAGGED: {result['reason']}")

        print(f"[NEETI] Result: {len(self.approved)} approved | {len(self.flagged)} flagged")
        return self.approved, self.flagged
