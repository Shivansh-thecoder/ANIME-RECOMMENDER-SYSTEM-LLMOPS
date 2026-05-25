from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException
from pathlib import Path

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting to build pipeline...")

        project_root = Path(__file__).resolve().parent.parent
        original_csv = str(project_root / "data" / "anime_with_synopsis.csv")
        processed_csv = str(project_root / "data" / "anime_updated.csv")

        loader = AnimeDataLoader(original_csv, processed_csv)
        processed_csv = loader.load_and_process()

        logger.info("Data  loaded and processed...")

        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_store_vectorstore()

        logger.info("Vector store Built sucesfully....")

        logger.info("Pipelien built sucesfuly....")
    except Exception as e:
            logger.error(f"Failed to execute pipeline {str(e)}")
            raise CustomException("Error during pipeline " , e)
    
if __name__=="__main__":
     main()
