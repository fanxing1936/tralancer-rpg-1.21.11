# prologue_multi hub
execute as @a[scores={rpg_pr_lv=1..}] run function rpg:prologue/rejoin
execute in rpg:armageddon run function rpg:prologue_i1/tick
execute if score #fight rpg_mk_i1 matches 1 in rpg:armageddon run function rpg:michael_boss_i1/tick
execute in rpg:armageddon_2 run function rpg:prologue_i2/tick
execute if score #fight rpg_mk_i2 matches 1 in rpg:armageddon_2 run function rpg:michael_boss_i2/tick
execute in rpg:armageddon_3 run function rpg:prologue_i3/tick
execute if score #fight rpg_mk_i3 matches 1 in rpg:armageddon_3 run function rpg:michael_boss_i3/tick
execute in rpg:armageddon_4 run function rpg:prologue_i4/tick
execute if score #fight rpg_mk_i4 matches 1 in rpg:armageddon_4 run function rpg:michael_boss_i4/tick
scoreboard players add #sec rpg_prh 1
execute if score #sec rpg_prh matches 20.. run function rpg:prologue/queue
