from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session , select
from models import Student, Group
from database import get_session , engine
from  typing import List

router = APIRouter()

@router.post("/students/", response_model=Student , tags=["Students"])
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@router.post("/groups/", response_model=Group, tags=["Groups"])
def create_group(group: Group, session: Session = Depends(get_session)):
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

@router.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/groups/{group_id}", response_model=Group, tags=["Groups"])
def get_group(group_id: int, session: Session = Depends(get_session)):
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.delete("/students/{student_id}" , tags=["Students"])
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"detail": "Student deleted"}

@router.delete("/groups/{group_id}", tags=["Groups"])
def delete_group(group_id: int, session: Session = Depends(get_session)):
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    session.delete(group)
    session.commit()
    return {"detail": "Group deleted"}

@router.get("/students/", tags=["Students"])
def get_students():
    with Session(engine) as session:
        result = session.exec(select(Student)).all()
        return result

@router.get("/groups/", tags=["Groups"])
def get_groups():
    with Session(engine) as session:
        result = session.exec(select(Group)).all()
        return result

@router.post("/groups/{group_id}/students/", response_model=Group, tags=["Students"])
def add_student_to_group(group_id: int, student: Student, session: Session = Depends(get_session)):
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    student.group_id = group_id
    session.add(student)
    session.commit()
    session.refresh(group)
    return group

@router.delete("/groups/{group_id}/students/{student_id}", tags=["Students"])
def remove_student_from_group(group_id: int, student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student or student.group_id != group_id:
        raise HTTPException(status_code=404, detail="Student not found in this group")
    student.group_id = None
    session.commit()
    return {"detail": "Student removed from group"}

@router.get("/groups/{group_id}/students/", response_model=List[Student], tags=["Students"])
def get_students_in_group(group_id: int, session: Session = Depends(get_session)):
    return session.exec(Student.select().where(Student.group_id == group_id)).all()

@router.post("/students/{student_id}/transfer/{new_group_id}",tags=["Students"])
def transfer_student(student_id: int, new_group_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.group_id = new_group_id
    session.commit()
    return {"detail": "Student transferred"}
