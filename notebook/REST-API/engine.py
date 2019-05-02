from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """A item recommendation engine
    """

    def __train_model(self):
        """Train the ALS model with the current dataset
        """
        logger.info("Training the ALS model...")

        # Train, Test
        (training, test) = self.ratings.randomSplit([0.7,0.3])

        # Build the recommendation model using ALS on the training data
        # Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics

        als = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="item_id", ratingCol="rating", coldStartStrategy="drop")

        self.model = als.fit(training)

        logger.info("ALS model built!")

    def items_for_user(self, numItems):

        userRecs = self.model.recommendForAllUsers(numItems)
        userRecs = userRecs.toPandas()
        userRecs = userRecs.to_json()

        return userRecs

    def user_recommended_item(self, numUsers):

        itemRecs = self.model.recommendForAllItems(numUsers)
        itemRecs = itemRecs.toPandas()
        itemRecs = itemRecs.to_json()
        
        return itemRecs

    def __init__(self, sc, dataset_path):
        """Init the recommendation engine given a Spark context and a dataset path
        """

        logger.info("Starting up the Recommendation Engine: ")

        self.sc = sc

        # Load dataset
        logger.info("Loading Ratings data...")
        lines = sc.read.text(dataset_path).rdd
        self.ratingsRDD = lines.map(lambda row: row.value.split(' '))\
                            .map(lambda p: Row(user_id=int(p[0]), item_id=int(p[1]), rating=float(p[2])))
        
        # Convert to DataFrame
        self.ratings = sc.createDataFrame(self.ratingsRDD)

        logger.info("Dataset loaded")

        # Start train
        self.__train_model()
