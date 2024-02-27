from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, File

from .schemas import Responce, Request
from service.excel_parse_service import ExcelParseService
from service.recommendation_service import RecommendationService
from models.vectorizers import RandomVectorizor
from models.combinators import RandomCombinator
from data.repo.projects_repo import ProjectsRepo

router = APIRouter(prefix="/api/text-reco")

project_repo = ProjectsRepo(Path("data/project_ideas"))

recommendation_service = RecommendationService(vectorizer=RandomVectorizor(n_dims=128), 
                                               combinator=RandomCombinator(project_repo))

@router.post("/from-json/")
def get_recos_from_json(request: Request) -> Responce:
    
    users_recos, projects = recommendation_service.get_recommendations(request.users,
                                                                       k_recs=request.k_recs, 
                                                                       n_users_in_project=request.n_users_in_project)
    
    responce = Responce(users=users_recos, projects=projects)

    return responce


@router.post("/from-xlsx/{k_recs}/{n_users_in_project}")
def get_recos_from_xlsx(file: Annotated[bytes, File()], k_recs: int, n_users_in_project: int) -> Responce:

    json_request = ExcelParseService.parse_excel(file)
    
    users_recos, projects = recommendation_service.get_recommendations(json_request, 
                                                                       k_recs=k_recs, 
                                                                       n_users_in_project=n_users_in_project)
    
    responce = Responce(users=users_recos, projects=projects)

    return responce
