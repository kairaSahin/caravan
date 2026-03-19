import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_error_logging() -> logging.Logger:
	log_dir = Path(__file__).resolve().parents[3] / "logs"
	log_dir.mkdir(parents=True, exist_ok=True)
	log_file = log_dir / "api-errors.log"

	logger = logging.getLogger("caravan.api")
	logger.setLevel(logging.INFO)

	if not any(
			isinstance(handler, RotatingFileHandler) and Path(handler.baseFilename) == log_file
			for handler in logger.handlers
	):
		handler = RotatingFileHandler(
			filename=log_file,
			maxBytes=1_000_000,
			backupCount=5,
			encoding="utf-8",
		)
		handler.setLevel(logging.ERROR)
		handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
		logger.addHandler(handler)

	return logger
