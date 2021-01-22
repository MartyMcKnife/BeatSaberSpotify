def create_logger():
    import multiprocessing, logging

    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] - %(module)s / %(funcName)s %(process)d - : %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    handler = logging.FileHandler("beatsaberspotify.log")
    handler.setFormatter(formatter)

    # this bit will make sure you won't have
    # duplicated messages in the output
    if not len(logger.handlers):
        logger.addHandler(handler)
    return logger