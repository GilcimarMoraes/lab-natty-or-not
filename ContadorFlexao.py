import mediapipe as mp 
import cv2 as cv
import numpy as np

"""def calcular_angulo(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radianos = np.arctan2(c[1] - b[1], c[0] - b[0] - np.arctan2(a[1] - b[1], a[0] - b[0]))
    angulo = np.abs(radianos * 180.0 / np.pi)

    if angulo > 180.0:
        angulo = 360 - angulo

    return angulo"""

# Como a primeira função não conseguiu efetuar a contagem estou alterando para o calculo da distancia euclidiana entre dois pontos
def calcular_distancia(ponto1, ponto2):
    return np.linalg.norm(np.array(ponto1) - np.array(ponto2))

cap = cv.VideoCapture('flexao.mp4')

# Configurando mediapipe pose

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

# Variaveis do Contador
contador = 0
#momento = 0
momento = None

# Processamento do video
while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Convertendo imagem para RGB
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose.process(image)
    
    # Convertendo imagem de volta para RGB
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        """# Pegando pontos necessários
        ombro = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        cotovelo = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        pulso = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # Calculando o ângulo do cotovelo
        angulo = calcular_angulo(ombro, cotovelo, pulso)

        # Lógica de contagem de flexao
        if angulo > 160:
            momento = "cima"
        
        if angulo < 90 and momento == 'cima':
            momento = "baixo"
            contador += 1"""

        # Posições relevantes: Nariz e pulso esquerdo
        nariz = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
        pulso = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        #Calulando a distância entre o nariz e o pulso
        distancia = calcular_distancia(nariz, pulso)

        # Imprimindo a distância para análise
        #print(f"Distância: {distancia:.4f}")


        # Definindo os limites empíricos para determinar "baixo" e "cima"
        if distancia < 0.15: #flexão completa (nariz proximo ao pulso)
            momento = "baixo"

        elif distancia > 0.30 and momento == "baixo":
            momento = "cima"
            contador += 1
        

        # Exibição do contador
        cv.putText(image, f'Flexoes: {contador}', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)

    # Renderizando os pontos de referência
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

   # points = results.pose_landmarks
   # mp_drawing.draw_landmarks(image, points, mp_pose.POSE_CONNECTIONS)

    # Exibindo o vídeo
    cv.imshow('Flexoes', image)

    if cv.waitKey(40) & 0XFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()