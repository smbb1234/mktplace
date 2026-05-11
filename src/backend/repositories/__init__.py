"""Repository package for persistence layer.

Provides repository classes for sessions and leads.
"""

from .leads import LeadsRepository
from .sessions import SessionsRepository

__all__ = ["LeadsRepository", "SessionsRepository"]
"""Repository package for backend data access.

Add repository classes here to keep DB access encapsulated and testable.
"""

__all__ = [
    "LeadsRepository",
    "SessionsRepository",
]
