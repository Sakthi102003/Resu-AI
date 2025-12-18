"""Template Routes - Template listing and information"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List, Dict
from routes.auth import get_current_user
from templates.template_manager import TemplateManager
from io import BytesIO

router = APIRouter(prefix="/templates", tags=["Templates"])


@router.get("/", response_model=List[Dict])
async def list_templates():
    """List all available resume templates"""
    return TemplateManager.list_templates()


@router.get("/{template_id}")
async def get_template_info(template_id: str):
    """Get information about a specific template"""
    try:
        return TemplateManager.get_template_info(template_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template not found: {template_id}"
        )


@router.post("/{template_id}/preview")
async def preview_template(
    template_id: str,
    resume_data: dict,
    theme_color: str = "#3B82F6",
    current_user: dict = Depends(get_current_user)
):
    """Preview a resume with a specific template"""
    try:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Preview request for template: {template_id}")
        logger.info(f"Resume data keys: {resume_data.keys() if resume_data else 'None'}")
        logger.info(f"Theme color: {theme_color}")
        
        pdf_buffer = TemplateManager.generate_resume(
            resume_data=resume_data,
            template_name=template_id,
            theme_color=theme_color
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=preview_{template_id}.pdf"
            }
        )
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating template preview: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating template preview: {str(e)}"
        )
