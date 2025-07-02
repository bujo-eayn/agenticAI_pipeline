import unittest
import time
import json
import os
from graph.nodes.smoldocling_call import smoldocling_node


class TestSmoldoclingNodeReal(unittest.TestCase):

    def test_smoldocling_node_real_server(self):
        # ---- INPUT SETUP ----
        test_file_path = input(
            "📂 Enter full file path to test (e.g., ./samples/test.pdf): ").strip()
        if not os.path.exists(test_file_path):
            print("❌ File not found. Please provide a valid file path.")
            return

        state = {
            "file_path": test_file_path,
            "status_updates": []
        }

        # ---- NODE EXECUTION ----
        print("🚀 Sending file to SmolDocling server...")
        try:
            new_state = smoldocling_node(state)
        except Exception as e:
            print("❌ Request failed:", e)
            return

        # ---- DEBUG OUTPUT ----
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"debug_smoldocling_output_{timestamp}.json"
        output_path = os.path.join("debug_outputs", filename)
        os.makedirs("debug_outputs", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(new_state, f, indent=2)

        print(f"✅ SmolDocling output saved to: {output_path}")
        print("📋 Status Updates:")
        for line in new_state.get("status_updates", []):
            print("  -", line)


if __name__ == "__main__":
    unittest.main()
