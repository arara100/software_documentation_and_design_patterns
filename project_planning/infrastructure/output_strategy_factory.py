from business_logic.interfaces.i_output_strategy import IOutputStrategy
from infrastructure.config import Config


def create_output_strategy() -> IOutputStrategy:
    """
    Factory function that reads OUTPUT_STRATEGY from Config and returns
    the appropriate concrete strategy.

    Switching output destination requires only a change in the environment
    variable OUTPUT_STRATEGY (e.g. "console" → "kafka") — no source code
    modifications are needed.
    """
    strategy_name = Config.OUTPUT_STRATEGY.lower()

    if strategy_name == "kafka":
        from infrastructure.output_strategies.kafka_output_strategy import KafkaOutputStrategy

        return KafkaOutputStrategy(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            topic=Config.KAFKA_TOPIC,
        )

    # Default: console
    from infrastructure.output_strategies.console_output_strategy import ConsoleOutputStrategy

    return ConsoleOutputStrategy()
