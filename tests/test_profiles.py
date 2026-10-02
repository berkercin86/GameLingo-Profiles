"""Offline checks for versioned GameLingo profile compatibility and risky aliases."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = ROOT / "profiles"


def load_profile(name):
    return json.loads((PROFILE_DIR / name).read_text(encoding="utf-8"))


def normalize_aliases(text, alias_map):
    # Mirror the app's length-prioritized token-boundary rule for regression
    # examples. This is a smoke check, not a replacement for Android tests.
    for original, replacement in sorted(
        alias_map.items(), key=lambda item: len(item[0]), reverse=True
    ):
        tokens = re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)?", original)
        if tokens:
            pattern = (
                r"(?<![A-Za-z0-9])" + r"\s+".join(map(re.escape, tokens))
                + r"(?![A-Za-z0-9])"
            )
            text = re.sub(pattern, lambda _: replacement, text, flags=re.I)
    return text


class CatalogContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = load_profile("index.json")
        cls.ragnarok = load_profile("god_of_war_ragnarok.json")

    def test_catalog_installed_profiles_match_files(self):
        self.assertEqual(self.index["schema_version"], 2)
        for game in self.index["games"]:
            if not game["available"]:
                continue
            profile = load_profile(game["file_name"])
            self.assertEqual(profile["schema_version"], 1)
            self.assertEqual(profile["id"], game["id"])
            self.assertEqual(profile["language"], "tr")
            self.assertEqual(profile["profile_version"], game["profile_version"])
            self.assertLess(
                (PROFILE_DIR / game["file_name"]).stat().st_size,
                512 * 1024 * 1024,
            )

    def test_unique_mapping_keys_and_parser_limits(self):
        for game in self.index["games"]:
            if not game["available"]:
                continue
            p = load_profile(game["file_name"])
            for key in ("translations", "glossary", "asr_aliases"):
                mapping = p.get(key, {})
                self.assertEqual(
                    len(mapping),
                    len({item.casefold() for item in mapping}),
                    f"{game['id']}/{key}: duplicate case-insensitive keys",
                )
                self.assertTrue(all(k.strip() and v.strip() for k, v in mapping.items()))
            self.assertLessEqual(len(p.get("asr_aliases", {})), 256)
            self.assertLessEqual(len(p.get("protected_names", [])) +
                                 len(p.get("glossary", {})), 384)
            self.assertLessEqual(len(p.get("translations", {})), 250_000)
            self.assertTrue(
                all(len(x) <= 1000 for x in p.get("translations", {}).values())
            )

    def test_ragnarok_v9_payload(self):
        p = self.ragnarok
        self.assertEqual(p["profile_version"], 9)
        self.assertGreaterEqual(len(p["protected_names"]), 70)
        self.assertGreaterEqual(len(p["glossary"]), 80)
        self.assertGreaterEqual(len(p["translations"]), 107)
        self.assertEqual(len(p["script_rescue_hashes"]), 3621)
        self.assertEqual(
            len(p["script_rescue_hashes"]),
            len(set(p["script_rescue_hashes"])),
        )
        for fingerprint in p["script_rescue_hashes"]:
            self.assertRegex(fingerprint, r"^[a-f0-9]{64}$")
        self.assertEqual(
            p["translations"]["I will not allow you to pick a fight with gods."],
            "Tanrılarla kavgaya tutuşmana izin vermeyeceğim.",
        )
        self.assertEqual(p["translations"]["I don't want to fight anyone."],
                         "Kimseyle savaşmak istemiyorum.")
        self.assertEqual(p["glossary"]["Draupnir Spear"],
                         "Draupnir Mızrağı")
        self.assertEqual(p["glossary"]["Sonic Arrows"],
                         "Sonik Oklar")
        self.assertEqual(
            p["translations"]["At least it didn't suffer."],
            "En azından acı çekmedi.",
        )
        self.assertEqual(
            p["translations"]["This is the natural order of things."],
            "Doğanın düzeni budur.",
        )
        self.assertEqual(
            p["asr_aliases"]["Emir himself sits atop your shoulders"],
            "Ymir himself sits atop your shoulders",
        )

    def test_short_observed_name_variants_only(self):
        aliases = self.ragnarok["asr_aliases"]
        self.assertNotIn("James", aliases)
        self.assertNotIn("fairies", aliases)
        self.assertEqual(
            normalize_aliases("He went to Needa Vellir.", aliases),
            "He went to Nidavellir.",
        )
        self.assertEqual(
            normalize_aliases("Fimbul Winter is coming.", aliases),
            "Fimbulwinter is coming.",
        )
        self.assertEqual(
            normalize_aliases("James is speaking to the fairies.", aliases),
            "James is speaking to the fairies.",
        )
        self.assertEqual(
            normalize_aliases("I'll allow you to pick a fight with God.", aliases),
            "I will not allow you to pick a fight with gods.",
        )


if __name__ == "__main__":
    unittest.main()
