# prologue_multi hub
scoreboard players operation #n rpg_prh = #q rpg_prh
execute if score #n rpg_prh matches 5.. run scoreboard players set #n rpg_prh 4
execute if score #n rpg_prh matches 1 run title @s actionbar {"text":"正在等待同伴一起进入序章（1/4）…… Waiting for companions (1/4)","color":"#E8D9B0"}
execute if score #n rpg_prh matches 2 run title @s actionbar {"text":"正在等待同伴一起进入序章（2/4）…… Waiting for companions (2/4)","color":"#E8D9B0"}
execute if score #n rpg_prh matches 3 run title @s actionbar {"text":"正在等待同伴一起进入序章（3/4）…… Waiting for companions (3/4)","color":"#E8D9B0"}
execute if score #n rpg_prh matches 4 run title @s actionbar {"text":"正在等待同伴一起进入序章（4/4）…… Waiting for companions (4/4)","color":"#E8D9B0"}
