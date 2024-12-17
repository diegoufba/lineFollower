import matplotlib.pyplot as plt
import pickle

x_graph_erro_medio_PD = []
y_graph_erro_medio_PD = []

x_graph_erro_medio_PDI = []
y_graph_erro_medio_PDI = []

with open(r"C:\Users\felip\OneDrive\Área de Trabalho\Trabalho Robotica 2\v3\lineFollower\x_erro_medio_PD.pkl", "rb") as file:
    x_graph_erro_medio_PD = pickle.load(file)

with open(r"C:\Users\felip\OneDrive\Área de Trabalho\Trabalho Robotica 2\v3\lineFollower\y_erro_medio_PD.pkl", "rb") as file:
    y_graph_erro_medio_PD = pickle.load(file)

with open(r"C:\Users\felip\OneDrive\Área de Trabalho\Trabalho Robotica 2\v3\lineFollower\x_erro_medio_PDI.pkl", "rb") as file:
    x_graph_erro_medio_PDI = pickle.load(file)

with open(r"C:\Users\felip\OneDrive\Área de Trabalho\Trabalho Robotica 2\v3\lineFollower\y_erro_medio_PDI.pkl", "rb") as file:
    y_graph_erro_medio_PDI = pickle.load(file)

fig, ax = plt.subplots()
ax.set_xlim([0, 5000*0.032])
ax.set_ylim([-0.5, 0.5])
ax.set_title(f"Erro Médio X Tempo")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Erro Médio")

ax.plot(x_graph_erro_medio_PD, y_graph_erro_medio_PD, label="PD", color='black')  # Linha azul com legenda "PD"

# Adicionar a segunda linha
ax.plot(x_graph_erro_medio_PDI, y_graph_erro_medio_PDI, label="PDI", color='green')  # Linha vermelha com legenda "PDI"

ax.axvline(x=4845*0.032, color='red', linestyle='--') # Adiciona a linha vertical em x=3450, quando aproximadamente completa uma volta          

ax.legend()

plt.show()