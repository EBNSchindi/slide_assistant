"""
Quick test script to verify variant generation works
"""
import sys
import os
from pathlib import Path

# Set TEST_MODE before any imports
os.environ["TEST_MODE"] = "true"

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from presentation.api.agents import AgentOrchestrator
from presentation.api.services import VariantStyleParser

# Test 1: Verify VariantStyleParser works
print("=" * 50)
print("TEST 1: VariantStyleParser")
print("=" * 50)

parser = VariantStyleParser()
profiles = parser.parse_variant_profiles()

print(f"✅ Loaded {len(profiles)} profiles:")
for profile in profiles:
    print(f"  - {profile['name']}: {profile.get('primary_color', 'N/A')}")

print("\n" + "=" * 50)
print("TEST 2: Variant Generation with Mock Agent")
print("=" * 50)

# Test 2: Test variant generation
orchestrator = AgentOrchestrator(api_key="test", model="mock", test_mode=True)

# Get project root directory dynamically
project_root = Path(__file__).parent.parent.parent
test_project_path = project_root / "presentation" / "projects" / "beispiel-projekt"

result = orchestrator.process(
    user_input="Test content for variant generation",
    project_path=str(test_project_path),
    project_name="beispiel-projekt",
    slide_title="test-variant-slide",
    preferences={"generate_variants": True},
)

print(f"\n✅ Success: {result['success']}")
print(f"✅ Agent steps: {len(result['agent_steps'])}")
print(f"✅ Generated slides: {len(result['generated_slides'])}")

# Print any errors
for step in result['agent_steps']:
    if step['status'] == 'error':
        print(f"❌ Error in {step['agent_name']}: {step.get('error', 'Unknown error')}")

if result['generated_slides']:
    slide = result['generated_slides'][0]
    print(f"✅ Slide name: {slide['slide_name']}")

    if 'variants' in slide:
        print(f"✅ Variants generated: {len(slide['variants'])}")
        for variant in slide['variants']:
            print(f"  - Profile: {variant['profile']}")
    else:
        print("⚠️ No variants found in slide")

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
