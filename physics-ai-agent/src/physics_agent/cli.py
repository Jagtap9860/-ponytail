"""Command-line interface: solve, chat, convert, constants, formulas, demo."""
from __future__ import annotations

import argparse
import sys

from physics_agent.agent.orchestrator import Orchestrator
from physics_agent.config import get_settings


def _orch(args: argparse.Namespace) -> Orchestrator:
    s = get_settings()
    return Orchestrator(level=args.level or s.level, mode=args.mode or s.mode)


def cmd_solve(args: argparse.Namespace) -> int:
    ans = _orch(args).solve(args.problem)
    print(ans.report())
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    orch = _orch(args)
    print(f"Physics AI Agent (level={orch.level}, mode={orch.mode}). "
          "Type 'quit' to exit, 'level N' / 'mode NAME' to switch.")
    while True:
        try:
            text = input("\nphysics> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            return 0
        if text.lower() in {"quit", "exit"}:
            return 0
        if text.lower().startswith("level "):
            try:
                orch.level = int(text.split()[1])
                print(f"level → {orch.level}")
            except ValueError:
                print("usage: level 1|2|3|4")
            continue
        if text.lower().startswith("mode "):
            orch.mode = text.split()[1]
            print(f"mode → {orch.mode}")
            continue
        if not text:
            continue
        try:
            print(orch.solve(text).report())
        except Exception as e:  # noqa: BLE001 - CLI must not crash the session
            print(f"error: {e}")


def cmd_convert(args: argparse.Namespace) -> int:
    from physics_agent.units.converter import UnitConverter
    q = UnitConverter.parse(args.quantity)
    print(f"{q.value} {q.unit} = {UnitConverter.convert(q.value, q.unit, args.to)} {args.to}")
    return 0


def cmd_constants(args: argparse.Namespace) -> int:
    from physics_agent.knowledge.constants import CONSTANTS, search_constants
    items = search_constants(args.search) if args.search else list(CONSTANTS.values())
    for c in items:
        print(f"{c.symbol:6s} = {c.value:.10g} {c.unit:12s}  {c.name} [{c.source}]")
    return 0


def cmd_formulas(args: argparse.Namespace) -> int:
    from physics_agent.knowledge.formulas import FORMULAS, search_formulas
    items = search_formulas(args.search) if args.search else list(FORMULAS.values())
    for f in items[: (args.limit or 50)]:
        print(f.describe())
        print()
    return 0


def cmd_tools(_: argparse.Namespace) -> int:
    from physics_agent.tools import TOOLS
    for name, t in sorted(TOOLS.items()):
        print(f"{name:28s} {t.description}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    demos = {
        "spring": "A 10 kg mass is attached to a spring with k = 500 N/m. Find its natural frequency.",
        "machine-vibration": ("I have a 20 kg machine mounted on a spring with stiffness "
                              "50000 N/m and damping coefficient 100 Ns/m. What is its natural "
                              "frequency and resonance behavior?"),
        "projectile": "A projectile is launched at 25 m/s at 40 deg. Find its range.",
        "resonance": ("My ANSYS modal analysis shows a natural frequency of 217 Hz while my "
                      "operating excitation is 215 Hz. What does this mean?"),
    }
    if args.which not in demos:
        print(f"unknown demo. choose from: {sorted(demos)}")
        return 1
    print(Orchestrator().solve(demos[args.which]).report())
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="physics-agent", description="Interactive physics reasoning engine")
    p.add_argument("--level", type=int, default=0, help="explanation level 1-4 (0=from env)")
    p.add_argument("--mode", default="", help="direct|guided|teaching|exam|research|engineering")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("solve", help="solve a physics problem")
    s.add_argument("problem", help="problem text in quotes")
    s.set_defaults(func=cmd_solve)
    c = sub.add_parser("chat", help="interactive session")
    c.set_defaults(func=cmd_chat)
    v = sub.add_parser("convert", help="unit conversion")
    v.add_argument("quantity", help="'3000 rpm'")
    v.add_argument("to", help="'rad/s'")
    v.set_defaults(func=cmd_convert)
    k = sub.add_parser("constants", help="list/search constants")
    k.add_argument("--search", default="")
    k.set_defaults(func=cmd_constants)
    f = sub.add_parser("formulas", help="list/search formulas")
    f.add_argument("--search", default="")
    f.add_argument("--limit", type=int, default=20)
    f.set_defaults(func=cmd_formulas)
    t = sub.add_parser("tools", help="list callable tools")
    t.set_defaults(func=cmd_tools)
    d = sub.add_parser("demo", help="run a canned demo")
    d.add_argument("which", help="spring|machine-vibration|projectile|resonance")
    d.set_defaults(func=cmd_demo)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
