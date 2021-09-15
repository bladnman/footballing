def weather_pieces(weather_parts):
    temp_bit = None
    wind_bit = None
    humid_bit = None

    def to_int(in_str):
        numeric_filter = filter(str.isdigit, in_str)
        return int("".join(numeric_filter))

    for part in weather_parts:
        if 'degrees' in part:
            temp_bit = to_int(part)
        elif 'humidity' in part:
            humid_bit = to_int(part)
        elif 'mph' in part:
            wind_bit = to_int(part)
    return (temp_bit, wind_bit, humid_bit)


def get_weathers(weather_str):
    weather_parts = weather_str.split(', ')
    temperature, wind_speed, humidity = weather_pieces(weather_parts)
    return (temperature, wind_speed, humidity)
