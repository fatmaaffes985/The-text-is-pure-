from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QMessageBox, QLabel, \
    QTextEdit, QScrollArea
import sys
import re
from functools import partial
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from math import log


def compter(texte):
    exceptions = {
        "d'accord", "d'antan", "d'habitude", "d'ailleurs",
        "d'aventure", "d'emblée", "d'autant", "aujourd'hui"
    }
    text = re.sub(r'[,;:!?.()\-\[\]"]', ' ', texte)
    mots = text.split()
    mots1 = []

    for mot in mots:
        if "'" in mot:
            if mot in exceptions:
                mots1.append(mot)
            else:
                mots1.extend(mot.split("'"))
        else:
            mots1.append(mot)

    return len(mots1)


def lister(texte):
    exceptions = {
        "d'accord", "d'antan", "d'habitude", "d'ailleurs",
        "d'aventure", "d'emblée", "d'autant", "aujourd'hui"
    }
    text = re.sub(r'[,;:!?.()\-\[\]"]', ' ', texte)
    mots = text.split()
    mots1 = []

    for mot in mots:
        if "'" in mot:
            if mot in exceptions:
                mots1.append(mot)
            else:
                mots1.extend(mot.split("'"))
        else:
            mots1.append(mot)

    resultat = []
    mots_vus = []

    for mot in mots1:
        if  mot not in mots_vus:
            mots_vus.append(mot)
            resultat.append(mot)
            resultat.append(mots1.count(mot))

    return resultat
def charger_stopwords(fichier="stopwords_fr.txt"):
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            stopwords = [ligne.strip().lower() for ligne in f if ligne.strip()]
            return stopwords
    except FileNotFoundError:
        print(f"Fichier {fichier} non trouvé, utilisation de la liste par défaut")
        return ["le", "la", "les", "un", "une", "des", "et", "ou", "mais",
                "je", "tu", "il", "elle", "nous", "vous", "ils", "elles"]



def traiter_stopwords(liste_mots, nb):
    stopwords_fr = charger_stopwords()
    results = []

    for i in range(0, len(liste_mots), 2):
        mot = liste_mots[i]
        if mot not in stopwords_fr:
            freq = liste_mots[i + 1]
            results.append(mot)
            results.append(freq)
            tf = freq / nb
            idf = log(nb / (1 + freq))
            results.append(tf * idf)

    return results

[("h",1,0.1),("")]
def trier_par_tfidf(liste):
    triplets = []
    for i in range(0, len(liste), 3):
        triplets.append((liste[i], liste[i + 1], liste[i + 2]))

    triplets.sort(key=lambda x: x[2], reverse=True)

    resultat = []
    for t in triplets:
        resultat.extend([t[0], t[1], t[2]])

    return resultat


def afficher(texte, label):
    text = texte.toPlainText()

    if text == "":
        QMessageBox.critical(w, "Erreur", "Vous devez écrire un texte")
        return
    elif compter(text) < 3:
        QMessageBox.critical(w, "Erreur", "Vous devez écrire au minimum 3 mots")
        return
    else:
        nb = compter(text)
        liste_mots = lister(text)
        nb_mots_uniques = len(liste_mots) // 2
        richesse = (nb_mots_uniques / nb) * 100

        if richesse > 90:
            etoiles = "⭐⭐⭐⭐⭐ Excellent ⭐⭐⭐⭐⭐"
            couleur = "#46ab27"
        elif richesse > 70:
            etoiles = "⭐⭐⭐⭐ Trés Bien ⭐⭐⭐⭐"
            couleur = "#85e069"
        elif richesse > 50:
            etoiles = "⭐⭐⭐ Bien ⭐⭐⭐"
            couleur = "#de9c95"
        elif richesse > 40:
            etoiles = "⭐⭐ Moyen ⭐⭐"
            couleur = "#e87b6f"
        else:
            etoiles = "⭐ Faible ⭐"
            couleur = "#f73520"

        affichage = "<html>"
        affichage += "<h1 style='text-align:center;color:#cfa49f;'>📊 RÉSULTATS DE L'ANALYSE</h1>"
        affichage += f"<h2 style='background-color:{couleur}; color:white; text-align:center; padding:10px;'>{etoiles}</h2>"
        affichage += "<h2>📝 Statistiques générales :</h2>"
        affichage += f"<h3>   • Nombre total de mots : {nb}</h3>"
        affichage += f"<h3>   • Mots uniques : {nb_mots_uniques}</h3>"
        affichage += f"<h3>   • Richesse lexicale : {richesse:.1f}%</h3>"

        liste_avec_tfidf = traiter_stopwords(liste_mots, nb)

        affichage += "<h2>📋 Mots et fréquences (avec TF-IDF) :</h2>"
        for i in range(0, len(liste_avec_tfidf), 3):
            mot = liste_avec_tfidf[i]
            freq = liste_avec_tfidf[i + 1]
            tfidf = liste_avec_tfidf[i + 2]
            affichage += f"<p>   • {mot} : {freq} (TF-IDF: {tfidf:.3f})</p>"

        liste_triee = trier_par_tfidf(liste_avec_tfidf)

        affichage += "<h2>🏆 Top 5 mots (par TF-IDF) :</h2>"
        nb_mots = len(liste_triee) // 3
        if nb_mots < 15:
            nb_afficher = nb_mots
        else:
            nb_afficher = 15

        for i in range(nb_afficher):
            mot = liste_triee[i * 3]
            tfidf = liste_triee[i * 3 + 2]
            affichage += f"<p>   {i + 1}. {mot} : {tfidf:.3f}</p>"

        affichage += "</html>"
        label.setText(affichage)


def effacer(texte, label):
    texte.clear()
    label.setText(
        "📊 RÉSULTATS DE L'ANALYSE \n\n📝 Statistiques générales :\n   • Nombre total de mots : 0\n   • Mots uniques : 0\n   • Richesse lexicale : 0.0%\n\n📋 Mots et fréquences (avec TF-IDF) :\n\n🏆 Top 5 mots (par TF-IDF) :")
    texte.setFocus()
    w.showNormal()


App = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle("Analyseur de Texte Français")
w.setStyleSheet("background-color:#fae5e3;font-weight:bold;")
w.setFont(QFont("Arial", 16))
w.resize(900, 900)

layout = QVBoxLayout()

texte = QTextEdit()
texte.setPlaceholderText("saisissez votre texte ici.....")
texte.setFont(QFont("Segoe UI", 11))
texte.setMinimumHeight(200)
layout.addWidget(texte)

layoutbtn = QHBoxLayout()
btn = QPushButton("Afficher")
btn1 = QPushButton("Effacer")
btn.setStyleSheet("background-color:#dec5bf;font-weight:bold;")
btn1.setStyleSheet("background-color:#dec5bf;font-weight:bold;")
btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
btn1.setFont(QFont("Segoe UI", 11))
layoutbtn.addWidget(btn)
layoutbtn.addWidget(btn1)
layout.addLayout(layoutbtn)

scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setMinimumHeight(350)

label = QLabel("📊 RÉSULTATS DE L'ANALYSE \n\n📝 Statistiques générales :\n"
               "   • Nombre total de mots : 0\n   "
               "   • Mots uniques : 0\n   "
               "   • Richesse lexicale : 0.0%\n\n"
               "📋 Mots et fréquences (avec TF-IDF) :\n\n"
               "🏆 Top 5 mots (par TF-IDF) :")
label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
label.setFont(QFont("Segoe UI", 10))
label.setStyleSheet("border:2px solid white; padding: 10px;")
label.setWordWrap(True)


scroll_area.setWidget(label)
layout.addWidget(scroll_area)

btn.clicked.connect(partial(afficher, texte, label))
btn1.clicked.connect(partial(effacer, texte, label))

w.setLayout(layout)
w.show()
sys.exit(App.exec_())