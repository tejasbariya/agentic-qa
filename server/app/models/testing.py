import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .base import Base

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("executions.id"))
    test_name = Column(String)
    file_path = Column(String)
    status = Column(String) # passed, failed, skipped
    duration_ms = Column(Integer)
    error_message = Column(String, nullable=True)

    execution = relationship("Execution", back_populates="test_results")
    failures = relationship("Failure", back_populates="test_result")

class Failure(Base):
    __tablename__ = "failures"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_result_id = Column(UUID(as_uuid=True), ForeignKey("test_results.id"))
    root_cause = Column(String)
    confidence_score = Column(Float)
    suggested_fix = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    test_result = relationship("TestResult", back_populates="failures")

class Coverage(Base):
    __tablename__ = "coverage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"))
    line_coverage = Column(Float)
    branch_coverage = Column(Float)
    function_coverage = Column(Float)
    report_data = Column(JSON) # Detailed file-by-file coverage
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"))
    format = Column(String) # HTML, PDF, JSON, MD
    file_url = Column(String)
    quality_score = Column(Float)
    risk_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
