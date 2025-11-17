import re
import hashlib
from typing import List, Dict, Any

from .base_engine import BaseEngine


def _make_id(seed: str) -> str:
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()


class RegexEngine(BaseEngine):
    """Simple regex-based entity and relation extractor."""

    PERSON_RE = re.compile(r"([A-Z][a-z]+\s[A-Z][a-z]+)")
    AGE_RE = re.compile(r"age\s(\d{1,3})")
    WORKS_AT_RE = re.compile(r"([A-Z][a-z]+\s[A-Z][a-z]+).*?works\s+at\s+([A-Z][a-zA-Z0-9&\-\s]+?)(?:\s+as\b|\.|,)")
    COMPANY_ONLY_RE = re.compile(r"works\s+at\s+([A-Z][a-zA-Z0-9&\-\s]+?)(?:\s+as\b|\.|,)")
    MANAGES_RE = re.compile(r"([A-Z][a-z]+\s[A-Z][a-z]+)\s+(manages|directs|leads|oversees|coordinates|handles|supervises)\s+(\d+)\s+projects:?\s*(.*)\.")
    PROJECT_RE = re.compile(r"Project\s+([A-Za-z0-9\-]+)")
    PROJECT_LINE_RE = re.compile(r"Project\s+([A-Za-z0-9\-]+)\s.*started\s+on\s+(\d{4}-\d{2}-\d{2}),\s+ends\s+on\s+(\d{4}-\d{2}-\d{2})")
    COMPANY_INDUSTRY_RE = re.compile(r"([A-Z][a-zA-Z0-9&\-]+)\s.*(operates in|specializes in|focuses in|focuses on|works in|is known for)\s+(.*)\.")

    def extract_entities(self, text: str, entity_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        # Persons with age and position
        for person in set(self.PERSON_RE.findall(text)):
            # find age in nearest context
            age_match = self.AGE_RE.search(text)
            age = int(age_match.group(1)) if age_match else None
            entity_id = _make_id(f"Person::{person}")
            entities.append({
                "id": entity_id,
                "type": "Person",
                "text": person,
                "attributes": {"name": person, "age": age},
                "confidence": 0.9,
                "method": "regex",
            })

        # Companies: from person -> company matches
        works = self.WORKS_AT_RE.findall(text)
        for m in works:
            person, company = m[0], m[1].strip()
            entity_id = _make_id(f"Company::{company}")
            entities.append({
                "id": entity_id,
                "type": "Company",
                "text": company,
                "attributes": {"name": company},
                "confidence": 0.88,
                "method": "regex",
            })

        # Companies: standalone captures (works at <company>) in case person not matched with the same pattern
        companies = self.COMPANY_ONLY_RE.findall(text)
        for comp in companies:
            company = comp.strip()
            entity_id = _make_id(f"Company::{company}")
            entities.append({
                "id": entity_id,
                "type": "Company",
                "text": company,
                "attributes": {"name": company},
                "confidence": 0.8,
                "method": "regex",
            })

        # Projects from Project lines
        for m in self.PROJECT_LINE_RE.findall(text):
            name, start, end = m
            entity_id = _make_id(f"Project::{name}")
            entities.append({
                "id": entity_id,
                "type": "Project",
                "text": name,
                "attributes": {"name": name, "start_date": start, "end_date": end},
                "confidence": 0.92,
                "method": "regex",
            })

        # Locations and other companies
        for match in set(self.COMPANY_INDUSTRY_RE.findall(text)):
            company, _, industry = match
            entity_id = _make_id(f"Company::{company}")
            entities.append({
                "id": entity_id,
                "type": "Company",
                "text": company,
                "attributes": {"name": company, "industry": industry.strip()},
                "confidence": 0.85,
                "method": "regex",
            })

        # Deduplicate by id
        seen = {}
        for e in entities:
            if e["id"] not in seen:
                seen[e["id"]] = e
            else:
                # merge attributes
                seen[e["id"]]["attributes"].update({k: v for k, v in e["attributes"].items() if v is not None})
        return list(seen.values())

    def extract_relations(self, text: str, entities: List[Dict[str, Any]], relation_defs: Dict[str, Any]) -> List[Dict[str, Any]]:
        relations = []
        id_map = { (e["type"], e["text"]) : e["id"] for e in entities }

        # works_at relations
        for m in self.WORKS_AT_RE.findall(text):
            person, company = m[0], m[1]
            if ("Person", person) in id_map and ("Company", company) in id_map:
                relations.append({
                    "id": _make_id(f"works_at::{person}::{company}"),
                    "type": "works_at",
                    "source": id_map[("Person", person)],
                    "target": id_map[("Company", company)],
                    "attributes": {},
                    "confidence": 0.9,
                    "method": "regex",
                })

        # manages / leads / supervises -> person to project relations
        for m in self.MANAGES_RE.findall(text):
            person, _, _, proj_list = m
            # split project list by comma
            project_names = [p.strip() for p in re.split(r",\s*| and ", proj_list) if p.strip()]
            for p in project_names:
                # sometimes projects have names like Alpha, Beta
                # try to find project entity id in entities
                key = ("Project", p)
                if key in id_map:
                    relations.append({
                        "id": _make_id(f"manages::{person}::{p}"),
                        "type": "manages",
                        "source": id_map[("Person", person)],
                        "target": id_map[key],
                        "attributes": {},
                        "confidence": 0.85,
                        "method": "regex",
                    })

        # project period (start_date, end_date) -> relation linking project to dates
        for m in self.PROJECT_LINE_RE.findall(text):
            name, start, end = m
            pid = id_map.get(("Project", name))
            if pid:
                relations.append({
                    "id": _make_id(f"project_period::{name}::{start}-{end}"),
                    "type": "project_period",
                    "source": pid,
                    "target": None,
                    "attributes": {"start_date": start, "end_date": end},
                    "confidence": 0.9,
                    "method": "regex",
                })

        # company industry
        for m in self.COMPANY_INDUSTRY_RE.findall(text):
            company, _, industry = m
            cid = id_map.get(("Company", company))
            if cid:
                relations.append({
                    "id": _make_id(f"company_industry::{company}::{industry}"),
                    "type": "company_industry",
                    "source": cid,
                    "target": None,
                    "attributes": {"industry": industry.strip()},
                    "confidence": 0.87,
                    "method": "regex",
                })

        # deduplicate relations by id
        seen = {}
        for r in relations:
            if r["id"] not in seen:
                seen[r["id"]] = r
        return list(seen.values())
