from DLProject.config.configuration import ConfigurationManager
from DLProject.components.prepare_base_model import PrepareBaseModel
from DLProject import logger


class PrepareBaseModelTrainingPipeline:
    def __init__(self, stage_name = "Prepare Base Model"):
        self.stage_name = stage_name
        logger.info(f">>>>>> {self.stage_name} stage started <<<<<<")

    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        prepare_base_model.get_base_model()
        prepare_base_model.update_base_model()
        logger.info(f">>>>>> {self.stage_name} stage completed <<<<<<")


if __name__ == "__main__":
    try:
        prep_model = PrepareBaseModelTrainingPipeline()
        prep_model.main()
    except Exception as e:
        logger.exception(e)
        raise e


