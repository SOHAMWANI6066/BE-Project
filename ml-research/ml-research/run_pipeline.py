import sys
import json
import traceback

from pipeline.analyze_clause import analyze_clause


def main():
    try:
        # Read entire stdin
        raw_input = sys.stdin.read()

        if not raw_input:
            print(json.dumps({"error": "No input received"}))
            sys.exit(1)

        clauses = json.loads(raw_input)

        if not isinstance(clauses, list):
            print(json.dumps({"error": "Expected list of clauses"}))
            sys.exit(1)

        results = []

        for clause in clauses:
            try:
                result = analyze_clause(clause)
                results.append(result)
            except Exception as e:
                results.append({
                    "error": str(e)
                })

        # 🔥 CRITICAL — only JSON output
        print(json.dumps(results))

    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "trace": traceback.format_exc()
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()