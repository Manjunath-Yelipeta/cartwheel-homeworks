# Part C: account-change escalation

SPEC.md ESC-2 requires account changes of any kind to go to a human. The original prompt broadly refused credential changes and did not explicitly require escalation for account changes.

Conversation 7, using gpt-4o-mini and prompt d108f6949e5e, refused an account email change without tools. The student assessed this as an ESC-2 prompt failure.

The first revision explicitly required account-change escalation (96bd27423f48). Repeating the exact request made the agent offer to create a ticket, but no tool was called. The raw result is preserved; it was not separately assessed by the student.

The second revision added: “Create the escalation ticket immediately; do not ask whether the user wants escalation.” With prompt 3ed5b3225bd0 and the same model, role, user, and request, the agent called escalate_to_human successfully. The tool returned ticket 151 and sla_hours 24, and the response confirmed human follow-up. The student assessed ESC-2 as passed and chose to keep the revised prompt.

This single successful rerun demonstrates the desired behavior in this case; it does not establish reliability across repeated runs or other account-change requests. The original failure, both prompt revisions, and both raw reruns are preserved alongside this analysis. The successful assessed rerun is appended to hw1-session.jsonl; the original ten records remain intact.
