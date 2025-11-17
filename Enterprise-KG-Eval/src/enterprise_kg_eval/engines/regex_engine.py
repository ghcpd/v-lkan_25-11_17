"""Rule-based extraction engine built on regular expressions."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

from ..config_loader import EntitySchema, RelationSchema
from ..data_loader import Document
from ..models import EntityPrediction, RelationPrediction
from .base import ExtractionEngine


class RegexExtractionEngine(ExtractionEngine):
    """Simple heuristic engine designed for semi-structured text."""

    KEY_VALUE_PATTERN = re.compile(
        r"(?P<label>[A-Za-z][A-Za-z _/]{1,40})\s*[:=]\s*(?P<value>[^|\n;]+)"
    )

    ENTITY_PATTERNS: Dict[str, Sequence[re.Pattern]] = {
        "Person": [
            re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"),
        ],
        "Company": [
            re.compile(
                r"\b[A-Z][\w& ]+(?:Corporation|Corp|Company|Inc\.?|LLC|Ltd\.?|Group)\b"
            )
        ],
        "Project": [
            re.compile(r"\bProject\s+[A-Z][\w-]+\b"),
        ],
        "Department": [
            re.compile(r"\b[A-Z][a-z]+ Department\b"),
            re.compile(r"Department of [A-Z][a-z]+"),
        ],
        "Position": [
            re.compile(
                r"\b(?:Director|Manager|Lead|Engineer|Specialist|Analyst|Architect)\b",
                re.IGNORECASE,
            )
        ],
        "Technology": [
            re.compile(r"\b[A-Z]{2,}(?:\s+[A-Z0-9]{2,})*\b"),
            re.compile(r"\bVersion\s+\d+(?:\.\d+)*\b", re.IGNORECASE),
        ],
        "Location": [
            re.compile(
                r"\b(?:New York|San Francisco|London|Berlin|Paris|Tokyo|Singapore|Sydney)\b"
            ),
            re.compile(r"\b[A-Z][a-z]+,\s*[A-Z][a-z]+\b"),
        ],
        "Team": [
            re.compile(r"\bTeam\s+[A-Z][\w-]+\b"),
        ],
        "Product": [
            re.compile(r"\bProduct\s+[A-Z][\w-]+\b"),
            re.compile(r"\b[A-Z][\w-]+ Platform\b"),
        ],
        "Client": [
            re.compile(r"\bClient\s+[A-Z][\w-]+\b"),
            re.compile(r"\b[A-Z][\w-]+ Holdings\b"),
        ],
    }

    ENTITY_ALIASES = {
        "employee": "Person",
        "staff": "Person",
        "manager": "Person",
        "company name": "Company",
        "project name": "Project",
        "dept": "Department",
        "department name": "Department",
        "role": "Position",
        "technology stack": "Technology",
        "city": "Location",
        "office": "Location",
        "team name": "Team",
        "product name": "Product",
        "client name": "Client",
    }

    RELATION_KEYWORDS: Dict[str, Sequence[str]] = {
        "works_at": ["works at", "employed at", "joined"],
        "manages": ["manages", "managing"],
        "leads": ["leads", "lead of"],
        "supervises": ["supervises", "supervision"],
        "project_period": ["project", "timeline", "period"],
        "company_industry": ["industry", "sector"],
        "employed_in": ["in the", "department"],
        "located_at": ["located", "based in", "headquartered"],
        "belongs_to": ["belongs to", "part of"],
        "assigned_to": ["assigned to", "assigned on"],
        "collaborates_with": ["collaborates with", "collaboration"],
        "reports_to": ["reports to", "reporting to"],
        "develops": ["develops", "building"],
        "uses_technology": ["uses", "leverages", "powered by"],
        "serves_client": ["serves", "engages", "supports"],
        "has_position": ["serves as", "working as", "position"],
        "team_member": ["team member", "member of"],
        "project_technology": ["technology", "stack"],
        "client_contract": ["contract", "agreement"],
        "department_head": ["heads", "heading", "director of"],
        "office_location": ["based in", "office", "located"],
        "project_budget": ["budget", "funding"],
        "technology_stack": ["stack", "technology"],
        "team_lead": ["team lead", "leads"],
        "product_manager": ["product manager", "manages"],
        "client_relationship": ["relationship", "engagement"],
        "cross_functional": ["cross-functional", "partners with"],
        "mentors": ["mentors", "coaches"],
        "project_stakeholder": ["stakeholder", "sponsor"],
        "vendor_relationship": ["vendor", "partnership"],
        "subsidiary_of": ["subsidiary", "owned by"],
    }

    SENTENCE_PATTERN = re.compile(r"[^.!?]+[.!?]?")
    DATE_PATTERN = re.compile(
        r"\b(?:\d{4}-\d{2}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b",
        re.IGNORECASE,
    )
    MONEY_PATTERN = re.compile(
        r"\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*(?:USD|EUR|GBP|million|billion|k)?",
        re.IGNORECASE,
    )

    def extract_entities(
        self, document: Document, entity_schema: EntitySchema
    ) -> List[EntityPrediction]:
        predictions: List[EntityPrediction] = []
        predictions.extend(self._extract_key_value_entities(document, entity_schema))
        predictions.extend(self._extract_regex_entities(document, entity_schema))
        return self._dedupe_entities(predictions)

    def extract_relations(
        self,
        document: Document,
        entity_predictions: List[EntityPrediction],
        relation_schema: RelationSchema,
    ) -> List[RelationPrediction]:
        sentences = list(self._iter_sentences(document.text))
        entities_by_type = defaultdict(list)
        for entity in entity_predictions:
            entities_by_type[entity.entity_type].append(entity)

        entity_type_names = set(entities_by_type.keys())
        relation_candidates: List[RelationPrediction] = []
        for relation_name, signature in relation_schema.items():
            entity_types = [item for item in signature if item in entity_type_names]
            attribute_names = [item for item in signature if item not in entity_type_names]

            if len(entity_types) >= 2:
                src_type, tgt_type = entity_types[:2]
                relation_candidates.extend(
                    self._match_entity_pair_relation(
                        relation_name,
                        src_type,
                        tgt_type,
                        entities_by_type,
                        sentences,
                    )
                )
            elif entity_types and attribute_names:
                relation_candidates.extend(
                    self._match_attribute_relation(
                        relation_name,
                        entity_types[0],
                        attribute_names,
                        entities_by_type,
                        sentences,
                    )
                )

        return self._dedupe_relations(relation_candidates)

    # ------------------------------------------------------------------ #
    # Entity helpers
    # ------------------------------------------------------------------ #
    def _extract_key_value_entities(
        self, document: Document, entity_schema: EntitySchema
    ) -> Iterable[EntityPrediction]:
        results: List[EntityPrediction] = []
        for match in self.KEY_VALUE_PATTERN.finditer(document.text):
            label = match.group("label").strip()
            value = match.group("value").strip()
            entity_type = self._map_label_to_entity(label, entity_schema)
            if not entity_type:
                continue
            attributes = self._collect_attributes(entity_type, document.text, entity_schema)
            results.append(
                EntityPrediction(
                    entity_type=entity_type,
                    text=value,
                    start=match.start("value"),
                    end=match.end("value"),
                    confidence=0.9,
                    attributes=attributes,
                )
            )
        return results

    def _extract_regex_entities(
        self, document: Document, entity_schema: EntitySchema
    ) -> Iterable[EntityPrediction]:
        results: List[EntityPrediction] = []
        for entity_type, patterns in self.ENTITY_PATTERNS.items():
            if entity_type not in entity_schema:
                continue
            for pattern in patterns:
                for match in pattern.finditer(document.text):
                    text = match.group().strip()
                    attributes = self._collect_attributes(
                        entity_type, document.text, entity_schema
                    )
                    results.append(
                        EntityPrediction(
                            entity_type=entity_type,
                            text=text,
                            start=match.start(),
                            end=match.end(),
                            confidence=0.6,
                            attributes=attributes,
                        )
                    )
        return results

    def _map_label_to_entity(
        self, label: str, entity_schema: EntitySchema
    ) -> str | None:
        normalized = label.strip().lower()
        for entity_type in entity_schema:
            if normalized == entity_type.lower():
                return entity_type
            if normalized.endswith(f" {entity_type.lower()}"):
                return entity_type
            if entity_type.lower() in normalized:
                return entity_type
        if normalized in self.ENTITY_ALIASES:
            alias = self.ENTITY_ALIASES[normalized]
            if alias in entity_schema:
                return alias
        return None

    def _collect_attributes(
        self, entity_type: str, text: str, entity_schema: EntitySchema
    ) -> Dict[str, str]:
        attributes: Dict[str, str] = {}
        for attribute in entity_schema.get(entity_type, []):
            pattern = re.compile(
                rf"{re.escape(attribute)}\s*[:=]\s*(?P<value>[^|\n;]+)", re.IGNORECASE
            )
            match = pattern.search(text)
            if match:
                attributes[attribute] = match.group("value").strip()
        return attributes

    def _dedupe_entities(self, predictions: Iterable[EntityPrediction]) -> List[EntityPrediction]:
        unique: Dict[Tuple[str, int, int], EntityPrediction] = {}
        for entity in predictions:
            key = (entity.entity_type, entity.start, entity.end)
            existing = unique.get(key)
            if not existing or entity.confidence > existing.confidence:
                unique[key] = entity
        return list(unique.values())

    # ------------------------------------------------------------------ #
    # Relation helpers
    # ------------------------------------------------------------------ #
    def _match_entity_pair_relation(
        self,
        relation_name: str,
        src_type: str,
        tgt_type: str,
        entities_by_type: Dict[str, List[EntityPrediction]],
        sentences: Sequence[Tuple[str, int, int]],
    ) -> Iterable[RelationPrediction]:
        keywords = [kw.lower() for kw in self.RELATION_KEYWORDS.get(relation_name, [])]
        results: List[RelationPrediction] = []
        for sentence_text, start, end in sentences:
            lower_sentence = sentence_text.lower()
            if keywords and not any(keyword in lower_sentence for keyword in keywords):
                continue
            sentence_entities = [
                entity
                for entity in entities_by_type.get(src_type, [])
                if start <= entity.start < end
            ]
            target_entities = [
                entity
                for entity in entities_by_type.get(tgt_type, [])
                if start <= entity.start < end
            ]
            if not sentence_entities or not target_entities:
                continue
            for source in sentence_entities:
                for target in target_entities:
                    if src_type == tgt_type and source.text == target.text:
                        continue
                    confidence = 0.55 + (0.15 if keywords else 0.0)
                    evidence = sentence_text.strip()
                    results.append(
                        RelationPrediction(
                            relation_type=relation_name,
                            source=source.text,
                            target=target.text,
                            evidence=evidence,
                            confidence=min(confidence, 0.95),
                            attributes={},
                        )
                    )
        return results

    def _match_attribute_relation(
        self,
        relation_name: str,
        entity_type: str,
        attribute_names: Sequence[str],
        entities_by_type: Dict[str, List[EntityPrediction]],
        sentences: Sequence[Tuple[str, int, int]],
    ) -> Iterable[RelationPrediction]:
        results: List[RelationPrediction] = []
        keywords = [
            keyword.lower()
            for attr in attribute_names
            for keyword in self._attribute_keywords(attr)
        ]
        for sentence_text, start, end in sentences:
            lower_sentence = sentence_text.lower()
            if keywords and not any(keyword in lower_sentence for keyword in keywords):
                continue
            scoped_entities = [
                entity
                for entity in entities_by_type.get(entity_type, [])
                if start <= entity.start < end
            ]
            if not scoped_entities:
                continue
            attributes: Dict[str, str] = {}
            for attribute in attribute_names:
                extracted = self._extract_attribute_value(attribute, sentence_text)
                if extracted:
                    attributes[attribute] = extracted
            confidence = 0.6 if attributes else 0.5
            target_value = self._format_attribute_target(attribute_names, attributes)
            for entity in scoped_entities:
                results.append(
                    RelationPrediction(
                        relation_type=relation_name,
                        source=entity.text,
                        target=target_value,
                        evidence=sentence_text.strip(),
                        confidence=confidence,
                        attributes=attributes,
                    )
                )
        return results

    def _attribute_keywords(self, attribute: str) -> Sequence[str]:
        if attribute in {"start_date", "end_date"}:
            return ["start", "date", "timeline", "end"]
        if attribute in {"industry", "sector"}:
            return ["industry", "sector"]
        if attribute == "budget":
            return ["budget", "funding"]
        return [attribute.replace("_", " ")]

    def _extract_attribute_value(self, attribute: str, text: str) -> str | None:
        if attribute in {"start_date", "end_date"}:
            match = self.DATE_PATTERN.search(text)
            return match.group() if match else None
        if attribute == "budget":
            match = self.MONEY_PATTERN.search(text)
            return match.group() if match else None
        if attribute in {"industry", "sector"}:
            match = re.search(
                r"(?:industry|sector)\s*(?:[:=]\s*)?(?P<value>[A-Za-z ]+)", text, re.IGNORECASE
            )
            return match.group("value").strip() if match else None
        return None

    def _format_attribute_target(
        self, attribute_names: Sequence[str], attributes: Dict[str, str]
    ) -> str:
        if attributes:
            parts = [f"{key}={value}" for key, value in attributes.items()]
            return "; ".join(parts)
        return ", ".join(attribute_names)

    def _dedupe_relations(
        self, predictions: Iterable[RelationPrediction]
    ) -> List[RelationPrediction]:
        unique: Dict[Tuple[str, str, str], RelationPrediction] = {}
        for relation in predictions:
            key = (relation.relation_type, relation.source, relation.target)
            existing = unique.get(key)
            if not existing or relation.confidence > existing.confidence:
                unique[key] = relation
        return list(unique.values())

    def _iter_sentences(self, text: str) -> Iterable[Tuple[str, int, int]]:
        for match in self.SENTENCE_PATTERN.finditer(text):
            yield match.group(), match.start(), match.end()
