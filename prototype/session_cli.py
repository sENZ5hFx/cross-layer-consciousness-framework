"""
CLCE Interactive Session CLI

Run: python prototype/session_cli.py

Commands during session:
  /goals           — show current goal hierarchy
  /memory          — show memory state
  /log             — show last 5 reflection events
  /awareness       — show current belief + uncertainty state
  /summary         — full session summary
  /quit or /exit   — exit session
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import CLCEOrchestrator
from embeddings import backend_info


BANNER = """
┌───────────────────────────────────────────────────────────────┐
│  CLCE — Cross-Layer Consciousness Engine           │
│  Phase 4 Interactive Session                      │
│  Type /quit to exit. Type /help for commands.     │
└───────────────────────────────────────────────────────────────┘
"""

HELP = """
Commands:
  /goals      Show goal hierarchy
  /memory     Show memory state
  /log        Show last 5 reflection events
  /awareness  Show beliefs and uncertainty flags
  /summary    Full session JSON summary
  /backend    Show embedding backend info
  /quit       Exit
"""


def main():
    print(BANNER)
    info = backend_info()
    print(f"  Embedding backend: {info['active_backend'].upper()}")
    if info["pseudo_fallback"]:
        print(f"  ⚠️  {info['upgrade_note']}")
    print()

    orc = CLCEOrchestrator()

    while True:
        try:
            user_input = input("you ❯ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit"):
            print("Session ended.")
            break

        if user_input == "/help":
            print(HELP)
            continue

        if user_input == "/goals":
            print(json.dumps(orc.mod_b.get_goal_hierarchy(), indent=2))
            continue

        if user_input == "/memory":
            print(json.dumps(orc.s2.get_state(), indent=2))
            continue

        if user_input == "/log":
            for e in orc.mod_c.get_audit_log()[-5:]:
                print(json.dumps(e, indent=2))
            continue

        if user_input == "/awareness":
            print(json.dumps(orc.mod_a.get_state_report(), indent=2))
            continue

        if user_input == "/summary":
            print(json.dumps(orc.get_session_summary(), indent=2))
            continue

        if user_input == "/backend":
            print(json.dumps(backend_info(), indent=2))
            continue

        result = orc.process(user_input)
        print(f"\n▶ {result.output}")
        print(f"  confidence={result.confidence:.3f}  coherence={result.coherence_score:.3f}  "
              f"action={result.reflection_action}  ⏱{result.elapsed_s}s\n")


if __name__ == "__main__":
    main()
