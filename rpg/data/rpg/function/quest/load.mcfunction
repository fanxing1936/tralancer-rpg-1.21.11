scoreboard objectives add rpg_q_st dummy
scoreboard objectives add rpg_q_mt dummy
scoreboard objectives add rpg_q_fd dummy
scoreboard objectives add rpg_q_eg dummy
scoreboard objectives add rpg_q_em dummy
scoreboard objectives add rpg_title dummy
scoreboard objectives add rpg_q1 dummy
scoreboard objectives add rpg_q2 dummy
scoreboard objectives add rpg_q3 dummy
scoreboard objectives add rpg_q4 dummy
scoreboard objectives add rpg_q5 dummy
scoreboard objectives add rpg_q6 dummy
scoreboard objectives add rpg_qc1 dummy
scoreboard objectives add rpg_qc2 dummy
scoreboard objectives add rpg_qc3 dummy
scoreboard objectives add rpg_qc4 dummy
scoreboard objectives add rpg_qc5 dummy
scoreboard objectives add rpg_qc6 dummy
scoreboard objectives add rpg_q_do trigger
bossbar add rpg:quest_sub ""
bossbar set rpg:quest_sub color pink
team add rpg_t_gate
team modify rpg_t_gate prefix ["",{"text":"","font":"rpg:world_titles","color":"white"},{"text":" ","color":"white"}]
team add rpg_t_ledger
team modify rpg_t_ledger prefix ["",{"text":"","font":"rpg:world_titles","color":"white"},{"text":" ","color":"white"}]
team add rpg_t_waverer
team modify rpg_t_waverer prefix ["",{"text":"","font":"rpg:world_titles","color":"white"},{"text":" ","color":"white"}]
team add rpg_t_grandmaster
team modify rpg_t_grandmaster prefix ["",{"text":"","font":"rpg:world_titles","color":"white"},{"text":" ","color":"white"}]
team add rpg_t_meteor
team modify rpg_t_meteor prefix ["",{"text":"","font":"rpg:world_titles","color":"white"},{"text":" ","color":"white"}]
team add rpg_t_merchant
team modify rpg_t_merchant prefix ["",{"text":"","font":"rpg:world_titles","color":"white"},{"text":" ","color":"white"}]
