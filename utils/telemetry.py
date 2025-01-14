import pickle
import random

from utils.telemetry_decoder import TelemetryDecoder


class TelemetryUtil:

    @staticmethod
    def get_telemetry():
        telemetry = {
            "takim_numarasi":1,
            "iha_enlem": random.randint(0, 9999)%10,
            "iha_boylam": random.randint(0, 9999)%10,
            "iha_irtifa": random.randint(0, 9999)%10,
            "iha_dikilme": random.randint(0, 100)%10,
            "iha_yonelme": random.randint(0, 100),
            "iha_yatis": random.randint(0, 100),
            "iha_hiz": random.randint(0, 100),
            "iha_batarya": random.randint(0, 100),
            "iha_otonom": random.randint(0, 1),
            "iha_kilitlenme": random.randint(0, 1),
            "hedef_merkez_X": random.randint(0, 100),
            "hedef_merkez_Y": random.randint(0, 100),
            "hedef_genislik": random.randint(0, 100),
            "hedef_yukseklik": random.randint(0, 100),
            "gps_saati":{
                "saat": random.randint(0, 24),
                "dakika": random.randint(0, 60),
                "saniye": random.randint(0, 60),
                "milisaniye": random.randint(0, 1000)
            }
        }
        return TelemetryDecoder.encode(telemetry)