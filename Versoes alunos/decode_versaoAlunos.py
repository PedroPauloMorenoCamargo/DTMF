
#Importe todas as bibliotecas
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.fftpack import fft
from scipy import signal as window

#funcao para transformas intensidade acustica em dB, caso queira usar
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

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   

       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2#numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  2 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("CAPTAÇÃO COMEÇA EM 4 SEGUNDOS")
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    time.sleep(4)
    #para gravar, utilize
    audio = sd.rec(int(2*44100), 44100,1)
    sd.wait()
    print("...     FIM")
    sd.play(audio)
    sd.wait()
    print(np.size(audio))
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    n = np.size(audio)
    t = np.linspace(0,2,n)
    
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    plt.plot(t[15000:15750],audio[:,0][15000:15750])
    plt.title("Aúdio recebido x Tempo")
    plt.ylabel("Amplitude")
    plt.xlabel("Tempo (s)")
    plt.show()
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = calcFFT(audio[:,0], 44100)
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.
    plt.figure(4)
    plt.plot(xf, np.abs(yf))
    plt.title('Fourier')
    plt.xlim([0,2000])
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Im (G)")
    plt.show()
    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.05, min_dist=50)
    picos = []
    for i in index:
        picos.append(int(xf[i]))

    print(f"Os picos encontrados foram {picos}")
    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF
    colunas = [1209,1336,1477,1633]
    linhas = [697,770,852,941]
    menor_dif_linha = 20000
    menor_dif_c = 20000000
    menor_coluna = 0
    menor_linha = 0
    for i in picos:
        for col in colunas:  
            if np.abs(col-i) < menor_dif_c:
                menor_coluna = col
                menor_dif_c = np.abs(col-i)
        for linha in linhas:  
            if np.abs(linha-i) < menor_dif_linha:
                menor_linha= linha
                menor_dif_linha = np.abs(linha-i)
    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 
    lista_inputs = [["1","2","3","A"],["4","5","6","B"],["7","8","9","C"],["X","0","#","D"]]
    print(f"A tecla apertada foi {lista_inputs[linhas.index(menor_linha)][colunas.index(menor_coluna)]}")

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
