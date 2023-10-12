from DLProject.config.configuration import ConfigurationManager
from DLProject.components.model_evaluation import Evaluation
from DLProject import logger

class EvaluationPipeline:
    def __init__(self, stage_name = "Model Evaluation using MLFlow"):
        self.stage_name = stage_name
        logger.info(f">>>>>> {self.stage_name} stage started <<<<<<")

    def main(self):
        config = ConfigurationManager()
        evaluation_config = config.get_evaluation_config()
        evaluation = Evaluation(evaluation_config)
        evaluation.evaluation()
        evaluation.log_into_mlflow()
        
        logger.info(f">>>>>> {self.stage_name} stage completed <<<<<< \n\n >>>>>>")


if __name__ == "__main__":
    try:
        evaluation_pipeline = EvaluationPipeline()
        evaluation_pipeline.main()
    except Exception as e:
        logger.exception(e)
        raise e