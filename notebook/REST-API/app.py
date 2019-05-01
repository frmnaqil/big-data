from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request
 
@main.route("/top/<int:count>/items", methods=["GET"])
def top_ratings(count):
    logger.debug("TOP %s item recommendation for each user requested", count)
    top_recommendation = recommendation_engine.items_for_user(count)
    return json.dumps(top_recommendation)

@main.route("/top/<int:count>/user", methods=["GET"])
def movie_ratings(count):
    logger.debug("TOP %s user recommendation for each movie", count)
    top_user = recommendation_engine.user_recommended_item(count)
    return json.dumps(top_user)


def create_app(spark_context, dataset_path):
    global recommendation_engine

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 
