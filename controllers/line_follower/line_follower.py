from controller import Robot

def run_robot(robot):
    time_step = 32
    max_speed = 6.28

    # Motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(1.0)
    right_motor.setVelocity(1.0)

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

    # Step simulation
    while robot.step(time_step) != -1:
        # read ir sensors
        left_ir0_value = round(left_ir0.getValue(),2)
        left_ir1_value = round(left_ir1.getValue(), 2)
        left_ir2_value = round(left_ir2.getValue(), 2)
        
        right_ir0_value = round(right_ir0.getValue(), 2)
        right_ir1_value = round(right_ir1.getValue(), 2)
        right_ir2_value = round(right_ir2.getValue(), 2)
        
        print(f"left: [{left_ir0_value}, {left_ir1_value}, {left_ir2_value}] right: [{right_ir0_value}, {right_ir1_value}, {right_ir2_value}]")
        
        #NORMALIZAÇÃO - PORQUE DESSES VALORES??? -> Investigar
        left_ir0_value = 1 if left_ir0_value< 5 else 0 
        left_ir1_value = 1 if left_ir1_value< 5 else 0
        left_ir2_value = 1 if left_ir2_value< 5 else 0
        
        right_ir0_value = 1 if right_ir0_value< 5 else 0 
        right_ir1_value = 1 if right_ir1_value< 5 else 0 
        right_ir2_value = 1 if right_ir2_value< 5 else 0 
        
        print(f"-Valores normalizados: left: [{left_ir0_value}, {left_ir1_value}, {left_ir2_value}] right: [{right_ir0_value}, {right_ir1_value}, {right_ir2_value}]")
        error = (left_ir0_value + left_ir1_value + left_ir2_value) - (right_ir0_value + right_ir1_value + right_ir2_value)
        print(f"--ERROR: {error}")
        left_speed = max_speed * 0.25
        right_speed = max_speed * 0.25

        #if (left_ir_value > right_ir_value) and (6 < left_ir_value < 15):
            #print("Go left")
            #left_speed = max_speed * 0.25
        #elif (right_ir_value > left_ir_value) and (6 < right_ir_value < 15):
            #print("Go right")
           # right_speed = -max_speed * 0.25

        #left_motor.setVelocity(left_speed)
        #right_motor.setVelocity(right_speed)

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)
