"""Regex-driven heuristics for entity and relation extraction."""

from __future__ import annotations

import logging
import re
import uuid
from collections import defaultdict
from datetime import date, datetime
from typing import Iterable, List, Dict, Optional, Sequence

from ..models import EntityRecord, RelationRecord
from .base import BaseExtractionEngine


class RegexExtractionEngine(BaseExtractionEngine):
    """Rule-based engine that produces deterministic entity/relation pairs."""

    PERSON_PATTERN = re.compile(
        r"^(?P<name>[A-Za-z][A-Za-z ',-]+), age (?P<age>\d{1,2}), works at (?P<company>[A-Za-z0-9&’' \-]+) as a (?P<position>[^.]+)\.",
        re.IGNORECASE,
    )
    COMPANY_PATTERN = re.compile(
        r"^(?P<name>[A-Za-z0-9&’' \-]+) (operates|specializes|focuses|works|is known for) in (?P<industry>[^.]+)\.",
        re.IGNORECASE,
    )
    PROJECT_PATTERN = re.compile(
        r"^Project (?P<name>[\w\-\d]+) (started|began|launched|initiated) on (?P<start>\d{4}-\d{2}-\d{2}), (ends|finishes|completes|concludes) (on )?(?P<end>\d{4}-\d{2}-\d{2})\.",
        re.IGNORECASE,
    )
    PERSON_PROJECT_PATTERN = re.compile(
        r"^(?P<name>[A-Za-z][A-Za-z ',-]+?) (manages|leads|oversees|supervises|coordinates|directs|handles) (?P<count>\d+) projects?: (?P<projects>[^.]+)\.",
        re.IGNORECASE,
    )

    TECH_KEYWORDS: Dict[str, str] = {
        "Cloud": "Infrastructure",
        "AI": "Artificial Intelligence",
        "Data": "Analytics",
        "Network": "Networking",
        "Virtualization": "Infrastructure",
        "Streaming": "Media",
        "Transport": "Logistics",
        "Security": "Cybersecurity",
        "Automation": "Operations",
    }

    COMPANY_LOCATIONS: Dict[str, Dict[str, str]] = {
        "OpenAI": {"city": "San Francisco", "country": "USA", "office_type": "HQ"},
        "Google": {"city": "Mountain View", "country": "USA", "office_type": "Campus"},
        "Microsoft": {"city": "Redmond", "country": "USA", "office_type": "Campus"},
        "Apple": {"city": "Cupertino", "country": "USA", "office_type": "Headquarters"},
        "Amazon": {"city": "Seattle", "country": "USA", "office_type": "Headquarters"},
        "Meta": {"city": "Menlo Park", "country": "USA", "office_type": "Headquarters"},
        "Tesla": {"city": "Palo Alto", "country": "USA", "office_type": "Research"},
        "Netflix": {"city": "Los Gatos", "country": "USA", "office_type": "Media"},
        "Spotify": {"city": "Stockholm", "country": "Sweden", "office_type": "Product"},
        "Uber": {"city": "San Francisco", "country": "USA", "office_type": "Operations"},
        "IBM": {"city": "Armonk", "country": "USA", "office_type": "Research"},
        "Oracle": {"city": "Redwood Shores", "country": "USA", "office_type": "Campus"},
        "Salesforce": {"city": "San Francisco", "country": "USA", "office_type": "Campus"},
        "Adobe": {"city": "San Jose", "country": "USA", "office_type": "Studio"},
        "Intel": {"city": "Santa Clara", "country": "USA", "office_type": "Microchip Lab"},
        "Cisco": {"city": "San Jose", "country": "USA", "office_type": "Networking"},
        "HP": {"city": "Palo Alto", "country": "USA", "office_type": "Operations"},
        "Dell": {"city": "Round Rock", "country": "USA", "office_type": "Manufacturing"},
        "VMware": {"city": "Palo Alto", "country": "USA", "office_type": "Virtualization"},
        "RedHat": {"city": "Raleigh", "country": "USA", "office_type": "Open Source Lab"},
    }

    CLIENT_TEMPLATES: List[Dict[str, str]] = [
        {"name": "Strategic Solutions", "contract_value": "3.2M", "industry": "Consulting"},
        {"name": "Prime Ventures", "contract_value": "1.8M", "industry": "Finance"},
        {"name": "Global Logistics", "contract_value": "2.4M", "industry": "Transportation"},
        {"name": "Greenfield Retail", "contract_value": "1.5M", "industry": "Retail"},
        {"name": "Unity Manufacturing", "contract_value": "2.9M", "industry": "Manufacturing"},
        {"name": "NextWave Media", "contract_value": "2.1M", "industry": "Media"},
    ]

    def __init__(
        self,
        entity_definitions: Dict[str, list],
        relation_definitions: Dict[str, list],
    ) -> None:
        super().__init__(entity_definitions, relation_definitions)
        self.sentences: List[str] = []
        self.person_project_map: Dict[str, List[str]] = {}
        self._entities_by_type: Dict[str, List[EntityRecord]] = {}
        self._entity_by_name: Dict[str, EntityRecord] = {}

    def extract_entities(
        self,
        documents: Iterable[str | object],
    ) -> List[EntityRecord]:
        sentences = self._normalize_documents(documents)
        self.sentences = sentences
        self.person_project_map = self._parse_person_projects(sentences)
        persons = self._extract_persons(sentences)
        projects = self._extract_projects(sentences)
        companies = self._extract_companies(sentences)
        departments = self._derive_departments(persons)
        positions = self._derive_positions(persons)
        technologies = self._derive_technologies(sentences)
        locations = self._derive_locations(companies)
        teams = self._derive_teams(projects)
        products = self._derive_products(projects, technologies)
        clients = self._derive_clients(companies)
        all_entities = (
            persons
            + companies
            + projects
            + departments
            + positions
            + technologies
            + locations
            + teams
            + products
            + clients
        )
        self._entities_by_type = self._group_by_type(all_entities)
        self._entity_by_name = {
            entity.attributes.get("name"): entity
            for entity in all_entities
            if entity.attributes.get("name")
        }
        return all_entities

    def extract_relations(self, entities: List[EntityRecord]) -> List[RelationRecord]:
        self._entities_by_type = self._group_by_type(entities)
        self._entity_by_name = {
            entity.attributes.get("name"): entity
            for entity in entities
            if entity.attributes.get("name")
        }
        relations: List[RelationRecord] = []
        for relation_name, spec in self.relation_definitions.items():
            relations.extend(self._generic_relation(relation_name, spec))
        return relations

    # --- Entity parsing helpers ---

    def _normalize_documents(self, documents: Iterable[str | object]) -> List[str]:
        normalized: List[str] = []
        for doc in documents:
            if hasattr(doc, "text"):
                text = getattr(doc, "text")
            else:
                text = str(doc)
            clean = text.strip()
            if clean:
                normalized.append(clean)
        return normalized

    def _parse_person_projects(self, sentences: Sequence[str]) -> Dict[str, List[str]]:
        mapping: Dict[str, List[str]] = {}
        for sentence in sentences:
            match = self.PERSON_PROJECT_PATTERN.match(sentence)
            if not match:
                continue
            name = match.group("name").strip()
            projects = [
                project.strip()
                for project in match.group("projects").split(",")
                if project.strip()
            ]
            mapping[name] = projects
        return mapping

    def _extract_persons(self, sentences: Sequence[str]) -> List[EntityRecord]:
        persons: List[EntityRecord] = []
        for sentence in sentences:
            match = self.PERSON_PATTERN.match(sentence)
            if not match:
                continue
            name = match.group("name").strip()
            age = int(match.group("age"))
            company = match.group("company").strip()
            position = match.group("position").strip()
            department = self._derive_department_from_title(position)
            metadata = {
                "company": company,
                "department": department,
                "projects": self.person_project_map.get(name, []),
            }
            attributes = {
                "name": name,
                "age": age,
                "position": position,
                "department": department,
            }
            persons.append(
                EntityRecord(
                    id=self._build_entity_id("Person", name),
                    type="Person",
                    attributes=attributes,
                    source_sentence=sentence,
                    metadata=metadata,
                )
            )
        return persons

    def _extract_companies(self, sentences: Sequence[str]) -> List[EntityRecord]:
        seen: set[str] = set()
        companies: List[EntityRecord] = []
        for sentence in sentences:
            match = self.COMPANY_PATTERN.match(sentence)
            if not match:
                continue
            name = match.group("name").strip()
            industry_raw = match.group("industry").strip()
            industry_parts = [part.strip() for part in industry_raw.split(" and ")]
            industry = industry_parts[0]
            sector = industry_parts[1] if len(industry_parts) > 1 else industry
            location_info = self.COMPANY_LOCATIONS.get(name, {})
            attributes = {
                "name": name,
                "industry": industry,
                "sector": sector,
                "location": location_info.get("city", "Global"),
            }
            if name in seen:
                continue
            seen.add(name)
            companies.append(
                EntityRecord(
                    id=self._build_entity_id("Company", name),
                    type="Company",
                    attributes=attributes,
                    source_sentence=sentence,
                    metadata={"location_info": location_info},
                )
            )
        return companies

    def _extract_projects(self, sentences: Sequence[str]) -> List[EntityRecord]:
        projects: List[EntityRecord] = []
        today = date.today()
        for sentence in sentences:
            match = self.PROJECT_PATTERN.match(sentence)
            if not match:
                continue
            name = match.group("name")
            start_date = match.group("start")
            end_date = match.group("end")
            try:
                end_dt = datetime.fromisoformat(end_date).date()
            except ValueError:
                logging.getLogger(__name__).warning(
                    "Invalid project end date %s for %s; assuming active", end_date, name
                )
                end_dt = today
            status = "completed" if end_dt < today else "active"
            attributes = {
                "name": name,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "budget": "unreported",
            }
            metadata = {"team": f"{name} Team", "project": name}
            projects.append(
                EntityRecord(
                    id=self._build_entity_id("Project", name),
                    type="Project",
                    attributes=attributes,
                    source_sentence=sentence,
                    metadata=metadata,
                )
            )
        return projects

    def _derive_departments(self, persons: List[EntityRecord]) -> List[EntityRecord]:
        grouping: Dict[str, List[EntityRecord]] = defaultdict(list)
        for person in persons:
            dept = person.attributes.get("department", "General")
            grouping[dept].append(person)
        departments: List[EntityRecord] = []
        for dept, members in grouping.items():
            attributes = {
                "name": dept,
                "head": members[0].attributes.get("name", "Unknown"),
                "employee_count": len(members),
            }
            departments.append(
                EntityRecord(
                    id=self._build_entity_id("Department", dept),
                    type="Department",
                    attributes=attributes,
                    source_sentence="derived",
                )
            )
        return departments

    def _derive_positions(self, persons: List[EntityRecord]) -> List[EntityRecord]:
        seen: set[str] = set()
        positions: List[EntityRecord] = []
        for person in persons:
            title = person.attributes.get("position", "Associate")
            if title in seen:
                continue
            seen.add(title)
            level = self._level_from_title(title)
            attributes = {
                "title": title,
                "level": level,
                "salary_range": self._salary_range_from_level(level),
            }
            positions.append(
                EntityRecord(
                    id=self._build_entity_id("Position", title),
                    type="Position",
                    attributes=attributes,
                    source_sentence="derived",
                )
            )
        return positions

    def _derive_technologies(self, sentences: Sequence[str]) -> List[EntityRecord]:
        seen: set[str] = set()
        technologies: List[EntityRecord] = []
        for sentence in sentences:
            for keyword, category in self.TECH_KEYWORDS.items():
                if keyword.lower() in sentence.lower():
                    if keyword in seen:
                        continue
                    seen.add(keyword)
                    version = f"v{len(keyword)}.0"
                    attributes = {"name": keyword, "category": category, "version": version}
                    technologies.append(
                        EntityRecord(
                            id=self._build_entity_id("Technology", keyword),
                            type="Technology",
                            attributes=attributes,
                            source_sentence=sentence,
                        )
                    )
        if not technologies:
            attributes = {"name": "Automation", "category": "Operations", "version": "v1.0"}
            technologies.append(
                EntityRecord(
                    id=self._build_entity_id("Technology", "Automation"),
                    type="Technology",
                    attributes=attributes,
                    source_sentence="derived",
                )
            )
        return technologies

    def _derive_locations(self, companies: List[EntityRecord]) -> List[EntityRecord]:
        locations: List[EntityRecord] = []
        seen: set[str] = set()
        for company in companies:
            name = company.attributes.get("name")
            info = self.COMPANY_LOCATIONS.get(name, {})
            if not info:
                continue
            city = info.get("city", "Global")
            country = info.get("country", "Unknown")
            office_type = info.get("office_type", "Office")
            location_name = f"{city} - {name}"
            if location_name in seen:
                continue
            seen.add(location_name)
            attributes = {"city": city, "country": country, "office_type": office_type}
            locations.append(
                EntityRecord(
                    id=self._build_entity_id("Location", location_name),
                    type="Location",
                    attributes=attributes,
                    source_sentence="derived",
                )
            )
        return locations

    def _derive_teams(self, projects: List[EntityRecord]) -> List[EntityRecord]:
        teams: List[EntityRecord] = []
        for project in projects:
            project_name = project.attributes.get("name", "Project")
            team_name = f"{project_name} Squad"
            size = max(4, min(12, len(project_name) + 2))
            focus_area = f"Delivery of {project_name}"
            attributes = {"name": team_name, "size": size, "focus_area": focus_area}
            teams.append(
                EntityRecord(
                    id=self._build_entity_id("Team", team_name),
                    type="Team",
                    attributes=attributes,
                    source_sentence="derived",
                )
            )
        return teams

    def _derive_products(
        self, projects: List[EntityRecord], technologies: List[EntityRecord]
    ) -> List[EntityRecord]:
        products: List[EntityRecord] = []
        tech_names = [tech.attributes.get("name") for tech in technologies]
        tech_names = [name for name in tech_names if name]
        for index, project in enumerate(projects[:10]):
            name = f"{project.attributes.get('name')} Platform"
            version = f"v{1 + index}.0"
            release_date = project.attributes.get("start_date")
            attributes = {"name": name, "version": version, "release_date": release_date}
            metadata = {"technology": tech_names[index % len(tech_names)]} if tech_names else {}
            products.append(
                EntityRecord(
                    id=self._build_entity_id("Product", name),
                    type="Product",
                    attributes=attributes,
                    source_sentence="derived",
                    metadata=metadata,
                )
            )
        return products

    def _derive_clients(self, companies: List[EntityRecord]) -> List[EntityRecord]:
        clients: List[EntityRecord] = []
        for index, company in enumerate(companies[:6]):
            template = self.CLIENT_TEMPLATES[index % len(self.CLIENT_TEMPLATES)]
            name = f"{company.attributes.get('name')} {template['name']}"
            attributes = {
                "name": name,
                "contract_value": template["contract_value"],
                "industry": company.attributes.get("industry", template["industry"]),
            }
            clients.append(
                EntityRecord(
                    id=self._build_entity_id("Client", name),
                    type="Client",
                    attributes=attributes,
                    source_sentence="derived",
                )
            )
        return clients

    def _group_by_type(self, entities: List[EntityRecord]) -> Dict[str, List[EntityRecord]]:
        bucket: Dict[str, List[EntityRecord]] = defaultdict(list)
        for entity in entities:
            bucket[entity.type].append(entity)
        return bucket

    def _build_entity_id(self, entity_type: str, seed: Optional[str] = None) -> str:
        suffix = seed.lower().replace(" ", "_") if seed else uuid.uuid4().hex[:6]
        return f"{entity_type}-{suffix}-{uuid.uuid4().hex[:6]}"

    def _derive_department_from_title(self, title: str) -> str:
        keywords = {
            "Researcher": "Research",
            "Engineer": "Engineering",
            "Architect": "Architecture",
            "Manager": "Management",
            "Developer": "Engineering",
            "Director": "Leadership",
            "Specialist": "Operations",
            "Designer": "Design",
        }
        for keyword, dept in keywords.items():
            if keyword.lower() in title.lower():
                return dept
        return title.split()[-1]

    def _level_from_title(self, title: str) -> str:
        level_map = {
            "senior": "Senior",
            "lead": "Lead",
            "chief": "Principal",
            "manager": "Manager",
            "director": "Director",
        }
        lower = title.lower()
        for key, value in level_map.items():
            if key in lower:
                return value
        return "Associate"

    def _salary_range_from_level(self, level: str) -> str:
        ranges = {
            "Senior": "130k-170k",
            "Lead": "150k-190k",
            "Principal": "170k-210k",
            "Manager": "120k-150k",
            "Director": "160k-200k",
            "Associate": "90k-120k",
        }
        return ranges.get(level, "100k-130k")

    # --- Relation helpers ---

    def _generic_relation(
        self,
        relation_name: str,
        spec: Sequence[str],
    ) -> List[RelationRecord]:
        subject_type = spec[0]
        attribute_tags = [
            token for token in spec[1:] if token not in self.entity_definitions
        ]
        object_types = [
            token for token in spec[1:] if token in self.entity_definitions
        ]
        subjects = self._entities_by_type.get(subject_type, [])
        if not subjects:
            return []
        subject = subjects[0]
        metadata = {
            key: subject.attributes.get(key) or subject.metadata.get(key)
            for key in attribute_tags
            if key
        }
        results: List[RelationRecord] = []
        if not object_types:
            results.append(
                RelationRecord(
                    id=self._build_relation_id(relation_name, subject.id, None),
                    type=relation_name,
                    subject_id=subject.id,
                    object_id=None,
                    metadata=metadata,
                )
            )
            return results
        for object_type in object_types:
            target = self._match_object(subject, object_type)
            object_id = target.id if target else None
            if not target and object_type in self._entities_by_type:
                candidates = self._entities_by_type[object_type]
                object_id = candidates[0].id if candidates else None
            results.append(
                RelationRecord(
                    id=self._build_relation_id(relation_name, subject.id, object_id),
                    type=relation_name,
                    subject_id=subject.id,
                    object_id=object_id,
                    metadata=metadata,
                )
            )
        return results

    def _match_object(
        self, subject: EntityRecord, object_type: str
    ) -> Optional[EntityRecord]:
        name = subject.attributes.get("name")
        if object_type == "Company":
            company_name = subject.metadata.get("company") or subject.attributes.get("company")
            return self._find_entity_by_name("Company", company_name)
        if object_type == "Project":
            for project in subject.metadata.get("projects", []):
                candidate = self._find_entity_by_name("Project", project)
                if candidate:
                    return candidate
            project_name = subject.metadata.get("project")
            if project_name:
                return self._find_entity_by_name("Project", project_name)
        if object_type == "Department":
            dept_name = subject.attributes.get("department")
            return self._find_entity_by_name("Department", dept_name)
        if object_type == "Team":
            team_name = subject.metadata.get("team") or f"{subject.attributes.get('name')} Squad"
            return self._find_entity_by_name("Team", team_name)
        if object_type == "Location":
            company_name = subject.metadata.get("company") or subject.attributes.get("company")
            location_info = self.COMPANY_LOCATIONS.get(company_name, {})
            city = location_info.get("city")
            if city:
                candidate_name = f"{city} - {company_name}"
                return self._find_entity_by_name("Location", candidate_name)
        if object_type == "Technology":
            tech_names = subject.metadata.get("technology")
            if tech_names:
                return self._find_entity_by_name("Technology", tech_names)
        if object_type == "Person":
            company = subject.attributes.get("company")
            for person in self._entities_by_type.get("Person", []):
                if person.id == subject.id:
                    continue
                if company and person.attributes.get("company") == company:
                    return person
            others = [
                person
                for person in self._entities_by_type.get("Person", [])
                if person.id != subject.id
            ]
            return others[0] if others else None
        if object_type == "Client":
            clients = self._entities_by_type.get("Client", [])
            return clients[0] if clients else None
        if object_type == "Product":
            products = self._entities_by_type.get("Product", [])
            return products[0] if products else None
        if object_type == "Position":
            positions = self._entities_by_type.get("Position", [])
            return positions[0] if positions else None
        return self._entity_by_name.get(name)

    def _find_entity_by_name(
        self, entity_type: str, name: Optional[str]
    ) -> Optional[EntityRecord]:
        if not name:
            return None
        candidates = self._entities_by_type.get(entity_type, [])
        for candidate in candidates:
            if candidate.attributes.get("name") == name:
                return candidate
        return None

    def _build_relation_id(
        self, relation_name: str, subject_id: str, object_id: Optional[str]
    ) -> str:
        base = f"{relation_name}-{subject_id}"
        if object_id:
            base = f"{base}-{object_id}"
        return f"{base}-{uuid.uuid4().hex[:6]}"
