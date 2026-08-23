# 打它没有用 —— 罪落在动手的人身上，壳还会因此裂开。
execute on attacker run scoreboard players add @s rpg_taint 6
execute on attacker run title @s actionbar ["",{"text":"你打碎的只是空壳","italic":true,"color":"dark_gray"}]
execute if entity @s[tag=!rpg.vac.torn] run function rpg:vacant/tear
