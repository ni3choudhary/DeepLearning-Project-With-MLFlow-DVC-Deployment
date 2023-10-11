from DLProject.config.configuration import ConfigurationManager
from DLProject.components.model_training import Training
from DLProject import logger

class ModelTrainingPipeline:
    def __init__(self, stage_name = "Model Training"):
        self.stage_name = stage_name
        logger.info(f">>>>>> {self.stage_name} stage started <<<<<<")

    def main(self):
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training = Training(config=training_config)
        training.get_base_model()
        training.train_valid_generator()
        training.train()
        
        logger.info(f">>>>>> {self.stage_name} stage completed <<<<<< \n\n >>>>>>")


if __name__ == "__main__":
    try:
        model_trn_pipeline = ModelTrainingPipeline()
        model_trn_pipeline.main()
    except Exception as e:
        logger.exception(e)
        raise e