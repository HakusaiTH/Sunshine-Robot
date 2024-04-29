def iot_call(text):
    commands = {
        "เปิดไฟภายในห้อง": ["led_1", ["ON"]],
        "เปิดไฟในห้อง": ["led_1", ["ON"]],
        "ปิดไฟภายในห้อง": ["led_1", ["OFF"]],
        "ปิดไฟในห้อง": ["led_1", ["OFF"]],
        "เปิดไฟนอกห้อง": ["led_2", ["ON"]],
        "ปิดไฟนอกห้อง": ["led_2", ["OFF"]],
    }

    return commands.get(text, ["unknown_command", []])

'''
# Example usage:
result = iot_call("เปิดไฟภายในห้อง")
print(result[0],result[1][0])
'''
