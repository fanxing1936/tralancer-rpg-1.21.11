execute store result score #d rpg_q_st run time query day
execute if score #d rpg_q_st = @s rpg_q_fd run function rpg:quest/title/get_waverer
