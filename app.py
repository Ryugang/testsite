from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 단어 데이터
words = {
    "음식": ["apple(사과)", "korean pancake(전)", "rice cake(떡)", "kimchi stew(김치찌개)", "rice(밥)"],
    "가구": ["television(티비)", "air conditioner(에어컨)", "desk(책상)", "pencil(연필)", "pen(펜)"],
    "생활": ["fun(재밌다)", "look(보다)", "eat(먹다)", "play(놀다)", "chess(화투)"]
}

# 오답 기록용 데이터
wrong_answers = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        button = request.form.get("button")
        if button == "단어 학습":
            return redirect(url_for("learn"))
        elif button == "단어 시험":
            return redirect(url_for("test"))
        elif button == "오답 확인":
            return redirect(url_for("review"))
    return render_template("index.html")

@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        theme = request.form["theme"]
        return render_template("learn.html", theme=theme, words=words[theme])
    return render_template("learn.html", theme="", words=[])

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        theme = request.form["theme"]
        word_index = 0 
        return redirect(url_for("test_word", theme=theme, word_index=word_index))
    return render_template("test.html", theme="", words=[])

@app.route("/test_word/<theme>/<int:word_index>", methods=["GET", "POST"])
def test_word(theme, word_index):
    if request.method == "POST":
        word = words[theme][word_index]
        answer = request.form["answer"]
        if answer == word.split('(')[1][:-1]:  # 정답 비교
            next_word_index = word_index + 1
            if next_word_index < len(words[theme]):
                return redirect(url_for("test_word", theme=theme, word_index=next_word_index))
            else:
                return redirect(url_for("index"))
        else:
            wrong_answers[(theme, word)] = wrong_answers.get((theme, word), 0) + 1
            return render_template("test.html", theme=theme, word_index=word_index, wrong=True, words=words[theme])

    if theme in words:
        if word_index < len(words[theme]):
            return render_template("test.html", theme=theme, word_index=word_index, wrong=False, words=words[theme])
    return redirect(url_for("index"))


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":
        word = request.form["word"]
        theme = request.form["theme"]
        count = int(request.form.get("count", 1))
        if count == 1:
            wrong_answers[(theme, word)] = 1
        else:
            wrong_answers[(theme, word)] = count
        return redirect(url_for("test"))
    return render_template("review.html", wrong_answers=wrong_answers)

if __name__ == "__main__":
    app.run(debug=True)
