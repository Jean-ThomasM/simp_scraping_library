import argparse
import logging
import sys

import config
from orchestrator import run_orchestrator


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/scraping.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Bouquineo Scraper")
    parser.add_argument(
        "--sample",
        type=int,
        help="Mode échantillon : limite le nombre de fiches à scraper.",
    )

    args = parser.parse_args()

    # Utilisation des arguments ou fallback sur le .env
    sample_size = args.sample
    if not sample_size and config.MODE == "test":
        sample_size = config.SAMPLE_SIZE

    try:
        run_orchestrator(sample_size=sample_size)
    except KeyboardInterrupt:
        logger.info(
            "Interruption volontaire par l'utilisateur. Le scraper s'arrête proprement."
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
