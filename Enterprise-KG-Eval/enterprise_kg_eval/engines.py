import re
from typing import List, Dict, Any


class BaseEngine:
    """Abstract engine. Implement extract_entities and extract_relations."""

    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def extract_relations(self, text: str, rel_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError


class RegexEngine(BaseEngine):
    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        found = []
        for ent_name, edef in entity_defs.items():
            # support edef as dict with 'pattern' or list of example strings
            if isinstance(edef, dict):
                pattern = edef.get('pattern')
                examples = edef.get('examples', [])
            elif isinstance(edef, list):
                pattern = None
                examples = edef
            else:
                pattern = None
                examples = []

            if pattern:
                for m in re.finditer(pattern, text, flags=re.I):
                    found.append({
                        'type': ent_name,
                        'text': m.group(0),
                        'start': m.start(),
                        'end': m.end(),
                    })

            for val in examples:
                idx = text.lower().find(str(val).lower())
                if idx >= 0:
                    found.append({
                        'type': ent_name,
                        'text': text[idx:idx + len(str(val))],
                        'start': idx,
                        'end': idx + len(str(val)),
                    })
        return found

    def extract_relations(self, text: str, rel_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        found = []
        # Very simple relation extraction using proximity + keyword patterns
        for rel_name, rdef in rel_defs.items():
            if isinstance(rdef, dict):
                keywords = rdef.get('keywords', [])
                typ_a = rdef.get('arg_a')
                typ_b = rdef.get('arg_b')
            elif isinstance(rdef, list):
                keywords = []
                typ_a = rdef[0] if len(rdef) > 0 else None
                typ_b = rdef[1] if len(rdef) > 1 else None
            else:
                keywords = []
                typ_a = None
                typ_b = None

            for kw in keywords:
                for m in re.finditer(re.escape(kw), text, flags=re.I):
                    # naive: capture neighbor tokens
                    window = text[max(0, m.start()-50):m.end()+50]
                    found.append({'type': rel_name, 'trigger': kw, 'context': window})

            if not keywords and typ_a and typ_b:
                # naive: check if both tokens occur in same text
                if typ_a.lower() in text.lower() and typ_b.lower() in text.lower():
                    found.append({'type': rel_name, 'args': [typ_a, typ_b]})
        return found


class StubLLMEngine(BaseEngine):
    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        # deterministic stub: use example values; also support list defs
        found = []
        for ent_name, edef in entity_defs.items():
            if isinstance(edef, dict):
                values = edef.get('examples', [])
            elif isinstance(edef, list):
                values = edef
            else:
                values = []
            for val in values:
                idx = text.lower().find(str(val).lower())
                if idx >= 0:
                    found.append({'type': ent_name, 'text': val, 'start': idx, 'end': idx + len(str(val))})
        return found

    def extract_relations(self, text: str, rel_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        # naive stub: match relation examples
        found = []
        for rel_name, rdef in rel_defs.items():
            examples = rdef.get('examples', [])
            for ex in examples:
                if ex.lower() in text.lower():
                    found.append({'type': rel_name, 'example': ex})
        return found
