import pickle


class TelemetryDecoder:
    @staticmethod
    def decode(telemetry):
        return pickle.loads(telemetry)

    @staticmethod
    def encode(telemetry):
        return pickle.dumps(telemetry)