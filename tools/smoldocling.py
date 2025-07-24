# tools/smoldocling.py

from langchain_core.tools import tool
from tools.smoldocling_tool import call_smoldocling
from utils.logger import logger
from typing import Dict, Any


@tool
def smoldocling_tool(file_path: str) -> Dict[str, Any]:
    """Extract structured information from PDF using SmolDocling.
    
    Args:
        file_path: Path to the PDF file to process
        
    Returns:
        Dictionary containing extracted structured information
    """
    logger.info("🪶 Running SmolDocling Tool for file: %s", file_path)

    try:
        smol_result = call_smoldocling(file_path)
        logger.info("✅ SmolDocling extraction complete.")
        return {
            "success": True,
            "data": smol_result,
            "message": "SmolDocling extraction completed successfully"
        }
    except Exception as e:
        logger.error("SmolDocling error: %s", e)
        return {
            "success": False,
            "data": {},
            "message": f"SmolDocling extraction failed: {str(e)}"
        }
