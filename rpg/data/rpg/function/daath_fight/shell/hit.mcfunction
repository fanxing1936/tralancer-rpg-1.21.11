# 护盾挨打：#d 十分之一点
scoreboard players operation @s rpg_dt_shell -= #d rpg_dt
playsound minecraft:block.glass.hit hostile @a[distance=..24] ~ ~ ~ 1 1.2
execute if score @s rpg_dt_shell matches ..0 run function rpg:daath_fight/shell/burst
