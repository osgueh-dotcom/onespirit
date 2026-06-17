from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.modules.auth.models import User
from app.modules.projects import service, schemas
from app.modules.projects.models import ProjectActivityLog

router = APIRouter(tags=["Project Workflow Module"])

PNL_ACCESS_ROLES = {"Super Admin", "Admin", "Management", "Finance"}
CANCEL_APPROVER_ROLES = {"Super Admin", "Admin", "Management", "Director"}
PROGRAM_STATUS_OPERATOR_ROLES = {"Super Admin", "Admin", "Management", "Director", "Staff", "PM"}

@router.get("/projects", response_model=List[schemas.ProjectResponse])
def get_all_projects(
    db: Session = Depends(deps.get_db),
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    po_id: Optional[UUID] = None,
    pm_id: Optional[UUID] = None,
    source_id: Optional[UUID] = None,
    quotation_status: Optional[str] = None,
    program_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    project_status: Optional[str] = None,
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Retrieve the list of active projects, optionally filtered by various attributes"""
    projects = service.get_projects(
        db, 
        status=status, 
        skip=skip, 
        limit=limit,
        po_id=po_id,
        pm_id=pm_id,
        source_id=source_id,
        quotation_status=quotation_status,
        program_status=program_status,
        payment_status=payment_status,
        project_status=project_status
    )
    
    response_list = []
    for p in projects:
        p_res = schemas.ProjectResponse.model_validate(p)
        readiness = service.calculate_project_readiness(p)
        p_res.project_readiness_score = readiness["project_readiness_score"]
        p_res.instrument_completion_rate = readiness["instrument_completion_rate"]
        response_list.append(p_res)
        
    return response_list

@router.get("/projects/{project_id}", response_model=schemas.ProjectDetailResponse)
def get_project_by_id(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Get project details by ID"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    project.validation_warnings = service.check_project_validation_warnings(project)
    project.instruments = [inst for inst in project.instruments if not inst.deleted_at]
    
    # Manually serialize to Pydantic to avoid dynamic attribute session commit side effects
    response_data = schemas.ProjectDetailResponse.model_validate(project)
    
    # Calculate readiness score and counts
    readiness = service.calculate_project_readiness(project)
    response_data.required_instruments_count = readiness["required_instruments_count"]
    response_data.completed_required_instruments_count = readiness["completed_required_instruments_count"]
    response_data.instrument_completion_rate = readiness["instrument_completion_rate"]
    response_data.missing_required_instruments_count = readiness["missing_required_instruments_count"]
    response_data.revision_required_count = readiness["revision_required_count"]
    response_data.overdue_instruments_count = readiness["overdue_instruments_count"]
    response_data.project_readiness_score = readiness["project_readiness_score"]
    
    # Mask PNL document link if unauthorized
    user_role = current_user.role.name if current_user and current_user.role else None
    if user_role not in PNL_ACCESS_ROLES:
        for inst in response_data.instruments:
            if inst.instrument_type == "PNL":
                inst.document_url = None
                
    return response_data

@router.post("/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_entry(
    project_in: schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Initialize a brand new event project"""
    return service.create_project(db, project_in=project_in, created_by_id=str(current_user.id))

@router.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project_entry(
    project_id: str,
    project_in: schemas.ProjectUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Update detailed attributes of an event project"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.update_project(db, db_project=project, project_in=project_in, changed_by_id=str(current_user.id))

@router.post("/projects/{project_id}/transition", response_model=schemas.ProjectResponse)
def transition_project_workflow(
    project_id: str,
    new_status: str,
    notes: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Transition a project's operational status and record transition history with strict approval gates"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Map input status to the new Program Status taxonomy case-insensitively
    valid_statuses_map = {
        "inquiry": "Inquiry", "confirmed": "Confirmed", "preparation": "Preparation",
        "ready": "Ready", "running": "Running", "completed": "Completed",
        "reporting": "Reporting", "closed": "Closed", "cancel": "Cancel",
        "canceled": "Cancel", "negotiation": "Inquiry"
    }
    normalized_status = valid_statuses_map.get(new_status.lower(), new_status)
    
    valid_statuses = ["Inquiry", "Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed", "Cancel"]
    if normalized_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status selection. Must be one of {valid_statuses}"
        )
        
    # Standardized business approval role matrix check
    user_role = current_user.role.name
    
    # 1. Cancel status requires administrative or management scope
    if normalized_status == "Cancel" and user_role not in CANCEL_APPROVER_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Directors, Management, or Administrators can cancel active event projects."
        )

    # 2. Confirmed or Completed status requires PM, Staff, Management, or Admin scope
    is_pm_assigned = project.program_manager_id == current_user.id
    if normalized_status in ["Confirmed", "Completed"] and not (is_pm_assigned or user_role in PROGRAM_STATUS_OPERATOR_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Management, Staff, the assigned Program Manager, or Administrators can confirm or complete active event projects."
        )

    # 3. Completed status requires all associated operations checklist tasks to be finished (done)
    if normalized_status == "Completed":
        from app.modules.tasks.models import Task
        uncompleted_tasks_count = db.query(Task).filter(
            Task.project_id == project.id,
            Task.status != "done",
            Task.deleted_at == None
        ).count()
        
        if uncompleted_tasks_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition to 'Completed' status. There are {uncompleted_tasks_count} uncompleted operational checklist tasks remaining."
            )
        
    return service.transition_project_status(
        db, 
        db_project=project, 
        new_status=normalized_status, 
        notes=notes, 
        changed_by_id=str(current_user.id)
    )

@router.get("/projects/{project_id}/logs", response_model=List[schemas.ProjectStatusLogResponse])
def get_project_status_logs(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Fetch status logs and audit trails of project state shifts"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.get_project_logs(db, project_id=project_id)

@router.patch("/projects/{project_id}/status", response_model=schemas.ProjectResponse)
def patch_project_status(
    project_id: str,
    payload: schemas.ProjectStatusUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Generic status update endpoint to shift quotation, program, payment, or project status"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    # Gate validation for generic endpoint
    user_role = current_user.role.name
    if payload.status_type == "program_status":
        valid_statuses = ["Inquiry", "Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed", "Cancel"]
        if payload.new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid program status selection. Must be one of {valid_statuses}"
            )
        if payload.new_status == "Cancel" and user_role not in CANCEL_APPROVER_ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Directors, Management, or Administrators can cancel active event projects."
            )
        is_pm_assigned = project.program_manager_id == current_user.id
        if payload.new_status in ["Confirmed", "Completed"] and not (is_pm_assigned or user_role in PROGRAM_STATUS_OPERATOR_ROLES):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Management, Staff, the assigned Program Manager, or Administrators can confirm or complete active event projects."
            )

    # Sprint 8: Perform operational readiness gate check
    gate = service.evaluate_project_readiness_gate(project, payload.status_type, payload.new_status)
    old_status_val = getattr(project, payload.status_type)
    
    if gate["severity"] == "critical" and not payload.force:
        # Log blocked attempt
        db.add(ProjectActivityLog(
            project_id=project.id,
            user_id=current_user.id,
            action="status_change_blocked",
            field_name=payload.status_type,
            old_value=old_status_val,
            new_value=payload.new_status,
            notes=f"Blocked status change to '{payload.new_status}' due to critical blockers: {', '.join(gate['blockers'])}"
        ))
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Status update blocked by critical readiness issues.",
                "severity": "critical",
                "blockers": gate["blockers"],
                "warnings": gate["warnings"],
                "recommendations": gate["recommendations"],
                "can_override": gate["can_override"]
            }
        )
    
    # Log forced or warning state transition outcomes
    if gate["severity"] == "critical" and payload.force:
        db.add(ProjectActivityLog(
            project_id=project.id,
            user_id=current_user.id,
            action="status_force_updated",
            field_name=payload.status_type,
            old_value=old_status_val,
            new_value=payload.new_status,
            notes=f"Forced status update to '{payload.new_status}'. Overrode critical blockers: {', '.join(gate['blockers'])}"
        ))
    elif gate["warnings"]:
        db.add(ProjectActivityLog(
            project_id=project.id,
            user_id=current_user.id,
            action="status_changed_with_readiness_warning",
            field_name=payload.status_type,
            old_value=old_status_val,
            new_value=payload.new_status,
            notes=f"Status changed to '{payload.new_status}' with warnings: {', '.join(gate['warnings'])}"
        ))

    try:
        updated_project = service.update_project_status_generic(
            db,
            db_project=project,
            status_type=payload.status_type,
            new_status=payload.new_status,
            notes=payload.notes,
            changed_by_id=str(current_user.id)
        )
        return updated_project
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/projects/{project_id}/readiness/check", response_model=schemas.ProjectReadinessCheckResponse)
def check_project_readiness_gate(
    project_id: str,
    payload: schemas.ProjectReadinessCheckRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Preview project readiness state before making a status transition"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    gate = service.evaluate_project_readiness_gate(project, payload.status_type, payload.target_status)
    
    # Log readiness check action in ProjectActivityLog
    db.add(ProjectActivityLog(
        project_id=project.id,
        user_id=current_user.id,
        action="readiness_check",
        notes=f"Readiness check performed for target status '{payload.target_status}' ({payload.status_type}). Score: {gate['readiness_score']:.1f}%"
    ))
    db.commit()
    
    return {
        "project_id": project.id,
        "status_type": payload.status_type,
        "target_status": payload.target_status,
        "allowed": gate["allowed"],
        "severity": gate["severity"],
        "can_override": gate["can_override"],
        "readiness_score": gate["readiness_score"],
        "instrument_completion_rate": gate["instrument_completion_rate"],
        "warnings": gate["warnings"],
        "blockers": gate["blockers"],
        "recommendations": gate["recommendations"]
    }


@router.delete("/projects/{project_id}", status_code=status.HTTP_200_OK)
def delete_project_entry(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Remove a project from active logs (Soft delete)"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    service.delete_project(db, db_project=project)
    return {"message": "Project successfully archived."}

@router.get("/projects/{project_id}/instruments", response_model=List[schemas.ProjectInstrumentRead])
def get_instruments_for_project(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """List operational instruments for a project"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    instruments = service.get_project_instruments(db, project_id=project_id)
    response_list = [schemas.ProjectInstrumentRead.model_validate(inst) for inst in instruments]
    
    # Mask PNL document link if unauthorized
    user_role = current_user.role.name if current_user and current_user.role else None
    if user_role not in PNL_ACCESS_ROLES:
        for inst in response_list:
            if inst.instrument_type == "PNL":
                inst.document_url = None
                
    return response_list

@router.post("/projects/{project_id}/instruments", response_model=schemas.ProjectInstrumentRead, status_code=status.HTTP_201_CREATED)
def create_instrument_for_project(
    project_id: str,
    payload: schemas.ProjectInstrumentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Create a new custom operational instrument for a project"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Validate payload.instrument_type and status choices
    valid_types = ["CL", "ROS", "CK", "PNL", "PF", "MATRIX", "OTHER"]
    if payload.instrument_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid instrument type. Must be one of {valid_types}"
        )
        
    valid_statuses = ["Not Required", "Not Started", "In Progress", "Done", "Need Revision"]
    if payload.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )

    try:
        inst = service.create_project_instrument(
            db,
            project_id=project_id,
            instrument_in=payload,
            user_id=str(current_user.id)
        )
        response_data = schemas.ProjectInstrumentRead.model_validate(inst)
        
        # Mask PNL document link if unauthorized
        user_role = current_user.role.name if current_user and current_user.role else None
        if user_role not in PNL_ACCESS_ROLES:
            if response_data.instrument_type == "PNL":
                response_data.document_url = None
                
        return response_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/projects/{project_id}/instruments/{instrument_id}", response_model=schemas.ProjectInstrumentRead)
def update_instrument_in_project(
    project_id: str,
    instrument_id: str,
    payload: schemas.ProjectInstrumentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Update status, notes, or URL link of an operational instrument"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    if payload.status is not None:
        valid_statuses = ["Not Required", "Not Started", "In Progress", "Done", "Need Revision"]
        if payload.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of {valid_statuses}"
            )

    try:
        inst = service.update_project_instrument(
            db,
            instrument_id=instrument_id,
            instrument_in=payload,
            user_id=str(current_user.id)
        )
        response_data = schemas.ProjectInstrumentRead.model_validate(inst)
        
        # Mask PNL document link if unauthorized
        user_role = current_user.role.name if current_user and current_user.role else None
        if user_role not in PNL_ACCESS_ROLES:
            if response_data.instrument_type == "PNL":
                response_data.document_url = None
                
        return response_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/projects/{project_id}/instruments/{instrument_id}", status_code=status.HTTP_200_OK)
def delete_instrument_from_project(
    project_id: str,
    instrument_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Remove an operational instrument from a project"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    success = service.delete_project_instrument(db, instrument_id=instrument_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrument not found or already deleted"
        )
    return {"message": "Instrument successfully deleted."}

@router.post("/projects/{project_id}/instruments/defaults", response_model=List[schemas.ProjectInstrumentRead], status_code=status.HTTP_200_OK)
def generate_default_instruments_for_project(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Auto-generate default operational instruments (CL, ROS, CK, PNL) for a project if they don't exist"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    service.ensure_default_project_instruments(db, project_id=project.id)
    instruments = service.get_project_instruments(db, project_id=project_id)
    response_list = [schemas.ProjectInstrumentRead.model_validate(inst) for inst in instruments]
    
    # Mask PNL document link if unauthorized
    user_role = current_user.role.name if current_user and current_user.role else None
    if user_role not in PNL_ACCESS_ROLES:
        for inst in response_list:
            if inst.instrument_type == "PNL":
                inst.document_url = None
                
    return response_list
