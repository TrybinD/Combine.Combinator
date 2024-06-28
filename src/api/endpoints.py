from pathlib import Path
import requests

from fastapi import APIRouter, BackgroundTasks

from service.recommendation_service import UserTeamRecommendationService
from models.vectorizers import NavecVectorizor
from models.combinators.xgboost_combinator import XGBoostCombinator

from data.repositories import UserInSearchRepository, TeamRepository, UserTeamRecommendationsRepository
import config

router = APIRouter()

vectorizor = NavecVectorizor(Path("models/navec_news_v1_1B_250K_300d_100q.tar"))
combinator = XGBoostCombinator(model_path=Path("model/xgb_combinator.pkl"), 
                               preprocessor_path=Path("model/preprocessor_v14.pkl"),
                               threshold=0.85)

recommendation_service = UserTeamRecommendationService(users_vectorizer=vectorizor, 
                                                       teams_vectorizer=vectorizor,
                                                       combinator=combinator)

def start_search_process_to_team(team_id):

    team = TeamRepository().get(id=team_id, is_active=True)[0]

    users = UserInSearchRepository().get(event_id=team.event_id, is_active=True)

    users_descriptions = {user.user_id: user.description for user in users}
    users_in_search_id_mapping = {user.user_id: user.id for user in users}

    teams_descriptions = {team.id: {"name": team.name, "description": team.description}}

    recommendations = recommendation_service.get_recommendations(users_descriptions,
                                                                 teams_descriptions)
    
    for reco in recommendations:
        UserTeamRecommendationsRepository().add(data={"team_id": reco["team_id"],
                                                      "user_in_search_id": users_in_search_id_mapping[reco["user_id"]]})
        
        requests.post(config.BOT_URL + "/message/send/", json={"message": "Мы нашли тебе новые варианты команды, посмотри скорее",
                                                               "user_id": reco["user_id"]})

    if recommendations:
        requests.post(config.BOT_URL + "/message/send/", json={"message": "Мы нашли тебе новых людей в команду, посмотри скорее",
                                                               "user_id": team.creator_id})


def start_search_process_to_user(user_in_search_id):

    user = UserInSearchRepository().get(id=user_in_search_id, is_active=True)[0]

    teams = TeamRepository().get(event_id=user.event_id, is_active=True)

    users_descriptions = {user.user_id: user.description}

    teams_descriptions = {team.id: {"name": team.name, "description": team.description} for team in teams}

    teams_creator_mapping = {team.id: team.creator_id for team in teams}

    recommendations = recommendation_service.get_recommendations(users_descriptions,
                                                                 teams_descriptions)
    
    for reco in recommendations:
        UserTeamRecommendationsRepository().add(data={"team_id": reco["team_id"],
                                                      "user_in_search_id": user.id})
        
        requests.post(config.BOT_URL + "/message/send/", json={"message": "Мы нашли тебе новых людей в команду, посмотри скорее!",
                                                               "user_id": teams_creator_mapping[reco["team_id"]]})
        
    if recommendations:
        requests.post(config.BOT_URL + "/message/send/", json={"message": "Мы нашли тебе новые варианты команды, посмотри скорее!",
                                                            "user_id": user.user_id})

@router.post("/recommendations-to-team/")
def get_recos_from_json(team_id: int, background_tasks: BackgroundTasks) -> str:

    background_tasks.add_task(start_search_process_to_team, team_id)
    
    return "start_searching"


@router.post("/recommendations-to-user/")
def get_recos_from_json(user_in_search_id: int, background_tasks: BackgroundTasks) -> str:

    background_tasks.add_task(start_search_process_to_user, user_in_search_id)
    
    return "start_searching"

