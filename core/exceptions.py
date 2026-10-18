"""
core/exceptions.py - Domain Exception Hierarchy for Clinical Triage Engine
"""

class TriagePipelineException(Exception):
    """Base exception for all clinical triage engine operations."""
    def __init__(self, message: str, error_code: str = "TRIAGE_PIPELINE_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

class ImageDecodingError(TriagePipelineException):
    """Raised when an incoming base64 payload cannot be parsed into an OpenCV matrix."""
    def __init__(self, message: str = "Corrupted or unsupported image binary format."):
        super().__init__(message, error_code="IMAGE_DECODING_FAILURE")

class OpticalProcessingError(TriagePipelineException):
    """Raised when HSV segmentation, Canny edge detection, or contour extraction fails."""
    def __init__(self, message: str = "Optical feature extraction algorithm encountered a critical error."):
        super().__init__(message, error_code="OPTICAL_PROCESSING_FAILURE")

class ProviderAPIError(TriagePipelineException):
    """Raised when an upstream multimodal vision API returns non-200 or invalid schema."""
    def __init__(self, provider: str, status_code: int, raw_error: str):
        super().__init__(
            f"Provider '{provider}' rejected inference request with status {status_code}.",
            error_code=f"{provider.upper()}_API_ERROR",
            details={"provider": provider, "status_code": status_code, "raw_error": raw_error}
        )

class SpecialistNotFoundException(TriagePipelineException):
    """Raised when no qualified on-call medical specialist satisfies the clinical criteria."""
    def __init__(self, specialty: str):
        super().__init__(
            f"No medical specialist currently on-call for department: '{specialty}'.",
            error_code="SPECIALIST_NOT_FOUND",
            details={"requested_specialty": specialty}
        )

class DatabaseIntegrityError(TriagePipelineException):
    """Raised when an SQLite transaction violates constraints or fails commit."""
    def __init__(self, operation: str, error: str):
        super().__init__(
            f"Database integrity fault during operation '{operation}': {error}",
            error_code="DATABASE_TRANSACTION_FAULT",
            details={"operation": operation, "error": error}
        )
