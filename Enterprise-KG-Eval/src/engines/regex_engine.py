"""Regex-based extraction engine implementation."""

import re
from typing import List, Dict, Any
import logging

from .base import BaseExtractionEngine

logger = logging.getLogger(__name__)


class RegexExtractionEngine(BaseExtractionEngine):
    """Regex-based entity and relation extraction."""

    def __init__(self):
        """Initialize regex extraction engine."""
        super().__init__("Regex")
        self.patterns = self._init_patterns()

    def _init_patterns(self) -> Dict[str, str]:
        """Initialize regex patterns for different entity and relation types."""
        return {
            # Entity patterns
            "Person": r"\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b",
            "Company": r"\b(OpenAI|Google|Microsoft|Apple|Amazon|Meta|Tesla|Netflix|Spotify|Uber|IBM|Oracle|Salesforce|Adobe|Intel|Cisco|HP|Dell|VMware|RedHat|Airbnb|Twitter|LinkedIn|Pinterest|Dropbox|Slack|Zoom|Shopify|Square|DocuSign)\b",
            "Project": r"Project\s+([A-Za-z0-9\-]+)",
            "Location": r"\b(Technology|Internet\s+Services|Software|Consumer\s+Electronics|E-commerce|Social\s+Media|Automotive|Clean\s+Energy|Entertainment|Streaming|Music|Audio\s+Technology|Transportation|Cloud|Enterprise|Database|CRM|Creative|Semiconductors|Networking|Computing|Printing|Hardware|Virtualization|Open\s+Source|Enterprise\s+Linux|Travel|Hospitality|Professional|Networking|Career|Visual\s+Discovery|Cloud\s+Storage|File\s+Sharing|Business|Communication|Collaboration|Video\s+Conferencing|Retail|Financial|Payment\s+Processing|Digital\s+Signature|Document\s+Management)\b",
            "Date": r"\b(\d{4}-\d{2}-\d{2})\b",
            "Age": r"age\s+(\d+)",
            "Position": r"as\s+an?\s+([A-Za-z\s]+?)(?:\.|,)",
            "Industry": r"(?:in|operates\s+in|specializes\s+in|focuses\s+on|works\s+in|known\s+for)\s+(?:the\s+)?([A-Za-z\s]+?)\s+(?:industry|sector)",
            "Department": r"(?:Department|department)\s+of\s+([A-Za-z\s]+)",
            "Technology": r"\b(Python|Java|SQL|AWS|Azure|Kubernetes|Docker|React|Angular|Node\.js|Django|Flask|TensorFlow|PyTorch)\b",
            "Product": r"Product\s+([A-Za-z0-9\-]+)",
            
            # Relation patterns
            "works_at": r"([A-Za-z\s]+)\s+(?:works|works at)\s+([A-Za-z0-9\s]+)",
            "manages": r"([A-Za-z\s]+)\s+manages?\s+([A-Za-z0-9\-,:\s]+)",
            "leads": r"([A-Za-z\s]+)\s+leads\s+([A-Za-z0-9\-,:\s]+)",
            "supervises": r"([A-Za-z\s]+)\s+supervises?\s+([A-Za-z0-9\-,:\s]+)",
            "project_period": r"Project\s+([A-Za-z0-9\-]+)\s+(?:started|began|launched|initiated)\s+on\s+(\d{4}-\d{2}-\d{2}),\s+(?:ends|concludes|finishes|completes)\s+on\s+(\d{4}-\d{2}-\d{2})",
            "company_industry": r"([A-Za-z0-9\s]+)\s+(?:operates in|specializes in|focuses on|works in|known for)\s+(?:the\s+)?([A-Za-z\s]+?)\s+industry",
        }

    def extract_entities(
        self,
        document: str,
        entity_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract entities using regex patterns.
        
        Args:
            document: Input text document
            entity_types: List of entity types to extract
            
        Returns:
            List of extracted entities
        """
        entities = []
        entity_id = 0

        for entity_type in entity_types:
            if entity_type not in self.patterns:
                logger.warning(f"No pattern found for entity type: {entity_type}")
                continue

            pattern = self.patterns[entity_type]
            try:
                for match in re.finditer(pattern, document, re.IGNORECASE):
                    entity_text = match.group(1) if match.groups() else match.group(0)
                    
                    entity = {
                        "id": f"e_{entity_id}",
                        "text": entity_text,
                        "type": entity_type,
                        "start": match.start(),
                        "end": match.end(),
                        "confidence": 0.85,  # Base regex confidence
                    }
                    
                    if self.validate_extraction(entity, "entity"):
                        entities.append(entity)
                        entity_id += 1
            except re.error as e:
                logger.error(f"Regex error for {entity_type}: {e}")

        logger.info(f"Extracted {len(entities)} entities from document")
        return entities

    def extract_relations(
        self,
        document: str,
        entities: List[Dict[str, Any]],
        relation_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract relations using regex patterns.
        
        Args:
            document: Input text document
            entities: Previously extracted entities
            relation_types: List of relation types to extract
            
        Returns:
            List of extracted relations
        """
        relations = []
        relation_id = 0

        for relation_type in relation_types:
            if relation_type not in self.patterns:
                logger.warning(f"No pattern found for relation type: {relation_type}")
                continue

            pattern = self.patterns[relation_type]
            try:
                for match in re.finditer(pattern, document, re.IGNORECASE):
                    groups = match.groups()
                    
                    if len(groups) >= 2:
                        head_text = groups[0].strip()
                        tail_text = groups[1].strip()
                        
                        # Try to match with extracted entities
                        head_entity = next(
                            (e for e in entities if head_text.lower() in e["text"].lower()),
                            None
                        )
                        tail_entity = next(
                            (e for e in entities if tail_text.lower() in e["text"].lower()),
                            None
                        )
                        
                        if head_entity and tail_entity:
                            relation = {
                                "id": f"r_{relation_id}",
                                "type": relation_type,
                                "head": head_entity["id"],
                                "head_text": head_entity["text"],
                                "tail": tail_entity["id"],
                                "tail_text": tail_entity["text"],
                                "confidence": 0.80,  # Base regex confidence
                            }
                            
                            if self.validate_extraction(relation, "relation"):
                                relations.append(relation)
                                relation_id += 1
            except re.error as e:
                logger.error(f"Regex error for {relation_type}: {e}")

        logger.info(f"Extracted {len(relations)} relations from document")
        return relations
