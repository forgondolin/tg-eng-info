#%%
import pandas as pd
import json

if 1 == 1:
  faces_path = 'src/result_faces_scaleFactor_13_minNeighbors_5_minSize_30_30.json'
  no_faces_path = 'src/result_no_faces_scaleFactor_13_minNeighbors_5_minSize_30_30.json'
  test_check = 0.9999999999999999
else:
  faces_path = 'src/result_faces_scaleFactor_105_minNeighbors_3_minSize_30_30.json'
  no_faces_path = 'src/result_no_faces_scaleFactor_105_minNeighbors_3_minSize_30_30.json'
  test_check = 1

with open(faces_path) as json_file:
  result_faces = json.load(json_file)
result_faces["raw_result"] = result_faces["raw_result"][:17130]
print(len(result_faces["raw_result"]))

with open(no_faces_path) as json_file:
  result_no_faces = json.load(json_file)
result_no_faces["raw_result"] = result_no_faces["raw_result"][:17130]
print(len(result_no_faces["raw_result"]))

#%%
# Count faces

def add_counts(result_data):
  result_data["count_imgs"] = len(result_data["raw_result"])
  result_data["count_0"] = 0
  result_data["count_1"] = 0
  result_data["count_2"] = 0
  result_data["count_1+"] = 0
  for img in result_data["raw_result"]:
      if img["face_count"] == 0:
        result_data["count_0"] += 1
      elif img["face_count"] == 1:
        result_data["count_1"] += 1
        result_data["count_1+"] += 1
      else:
        result_data["count_2"] += 1
        result_data["count_1+"] += 1
  print(str(result_data["count_0"]) + " images with 0 faces (" + str(result_data["count_0"] * 100 / result_data["count_imgs"]) + "%)")
  print(str(result_data["count_1"]) + " images with 1 faces (" + str(result_data["count_1"]*100/result_data["count_imgs"]) + "%)")
  print(str(result_data["count_1+"]) + " images with 1 or more faces (" + str(result_data["count_1+"]*100/result_data["count_imgs"]) + "%)")
  print(str(result_data["count_2"]) + " images with 2 or more faces (" + str(result_data["count_2"]*100/result_data["count_imgs"]) + "%)")

print("=== Faces ===")
add_counts(result_faces)

print("=== No Faces ===")
add_counts(result_no_faces)

#%% [markdown]

# +---------------------+-------------------------+----------------------+------+
# |                     | (B) Não Face (previsto) | (xB) Face (previsto) |      |
# +---------------------+-------------------------+----------------------+------+
# | (A) Não Face (real) |           B_A           |         xB_A         |  P_A |
# +---------------------+-------------------------+----------------------+------+
# |   (xA) Face (real)  |           B_xA          |         xB_xA        | P_xA |
# +---------------------+-------------------------+----------------------+------+
# |                     |           P_B           |         P_xB         |   1  |
# +---------------------+-------------------------+----------------------+------+

#%%

results_total = result_faces["count_imgs"] + result_no_faces["count_imgs"] # Universo
P_A = result_no_faces["count_imgs"] / results_total
P_xA = result_faces["count_imgs"] / results_total
P_B = (result_no_faces["count_0"] + result_faces["count_0"]) / results_total
P_xB = (result_no_faces["count_1+"] + result_faces["count_1+"]) / results_total
print([P_A, P_xA, sum([P_A, P_xA])])
assert sum([P_A, P_xA]) == 1, "Todas imagens devem ter ou nao faces"
print([P_B, P_xB, sum([P_B, P_xB])])
assert sum([P_B, P_xB]) == 1, "Todas previsoes devem ter ou nao faces"

P_A_n_B = result_no_faces["count_0"] / results_total
P_xA_n_B = result_faces["count_0"] / results_total
P_A_n_xB = result_no_faces["count_1+"] / results_total
P_xA_n_xB = result_faces["count_1+"] / results_total
print([P_A_n_B, P_xA_n_B, P_A_n_xB, P_xA_n_xB, sum([P_A_n_B, P_xA_n_B, P_A_n_xB, P_xA_n_xB])])
assert sum([P_A_n_B, P_xA_n_B, P_A_n_xB, P_xA_n_xB]) == test_check, "Todas intersecoes somam 1"

P_B_A = P_A_n_B / P_A
P_xB_A = P_A_n_xB / P_A
P_B_xA = P_xA_n_B / P_xA
P_xB_xA = P_xA_n_xB / P_xA
print([P_B_A, P_xB_A, sum([P_B_A, P_xB_A])])
assert sum([P_B_A, P_xB_A]) == 1, "Uma nao face pode so ser prevista como face ou nao"
print([P_B_xA, P_xB_xA, sum([P_B_xA, P_xB_xA])])
assert sum([P_B_xA, P_xB_xA]) == 1, "Uma face pode so ser prevista como face ou nao"

result_print = [[P_B_A, P_xB_A, P_A],
          [P_B_xA, P_xB_xA, P_xA],
          [P_B, P_xB, 1]]
pd.DataFrame(result_print, columns=["(B) Não Face (previsto)", "(xB) Face (previsto)", ""], index=["(A) Não Face (real)", "(xA) Face (real)", ""])
