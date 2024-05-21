import streamlit as st
from langchain_openai import ChatOpenAI

# Setze deinen OpenAI API-Schlüssel hier ein
api_key = 'sk-proj-TXuLkPCP4SSIoJRxqyMLT3BlbkFJnNQQhkZGeC3aqeOlY1jl'

# Initialisiere das Sprachmodell
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-3.5-turbo-0301"  # Stelle sicher, dass du das richtige Modell verwendest
)

# Definiere die Prompts für die verschiedenen Schwierigkeitsgrade
prompts = {
    1: "Stelle eine einfache Quizfrage für Kinder.",
    2: "Stelle eine einfache Quizfrage.",
    3: "Stelle eine mittelschwere Quizfrage.",
    4: "Stelle eine schwierige Quizfrage für intelligente Erwachsene."
}

# Definiere eine Funktion, um eine Frage zu generieren
def ask_question(level):
    prompt = prompts[level]
    response = llm.invoke(prompt)
    return response.content.strip()

# Definiere eine Funktion, um die Antwort zu überprüfen
def check_answer(question, user_answer):
    prompt = f"Die Frage war: '{question}'\nDie Antwort des Kindes war: '{user_answer}'\nIst die Antwort richtig oder falsch? Begründe kurz."
    response = llm.invoke(prompt)
    return response.content.strip()

def main():
    st.title("AI Quiz Game")

    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'start'
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.correct_answers = []
        st.session_state.current_question_index = 0
        st.session_state.level = 1
        st.session_state.answer_submitted = False

    def reset_game():
        st.session_state.game_state = 'start'
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.correct_answers = []
        st.session_state.current_question_index = 0
        st.session_state.answer_submitted = False

    if st.session_state.game_state == 'start':
        if st.button("Lass uns spielen"):
            st.session_state.game_state = 'select_level'

    elif st.session_state.game_state == 'select_level':
        st.write("Wähle ein Level:")
        level = st.radio("", [1, 2, 3, 4], index=st.session_state.level - 1, format_func=lambda x: f"Level {x}: " + ["Kinderfragen", "Einfache Fragen", "Mittelschwere Fragen", "Anspruchsvolle Fragen"][x-1])
        st.session_state.level = level
        if st.button("Start"):
            st.session_state.current_question_index = 0
            st.session_state.questions.append(ask_question(level))
            st.session_state.game_state = 'question'

    elif st.session_state.game_state == 'question':
        if st.session_state.current_question_index < 5:
            question = st.session_state.questions[-1]
            st.write(f"Frage {st.session_state.current_question_index + 1}: {question}")
            if not st.session_state.answer_submitted:
                user_answer = st.text_input("Deine Antwort:", key=f"answer_{st.session_state.current_question_index}")

                if st.button("Antwort einreichen"):
                    evaluation = check_answer(question, user_answer)
                    st.session_state.answers.append(user_answer)
                    if "richtig" in evaluation.lower():
                        st.session_state.correct_answers.append(True)
                        st.session_state.score += 1
                        st.success("Richtig!")
                    else:
                        st.session_state.correct_answers.append(False)
                        st.error(f"Falsch! {evaluation}")
                    st.session_state.answer_submitted = True
            else:
                if st.button("Weiter"):
                    st.session_state.current_question_index += 1
                    st.session_state.answer_submitted = False
                    if st.session_state.current_question_index < 5:
                        st.session_state.questions.append(ask_question(st.session_state.level))
                    else:
                        st.session_state.game_state = 'result'
        else:
            st.session_state.game_state = 'result'

    elif st.session_state.game_state == 'result':
        st.write("Quiz beendet!")
        st.write(f"Dein Ergebnis: {st.session_state.score} von 5")
        st.write("Fragen und Antworten:")
        for i in range(5):
            st.write(f"Frage {i+1}: {st.session_state.questions[i]}")
            st.write(f"Deine Antwort: {st.session_state.answers[i]}")
            st.write(f"Richtig: {'Ja' if st.session_state.correct_answers[i] else 'Nein'}")
        if st.button("Neues Spiel"):
            reset_game()

if __name__ == "__main__":
    main()
