
# Boss 唯一 id 独立于四槽血条；即使四槽已满，近邻战斗也不会串侍从。
scoreboard players add #boom_seq rpg_boom_id 1
scoreboard players operation @s rpg_boom_id = #boom_seq rpg_boom_id
