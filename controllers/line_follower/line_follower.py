from controller import Robot
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run_robot(robot):
    time_step = 32
    max_speed = 1.0

    # Motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(max_speed)
    right_motor.setVelocity(max_speed)

    # Enable ir sensors
    left_ir0 = robot.getDevice('ir0left')
    left_ir0.enable(time_step)
    left_ir1 = robot.getDevice('ir1left')
    left_ir1.enable(time_step)
    left_ir2 = robot.getDevice('ir2left')
    left_ir2.enable(time_step)
    
    right_ir0 = robot.getDevice('ir0right')
    right_ir0.enable(time_step)
    right_ir1 = robot.getDevice('ir1right')
    right_ir1.enable(time_step)
    right_ir2 = robot.getDevice('ir2right')
    right_ir2.enable(time_step)
    
    controller = True #True para PD, False para PDI
    
    graph1Timing = 0
    graph1GenerationTiming = 0
    aux_erros = []
    aux_times = 1
    
    tempo_estabilizacao = 0
    tempo_decorrido = 0
    
    erro_anterior = 0
    integral_erro = 0
    limite_integral = 10
    
    #DETECTION THRESHOLD (Preto 296.02, Branco 59.2)
    ir_threshould = 200.0
    
    #CONSTANTES DOS CONTROLADORES
    kd_PD = 1
    kp_PD = 1
    
    kd_PDI = 1
    kp_PDI = 0.5
    ki_PDI = 0.1
    
    #1, 0.5, 4
    
    #VETORES DOS GRAFICOS
    x_graph_erro_medio = []
    y_graph_erro_medio = []
    
    x_graph_estabilizacao = []
    y_graph_estabilizacao = []
    
    # Step simulation
    while robot.step(time_step) != -1:
        
        # read ir sensors
        left_ir0_value = round(left_ir0.getValue(),2)
        left_ir1_value = round(left_ir1.getValue(), 2)
        left_ir2_value = round(left_ir2.getValue(), 2)
        
        right_ir0_value = round(right_ir0.getValue(), 2)
        right_ir1_value = round(right_ir1.getValue(), 2)
        right_ir2_value = round(right_ir2.getValue(), 2)
        
        #print(f"left: [{left_ir0_value}, {left_ir1_value}, {left_ir2_value}] right: [{right_ir0_value}, {right_ir1_value}, {right_ir2_value}]")
        
        #ABSTRACAO APLICADA: 0 significa não detecta a linha preta e 1 significa detecta a linha preta em vez de representar as cores
        left_ir0_value = 0 if left_ir0_value< ir_threshould else 1 
        left_ir1_value = 0 if left_ir1_value< ir_threshould else 1
        left_ir2_value = 0 if left_ir2_value< ir_threshould else 1
        
        right_ir0_value = 0 if right_ir0_value< ir_threshould else 1 
        right_ir1_value = 0 if right_ir1_value< ir_threshould else 1 
        right_ir2_value = 0 if right_ir2_value< ir_threshould else 1 
        
        #print(f"-Valores normalizados: left: [{left_ir0_value}, {left_ir1_value}, {left_ir2_value}] right: [{right_ir0_value}, {right_ir1_value}, {right_ir2_value}]")
        erro = (left_ir0_value + 2*left_ir1_value + 3*left_ir2_value) - (right_ir0_value + 2*right_ir1_value + 3*right_ir2_value)
        
        #GRAFICO 1 - Erro medio X Tempo
        if graph1Timing >= time_step*50: #Registra o erro medio apos 50 time_steps, 1.6 segundos
               
            x_graph_erro_medio.append(0.032*50*aux_times)
            y_graph_erro_medio.append(np.mean(aux_erros))
            
            aux_erros = []
            aux_times += 1
            graph1Timing = 0
            
        else:
            aux_erros.append(erro) #acumula o erro nos 50 time steps
            graph1Timing += time_step
            
        if graph1GenerationTiming >= 5000*time_step: #gera um grafico a cada pouco mais que 2 minutos, uma volta completa e mais um pouco
            
            #with open(r"C:\Users\felip\OneDrive\Área de Trabalho\Trabalho Robotica 2\v3\lineFollower\x_erro_medio_PDI.pkl", "wb") as file:
               #pickle.dump(x_graph_erro_medio, file)
               
            #with open(r"C:\Users\felip\OneDrive\Área de Trabalho\Trabalho Robotica 2\v3\lineFollower\y_erro_medio_PDI.pkl", "wb") as file:
               #pickle.dump(y_graph_erro_medio, file)    
            
            fig, ax = plt.subplots()
            ax.set_xlim([0, 5000*0.032])
            ax.set_ylim([-0.5, 0.5])
            ax.set_title(f"Erro Médio X Tempo")
            ax.set_xlabel("Tempo (s)")
            ax.set_ylabel("Erro Médio")
            
            ax.axvline(x=4845*0.032, color='red', linestyle='--', label="x = 110") # Adiciona a linha vertical em x=3450, quando aproximadamente completa uma volta          
           
            graph = ax.plot(x_graph_erro_medio, y_graph_erro_medio, color='black')[0]
            plt.show()
            
            graph1GenerationTiming = 0        
            
        else:
            graph1GenerationTiming += time_step
        #GRAFICO 1 - Erro medio X Tempo
         
        #GRAFICO 2 - Tempo de estabilizacao X Duracao do trajeto
        tempo_decorrido +=1
         
        if erro != 0:
            tempo_estabilizacao += 1
        else:
           x_graph_estabilizacao.append(tempo_decorrido)
           y_graph_estabilizacao.append(tempo_estabilizacao)
           tempo_estabilizacao = 0
           
        if tempo_decorrido == 4845: #gera um grafico a cada pouco mais que 2 minutos, uma volta completa e mais um pouco
            fig, ax = plt.subplots()
            ax.set_xlim([0, 4845])
            ax.set_ylim([0, 5])
            ax.set_title(f"Tempo de estabilização X Duração do trajeto")
            ax.set_xlabel("Duração do trajeto (TS)")
            ax.set_ylabel("Tempo de estabilização (TS)")
                       
            graph = ax.plot(x_graph_estabilizacao, y_graph_estabilizacao, color='black')[0]
            plt.show()
            
            tempo_estabilizacao = 0
            tempo_decorrido = 0
            #GRAFICO 2 - Tempo de estabilizacao X Duracao do trajeto    
          

        if controller: #Switch PD e PDI
            #PD
            derivada_erro = (erro - erro_anterior)/time_step
            controle = erro*kp_PD + derivada_erro*kd_PD
            
            #print(f"---CONTROLE: {controle}")
            
            if controle > 0: #Significa que os sensores da esquerda do robô estão sobre a faixa, está virando para a direita ajustar para a esquerda
                left_motor.setVelocity(max_speed-controle)
                right_motor.setVelocity(max_speed+controle)
            elif controle < 0: #Significa que os sensores da direita do robô estão sobre a faixa, o robo está virando para a esquerda ajustar para a direita
                left_motor.setVelocity(max_speed-controle)
                right_motor.setVelocity(max_speed+controle)
            else:
                left_motor.setVelocity(max_speed)
                right_motor.setVelocity(max_speed)
            
            #print(f"--ERROR: {erro}")
            
            erro_anterior = erro   
        else:
            #PDI
            derivada_erro = (erro - erro_anterior)/time_step
            
            integral_erro += erro
            if integral_erro > limite_integral:
                integral_erro = limite_integral
            elif integral_erro < -limite_integral:
                integral_erro = -limite_integral
                
            if erro == 0: 
                integral_erro *= 0.9
                
            
            controle = erro*kp_PDI + derivada_erro*kd_PDI + integral_erro*ki_PDI
            #print(f"---CONTROLE: {controle}")
                
            if controle > 0: #Significa que os sensores da esquerda do robô estão sobre a faixa, está virando para a direita ajustar para a esquerda
                left_motor.setVelocity(max_speed-controle)
                right_motor.setVelocity(max_speed+controle)
            elif controle < 0: #Significa que os sensores da direita do robô estão sobre a faixa, o robo está virando para a esquerda ajustar para a direita
                left_motor.setVelocity(max_speed-controle)
                right_motor.setVelocity(max_speed+controle)
            else:
                left_motor.setVelocity(max_speed)
                right_motor.setVelocity(max_speed)
            
            #print(f"--ERROR: {erro}")
            
            erro_anterior = erro   
                

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)
