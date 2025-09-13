from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Ganti dengan API key OpenAI kamu
openai.api_key = "ISI_API_KEY_MU"

@app.route("/")
def home():
    return render_template("index.html")

# --- BMI Calculator ---
@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    if request.method == "POST":
        tinggi = float(request.form["tinggi"]) / 100
        berat = float(request.form["berat"])
        bmi_val = round(berat / (tinggi**2), 2)

        if bmi_val < 18.5:
            kategori = "Kurus"
        elif bmi_val < 24.9:
            kategori = "Normal"
        elif bmi_val < 29.9:
            kategori = "Overweight"
        else:
            kategori = "Obesitas"

        return render_template("bmi.html", bmi=bmi_val, kategori=kategori)
    return render_template("bmi.html", bmi=None, kategori=None)

# --- Chatbot AI ---
@app.route("/chat", methods=["GET", "POST"])
def chat():
    jawaban = None
    if request.method == "POST":
        pesan = request.form["pesan"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Berikan saran kesehatan untuk remaja Indonesia: {pesan}",
            max_tokens=200
        )
        jawaban = response["choices"][0]["text"].strip()
    return render_template("chat.html", jawaban=jawaban)

# --- Food Log ---
@app.route("/food", methods=["GET", "POST"])
def food():
    kalori = None
    if request.method == "POST":
        makanan = request.form["makanan"]
        # sementara estimasi kalori sederhana
        kalori = f"Estimasi kalori untuk {makanan}: sekitar 250 kkal"
    return render_template("food.html", kalori=kalori)

# --- Activity Tracker ---
@app.route("/activity", methods=["GET", "POST"])
def activity():
    hasil = None
    if request.method == "POST":
        aktivitas = request.form["aktivitas"]
        durasi = float(request.form["durasi"])
        # estimasi sederhana: 5 kkal per menit
        kalori_bakar = durasi * 5
        hasil = f"Anda membakar sekitar {kalori_bakar} kkal dengan {aktivitas}."
    return render_template("activity.html", hasil=hasil)

# --- Report Page ---
@app.route("/report")
def report():
    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)
