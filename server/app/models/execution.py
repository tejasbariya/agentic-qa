import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from .base import Base

class ScanStatus(str, enum.Enum):
    PENDING = "PENDING"
    CLONING = "CLONING"
    ANALYZING = "ANALYZING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Scan(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"))
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING)
    detected_tech = Column(JSON, default={})
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    repository = relationship("Repository", back_populates="scans")
    executions = relationship("Execution", back_populates="scan")

class Execution(Base):
    __tablename__ = "executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"))
    test_type = Column(String) # unit, api, e2e, security
    status = Column(String) # running, passed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    scan = relationship("Scan", back_populates="executions")
    logs = relationship("Log", back_populates="execution")
    test_results = relationship("TestResult", back_populates="execution")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String) # e.g., Repository Analyzer
    description = Column(String)
    status = Column(String) # idle, busy, offline
    last_active = Column(DateTime, default=datetime.utcnow)

class Log(Base):
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("executions.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    message = Column(String)
    metadata_json = Column(JSON, default={})

    execution = relationship("Execution", back_populates="logs")
