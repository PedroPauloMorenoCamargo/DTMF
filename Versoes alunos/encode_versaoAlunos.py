
#importe as bibliotecas
from typing_extensions import Self
import suaBibSignal
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from scipy.io.wavfile import write
import wavio
#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    W = window.hamming(N)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fft(signal*W)
    return(xf, np.abs(yf[0:N//2]))


def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    lista = ["1","2","3","A","4","5","6","B","7","8","9","C","X","0","#","D"]
    lista_inputs = [["1","2","3","A"],["4","5","6","B"],["7","8","9","C"],["X","0","#","D"]]
    sem_input = True
    while sem_input:
        tecla = str(input("Digite uma tecla: "))
        if tecla not in lista:
            print("Erro com input, digite de novo")
        else:
            sem_input = False
    S_rate = 44100
    T = 1/S_rate
    A = 1
    colunas = [1209,1336,1477,1633]
    linhas = [697,770,852,941]
    for i in range(0,4):
        for j in range(0,4):
            if tecla == lista_inputs[i][j]:
                fl = linhas[i]
                fc = colunas[j]
                print(fl,fc)
    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(tecla))
    t = 5
    N = S_rate*t
    wl = 2*np.pi*fl
    wc = 2*np.pi*fc
    teq = np.arange(N)*T
    senoidel = np.sin(wl*teq)
    senoidec = np.sin(wc*teq)
    signal = A*(np.sin(wl*teq)+np.sin(wc*teq))
    sd.play(signal, S_rate)
    # Exibe gráficos
    plt.figure(1)
    plt.plot(teq[200:800],senoidel[200:800],label= f"sinal {fl} hz")
    plt.title(f'Senoide {fl} hz x Tempo')
    plt.ylabel("Amplitude")
    plt.xlabel("Tempo (s)")
    plt.show()
    plt.figure(2)
    plt.plot(teq[200:800],senoidec[200:800],label= f"sinal {fc} hz")
    plt.title(f'Senoide {fc} hz x Tempo')
    plt.ylabel("Amplitude")
    plt.xlabel("Tempo (s)")
    plt.show()
    plt.figure(3)
    plt.plot(teq[200:800],signal[200:800],label= "sinal final")
    plt.title('Senoide Enviada x Tempo')
    plt.ylabel("Amplitude")
    plt.xlabel("Tempo (s)")
    plt.show()
    # aguarda fim do audio
    sd.wait()
    x,y = calcFFT(signal,S_rate)
    plt.figure(4)
    plt.plot(x, np.abs(y))
    plt.title('Fourier')
    plt.xlim([0,1700])
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Im (G)")
    plt.show()
    f = open("sons/0.wav", "x")
    f.close()
    wavio.write("sons/0.wav", signal, S_rate, sampwidth=3)
if __name__ == "__main__":
    main()
