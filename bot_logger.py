import logging


LOGGER = logging.basicConfig(
    filename="/home/isaevmik/airdropbot/airdropbotmain.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
