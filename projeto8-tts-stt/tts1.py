import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import wikipedia
import webbrowser
import requests
from datetime import datetime

class AssistenteVirtual:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def text_to_speech(self, texto, lang='pt-br', slow=False):
        #Converte texto em áudio
        try:
            tts = gTTS(text=texto, lang=lang, slow=slow)
            filename = "resposta.mp3"
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        except Exception as e:
            print(f"Erro no TTS: {e}")

    def speech_to_text(self):
        # Converte fala em texto
        try:
            with self.microphone as source:
                print("Ouvindo...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            texto = self.recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")
            return texto.lower()
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido")
            return ""
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio")
            return ""
        except Exception as e:
            print(f"Erro no STT: {e}")
            return ""

    def pesquisar_wikipedia(self, query):
        #Pesquisa no Wikipedia
        try:
            wikipedia.set_lang('pt')
            resultado = wikipedia.summary(query, sentences=3)
            return resultado
        except:
            return "Não encontrei resultados na Wikipedia"

    def abrir_youtube(self, pesquisa=None):
        #Abre o YouTube
        if pesquisa:
            url = f"https://www.youtube.com/results?search_query={pesquisa}"
        else:
            url = "https://www.youtube.com"
        webbrowser.open(url)
        return f"Abrindo YouTube {'com a pesquisa ' + pesquisa if pesquisa else ''}"

    def localizar_farmacia(self):
        #Encontra a farmácia mais próxima
        # Em uma implementação real, usaria API de geolocalização
        return "A farmácia mais próxima está a 2km da sua localização, na Rua das Flores, 123."

    def dizer_hora(self):
        #Diz a hora
        agora = datetime.now()
        data_formatada = agora.strftime("%d:%m:Y")

        hora_formatada = agora.strftime("%H:%M")
        return f"Agora são {hora_formatada} do dia {data_formatada}"

    def executar_comando(self, comando):
        #Interpreta e executa os comandos
        if 'wikipedia' in comando or 'pesquisar' in comando:
            self.text_to_speech("O que devo pesquisar?")
            pesquisa = self.speech_to_text()
            if pesquisa:
                resultado = self.pesquisar_wikipedia(pesquisa)
                self.text_to_speech("De acordo com a Wikipedia")
                self.text_to_speech(resultado)

        elif 'youtube' in comando:
            if 'pesquisar' in comando:
                self.text_to_speech("O que devo pesquisar no YouTube?")
                pesquisa = self.speech_to_text()
                if pesquisa:
                    self.text_to_speech(self.abrir_youtube(pesquisa))
            else:
                self.text_to_speech(self.abrir_youtube())

        elif 'farmácia' in comando or 'farmacia' in comando:
            self.text_to_speech(self.localizar_farmacia())

        elif 'hora' in comando:
            self.text_to_speech(self.dizer_hora())

        elif 'sair' in comando or 'parar' in comando:
            self.text_to_speech("Até logo!")
            exit()

        else:
            self.text_to_speech("Desculpe, não reconheci esse comando. Diga 'Wikipedia', 'YouTube', 'farmácia', 'hora', ou 'sair'")

    def iniciar(self):
        #Inicia o assistente virtual
        self.text_to_speech("Assistente virtual iniciado. Como posso ajudar?")
        
        while True:
            print("Estou ouvindo...")
            comando = self.speech_to_text()
            if comando:
                self.executar_comando(comando)

# Execução principal
if __name__ == "__main__":
    # Instruções de instalação (descomente se necessário)
    # !pip install speechrecognition gTTS playsound wikipedia requests pyjokes
    
    assistente = AssistenteVirtual()
    assistente.iniciar()