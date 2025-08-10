"""
Database Manager Wrapper

This is a wrapper for the DatabaseManager to maintain compatibility
with the enhanced endpoints that expect utils.database_manager.
"""

# Import the actual DatabaseManager from utils.database
from utils.database import DatabaseManager

# Re-export for compatibility
__all__ = ['DatabaseManager']
