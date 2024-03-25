with open("setting.txt", "r") as f:
    lines = f.readlines()

# 設定値を格納する辞書
settings = {}

for line in lines:
    key, value = line.strip().split("=")
    settings[key] = value

# 設定値を出力
print(f"track_len: {settings['track_len']}")
print(f"track_thickness: {settings['track_thickness']}")
print(f"anomaly_threshold: {settings['anomaly_threshold']}")