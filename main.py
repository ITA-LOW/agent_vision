import cv2
import time
from agent import Agent
from vision import detect_face_position, detect_face_position_yunet
import motion

def main():
    agent = Agent()
    
    plan_library = [
        ('adjust_vision', {'context': {'position': 'top_left'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'top_center'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'top_right'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'middle_left'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'middle_center'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'middle_right'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'bottom_left'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'bottom_center'}, 'plan': ['look_at_position']}),
        ('adjust_vision', {'context': {'position': 'bottom_right'}, 'plan': ['look_at_position']}),
    ]
    
    motion.reset_pos()
    
    agent.set_plan_library(plan_library)
    agent.add_beliefs({'profile': 'confident'})  # Colocar na biblioteca de planos
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print("Erro ao ler o frame.")
            break
        
        # Detecta a posição do rosto
        position = detect_face_position_yunet(frame) # Yunet
        # position = detect_face_position(frame) # Haarcascade
        
        if position:
            agent.add_beliefs({'position': position})
            agent.add_desires("adjust_vision")
            goal = agent.get_desires()
            agent.update_intention(goal)
            agent.execute_intention()
        
        #cv2.imshow("Webcam", frame)   #util para humanos, inutil para o robo
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Encerra o loop se 'q' for pressionado
        
        time.sleep(0.25)  # Delay para processamento
    
    cap.release()
    cv2.destroyAllWindows()
    
    motion.cleanup()

if __name__ == "__main__":
    main()
