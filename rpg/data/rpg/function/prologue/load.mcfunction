# prologue_multi hub
# 序章调度（prologue_multi.py）：每个战场的计分项、血条在各自的 load 里
scoreboard objectives add rpg_pr_g dummy
scoreboard objectives add rpg_pr_qt dummy
scoreboard objectives add rpg_prh dummy
execute in rpg:armageddon run function rpg:prologue_i1/load
execute in rpg:armageddon run function rpg:michael_boss_i1/load
execute unless score #owe rpg_pr_i1 matches 0.. run scoreboard players set #owe rpg_pr_i1 0
execute in rpg:armageddon_2 run function rpg:prologue_i2/load
execute in rpg:armageddon_2 run function rpg:michael_boss_i2/load
execute unless score #owe rpg_pr_i2 matches 0.. run scoreboard players set #owe rpg_pr_i2 0
execute in rpg:armageddon_3 run function rpg:prologue_i3/load
execute in rpg:armageddon_3 run function rpg:michael_boss_i3/load
execute unless score #owe rpg_pr_i3 matches 0.. run scoreboard players set #owe rpg_pr_i3 0
execute in rpg:armageddon_4 run function rpg:prologue_i4/load
execute in rpg:armageddon_4 run function rpg:michael_boss_i4/load
execute unless score #owe rpg_pr_i4 matches 0.. run scoreboard players set #owe rpg_pr_i4 0
