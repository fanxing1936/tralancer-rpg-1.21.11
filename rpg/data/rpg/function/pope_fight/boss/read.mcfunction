# 每 5 刻读一次血量（一次 NBT），转身面向最近的玩家。
scoreboard players set #h rpg_pf 0
execute store result score #hp rpg_pf run data get entity @s Health
execute store result bossbar minecraft:pope value run scoreboard players get #hp rpg_pf
function rpg:pope_fight/bar/hp
execute if score #hp rpg_pf matches ..40 run return run function rpg:pope_fight/stage3_enter
execute if score #next rpg_pf matches 750 if score #hp rpg_pf matches ..750 run function rpg:pope_fight/boss/wave_due
execute if score #next rpg_pf matches 500 if score #hp rpg_pf matches ..500 run function rpg:pope_fight/boss/wave_due
execute if score #next rpg_pf matches 250 if score #hp rpg_pf matches ..250 run function rpg:pope_fight/boss/wave_due
execute if score #ultl rpg_pf matches 625 if score #hp rpg_pf matches ..625 run function rpg:pope_fight/boss/ult_due
execute if score #ultl rpg_pf matches 375 if score #hp rpg_pf matches ..375 run function rpg:pope_fight/boss/ult_due
execute if score #sk rpg_pf matches 0 facing entity @a[distance=..32,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
