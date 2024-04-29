import openai

api_key = "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"
openai.api_key = api_key

def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_log,
        max_tokens=3800,
        stop=None,
        temperature=0.7,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content

def answer_question(user_input):
    message_log = [
        {"role": "system", "content": "Yak Robot เป็นหุ่นยนต์ที่จะทำให้ห้องของคุณสะดวกสบายยิ่งขึ้นด้วยความสามารถในการควบคุมผ่าน อินเทอร์เน็ตของสรรพสิ่ง"},
        {"role": "system", "content": "Yakhotel เป็นโรงแรมแห่งอนาคตที่ผสมผสานเทคโนโลยีหุ่นยนต์ อินเทอร์เน็ตของสรรพสิ่ง และความเป็นไทย..."},
        {"role": "user", "content": "จังหวัด กรุงเทพมหานคร light rain สภาพอากาส 29.09  องศาเซลเซียส ความชื่น 54 %"},
        {"role": "system", "content": "จังหวัด กรุงเทพมหานคร สภาพอากาศปัจจุบันเป็นฝนเล็กน้อย อุณหภูมิอยู่ที่ประมาณ 29.09 องศาเซลเซียส และความชื้นสัมพัทธ์ประมาณ 54% อย่าลืมเตรียมตัวกันน้ำฝนด้วยนะคะ หากมีข้อสงสัยเพิ่มเติม สามารถถามเพิ่มเติมได้เลยค่ะ"},
        {"role": "user", "content": "จังหวัด ระยอง bright สภาพอากาส 25.00  องศาเซลเซียส ความชื่น 54 %"},
        {"role": "system", "content": "จังหวั ดระยอง สภาพอากาศปัจจุบันแจ่มใส อุณหภูมิอยู่ที่ประมาณ 25.00 องศาเซลเซียส และความชื้นสัมพัทธ์ประมาณ 54% ขอให้เป็นเช้าที่แจ่มใสสำหรับคุณ"},       
        {"role": "user", "content": "จังหวัด กรุงเทพมหานคร PM2.5 86 aqi"},
        {"role": "system", "content": "จังหวัด กรุงเทพมหานคร PM2.5 86 aqi เป็นสิ่งสำคัญที่จะระวังและรับมือกับปัญหามลพิษอากาศให้เหมาะสมในพื้นที่นี้ โดยการสวมหน้ากากอนามัยเมื่ออยู่นอกบ้าน"},       
        {"role": "user", "content": "จังหวัด ระยอง PM2.5 50 aqi"},
        {"role": "system", "content": "จังหวัด ระยอง PM2.5 50 aqi เป็นค่าที่เหมาะสำหรับกิจกรรมนอกบ้าน"},       
    ]

    first_request = True

    if first_request:
        message_log.append({"role": "user", "content": user_input})
        response = send_message(message_log)
        message_log.append({"role": "assistant", "content": response})
        return response
        first_request = False
    else:
        message_log.append({"role": "user", "content": user_input})
        response = send_message(message_log)
        message_log.append({"role": "assistant", "content": response})
        return response
    
# print(answer_question("Yak Robot คืออะไร"))
# print(answer_question("จังหวัด กรุงเทพมหานคร light rain สภาพอากาส 29.09  องศาเซลเซียส ความชื่น 54 %"))
# print(answer_question("จังหวัด กรุงเทพมหานคร PM2.5 86 เอคิวไอ"))  